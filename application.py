import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask,render_template,request

app=Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

books=db.execute("SELECT * FROM BOOKS")

@app.route("/")
def index():
    headline="Good Morning"
    return render_template("index.html", headline=headline)

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form.get("username")
        return render_template("login.html", name=name)
    else:
        return render_template("login.html")


@app.route("/searchpage", methods=["GET","POST"])
def searchpage():
    if request.method == "POST":
        name = request.form.get("name")
        return render_template("searchpage.html", name=name)
    else:
        return render_template("searchpage.html")


@app.route("/booksearch", methods=["POST"])
def booksearch():
    if request.method == "POST":
        isbn = request.form.get("isbn")
        bookauthorname = request.form.get("bookauthorname")
        searchname = "%%"+bookauthorname+"%%"
        if db.execute("SELECT * FROM BOOKS WHERE ISBN = :isbn",{"isbn":isbn}).rowcount==0:
            return render_template("errormsg.html", headline="Invalid ISBN.")
        else:
            books = db.execute("SELECT * FROM BOOKS WHERE ISBN = :isbn AND (TITLE LIKE :title OR AUTHOR LIKE :author)",{"isbn":isbn,"title":searchname,"author":searchname})
            return render_template("booksearch.html",books=books)
    else:
        return render_template("searchpage.html")

@app.route("/logout")
def logout():
    headline="Thanks for Visiting"
    return render_template("logout.html",headline=headline)
