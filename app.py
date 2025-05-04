import inspect
import random
import re
import sqlite3
import string
from flask import Flask, g, request, redirect, render_template, url_for
# from flask_limiter import Limiter



DATABASE = "database.db"
app = Flask(__name__)
# limiter = Limiter(
#    key_func=lambda: request.remote_addr,
#    app=app,
#)


def get_database():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_database():
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.teardown_appcontext
def teardown_db(e):
    close_database()


def initialize_database():
    with app.app_context():
        db = get_database()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command("initdb")
def initdb_command():
    """Initialize the database."""
    initialize_database()
    print("Initialized the database.")


def add_to_database(long_link: str, short_link: str) -> bool:
    try:
        db = get_database()
        cursor = db.cursor()
        query = "INSERT INTO links (long_link, short_link_code) VALUES (?, ?)"
        rows = cursor.execute(query, [long_link, short_link])
        db.commit()
        return True
    except Exception as e:
        function_name = inspect.currentframe().f_code.co_name
        print(f"Error {e} at function {function_name}")
        return False


def gen_short_link_code() -> str:
    charset = string.ascii_letters + string.digits
    db = get_database()
    cursor = db.cursor()
    while True:
        short_link_code = ''.join(random.choices(charset, k=4))
        if len(cursor.execute("SELECT id FROM links WHERE short_link_code = ?", [short_link_code]).fetchall()) == 0:
            return short_link_code
    

def is_long_link_in_db(short_link_code: str) -> str:
    db = get_database()
    cursor = db.cursor()
    query = "SELECT long_link FROM links WHERE short_link_code = ?"
    rows = cursor.execute(query, [short_link_code]).fetchall()
    if len(rows) == 0:
        return ''
    return rows[0][0]


def is_short_link_in_db(long_link: str) -> str:
    db = get_database()
    cursor = db.cursor()
    query = "SELECT short_link_code FROM links WHERE long_link = ?"
    rows = cursor.execute(query, [long_link]).fetchall()
    if len(rows) == 0:
        return ''
    return rows[0][0]


def is_a_valid_url(link: str) -> bool:
    pattern = r'((?:http(?:s)?://)?(?:\w+(?:\.|\:)[\w\W]+)+)'
    patt_compiled = re.compile(pattern)
    results = patt_compiled.findall(link)
    if len(results) > 0:
        return True
    return False


@app.route("/", methods=["GET"])
def index_get():

    standard_host = f"localhost:{ request.host.split(":")[1] }"

    return render_template("index.html", short_link_code="", redirect_link=f"{ standard_host }", message="")


@app.route("/", methods=["POST"])
# @limiter.limit("5 per minute")
def index_post():
    standard_host = f"{ request.host }"

    long_link: str = request.form.get("original-link")
    if not long_link:
        return redirect(url_for("index"))
    
    if not is_a_valid_url(long_link):
        message = "Unrecognizable link"
        return render_template("index.html", short_link_code="", redirect_link=f"{ standard_host }", message=message)
    
    if short_link_code := is_short_link_in_db(long_link):
        return render_template("index.html", short_link_code=f'{ short_link_code }', redirect_link=f'{ standard_host }/{ short_link_code }', message="")

    short_link_code: str = gen_short_link_code()
    if not add_to_database(long_link, short_link_code):
        message: str = "Oops! Something went wrong. Please try again later."
        return render_template("index.html", short_link_code="", message=message)
    
    return render_template("index.html", short_link_code=f'{ short_link_code }', redirect_link=f'{ standard_host }/{ short_link_code }', message="")


@app.route("/<shor_link_code>", methods=["GET"])
def redirecting(shor_link_code: str):
    if shor_link_code:
        long_link = is_long_link_in_db(shor_link_code)
        if long_link:
            return redirect(long_link)
        return redirect(url_for("index_get"))


