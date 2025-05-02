import random
import string
import re
import sqlite3
from flask import Flask, request, redirect, render_template, url_for


app = Flask(__name__)
sql = sqlite3.connect("database", check_same_thread=False)
con = sql.cursor()


def create_database():
    query = """CREATE TABLE IF NOT EXISTS links (
id INTEGER PRIMARY KEY AUTOINCREMENT,
long_link TEXT NOT NULL UNIQUE,
shorcut_link TEXT NOT NULL UNIQUE
) """
    con.execute(query)
    sql.commit()


def add_to_database(long_link: str, shorcuted_link: str) -> bool:
    try:
        query = "INSERT INTO links (long_link, shorcut_link) VALUES (?, ?)"
        rows = con.execute(query, [long_link, shorcuted_link])
        sql.commit()
        return True
    except Exception as e:
        return False


def create_shorcut_link() -> str:
    charset = string.ascii_letters + string.digits
    while True:
        shorcut_link = ''.join(random.choices(charset, k=4))
        if len(con.execute("SELECT id FROM links WHERE shorcut_link = ?", [shorcut_link]).fetchall()) == 0:
            return shorcut_link
    

def link_is_in_database(shor_link: str) -> str:
    query = "SELECT long_link FROM links WHERE shorcut_link = ?"
    rows = con.execute(query, [shor_link]).fetchall()
    if len(rows) == 0:
        return ''
    return rows[0][0]

def shorcut_link_is_in_database(long_link: str) -> str:
    query = "SELECT shorcut_link FROM links WHERE long_link = ?"
    rows = con.execute(query, [long_link]).fetchall()
    if len(rows) == 0:
        return ''
    return rows[0][0]

def is_a_valid_website(link: str) -> bool:
    pattern = r'((?:http(?:s)?://)?(?:\w+(?:\.|\:)[\w\W]+)+)'
    patt_compiled = re.compile(pattern)
    results = patt_compiled.findall(link)
    if len(results) > 0:
        return True
    return False

create_database()

@app.route("/", methods=["GET", "POST"])
def index():
    standard_host = "localhost:5000"
    if request.method == "GET":
        return render_template("index.html", shortened_link="", full_link=f"{ standard_host }", message="")
    
    long_link: str = request.form.get("original-link")
    
    if not is_a_valid_website(long_link):
        return render_template("index.html", shortened_link="", full_link=f"{ standard_host }", message="Unrecognizable link")

    if not long_link:
        return redirect(url_for("index"))
    
    link = shorcut_link_is_in_database(long_link)
    if link:
        return render_template("index.html", shortened_link=f'{ link }', full_link=f'{ standard_host }/{ link }', message="")

    shorcut_link = create_shorcut_link()
    
    if not add_to_database(long_link, shorcut_link):
        message = "Oops! Something went wrong. Please try again later."

        return render_template("index.html", shortened_link="", message=message)
    
    return render_template("index.html", shortened_link=f'{ shorcut_link }', full_link=f'{ standard_host }/{ shorcut_link }', message="")


@app.route("/<shor_link>", methods=["GET"])
def redirecting(shor_link):
    if shor_link:
        link = link_is_in_database(shor_link)
        if link:
            return redirect(link)
        return redirect(url_for("index"))


