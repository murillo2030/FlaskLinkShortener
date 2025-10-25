import inspect
import os
import random
import re
import sqlite3
import string
from flask import Flask, g, request, redirect, render_template, url_for
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address




DATABASE = "database.db"

app = Flask(__name__)
# limiter = Limiter(
#    get_remote_address,
#    app=app,
#    storage_uri="redis://localhost:6379",
#    storage_options={"socket_connect_timeout": 30},
# )


def get_database() -> str | None:
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_database() -> None:
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.teardown_appcontext
def teardown_db(e) -> None:
    close_database()


def initialize_database() -> None:
    with app.app_context():
        db = get_database()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()
        

@app.cli.command("initdb")
def initdb_command() -> None:
    """Initialize the database."""
    initialize_database()
    print("Database initialized.")


def add_to_database(long_link: str, short_link_code: str) -> bool:
    try:
        db = get_database()
        cursor = db.cursor()
        query = "INSERT INTO links (long_link, short_link_code) VALUES (?, ?)"
        rows = cursor.execute(query, [long_link, short_link_code])
        db.commit()
        return True
    except Exception as e:
        function_name = inspect.currentframe().f_code.co_name
        print(f"Error {e} at function {function_name}")
        return False


def generate_short_link_code() -> str:
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
    pattern_object = re.compile(pattern)
    results = pattern_object.findall(link)
    if len(results) > 0:
        return True
    return False

def is_a_valid_short_link(shor_link_code: str) -> bool:
    pattern = r'[a-zA-Z0-9]{4}'
    pattern_object = re.compile(pattern)
    results = pattern_object.findall(shor_link_code)
    if len(results) > 0:
        return True
    return False


@app.route("/", methods=["GET"])
# @limiter.limit("120 per minute")
def index_get():
    standard_host = f"{ request.host }"
    return render_template("index.html", short_link_code="", redirect_link=f"{ standard_host }", message="")


@app.route("/", methods=["POST"])
# @limiter.limit("5 per minute")
def index_post():
    standard_host = f"{ request.host }"
    long_link: str = request.form.get("long-link")
    
    if not long_link:
        return redirect(url_for("index"))

    if not is_a_valid_url(long_link):
        message = "Unrecognizable link"
        return render_template("index.html", short_link_code="", redirect_link=f"{ standard_host }", message=message)
    
    if short_link_code := is_short_link_in_db(long_link):
        return render_template("index.html", short_link_code=f'{ short_link_code }', redirect_link=f'{ standard_host }/{ short_link_code }', message="")

    short_link_code: str = generate_short_link_code()
    if not add_to_database(long_link, short_link_code):
        message: str = "Oops! Something went wrong. Please try again later."
        return render_template("index.html", short_link_code="", message=message)

    return render_template("index.html", short_link_code=f'{ short_link_code }', redirect_link=f'{ standard_host }/{ short_link_code }', message="")


@app.route("/<short_link_code>", methods=["GET"])
# @limiter.limit("15 per minute")
def redirecting(short_link_code: str):
    if is_a_valid_short_link(short_link_code):
        long_link = is_long_link_in_db(short_link_code)
        if long_link:
            return redirect(long_link)
    return redirect(url_for("index_get"))
    

@app.route("/get/link/<short_link_code>")
# @limiter.limit("15 per minute")
def get_link(short_link_code: str):
    if is_a_valid_short_link(short_link_code):
        link = is_long_link_in_db(short_link_code)
        if link:
            return f"<p id='link'> { link } </p>"
    return f""


