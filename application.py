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

@app.route("/registration",methods=["GET","POST"])
def registration():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"username {username}")
        print(f"password {password}")
        if db.execute("SELECT * FROM USERS WHERE NAME = :name",{"name":name}).rowcount==0:
            db.execute("INSERT INTO USERS (NAME, USERNAME, PASSWORD) VALUES (:name, :username, :password)",{"name": name, "username": username, "password":password})
            db.commit()
            return render_template("login.html", name=name)
        else:
            return render_template("errormsg.html", headline="User already exists.Please login from home page")

    else:
        return render_template("registration.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if db.execute("SELECT * FROM USERS WHERE USERNAME = :username AND PASSWORD = :password",{"username":username, "password":password}).rowcount==0:
            return render_template("errormsg.html", headline="Invalid username or password.")
        else:
            names = db.execute("SELECT NAME FROM USERS WHERE USERNAME = :username AND PASSWORD = :password",{"username":username, "password":password})
            return render_template("searchpage.html",names=names)
    else:
        return render_template("login.html")


@app.route("/searchpage", methods=["GET","POST"])
def searchpage():
    if request.method == "POST":
        name = request.form.get("name")
        #return render_template("searchpage.html", name=name)
        isbn = request.form.get("isbn")
        bookauthorname = request.form.get("bookauthorname")
        isbn1 = "%%"+isbn+"%%"
        searchname = "%%"+bookauthorname+"%%"
        if db.execute("SELECT * FROM BOOKS WHERE ISBN like :isbn",{"isbn":isbn1}).rowcount==0:
            return render_template("errormsg.html", headline="Invalid ISBN.")
        else:
            books = db.execute("SELECT * FROM BOOKS WHERE ISBN like :isbn AND (TITLE LIKE :title OR AUTHOR LIKE :author)",{"isbn":isbn1,"title":searchname,"author":searchname})
            return render_template("searchpage.html",books=books)
    else:
        return render_template("searchpage.html")


@app.route("/booksearch/<isbn>",methods=["GET","POST"])
def booksearch(isbn):
    #if request.method == "GET":
    #    isbn = request.form.get("isbn")
        print(f"isbn {isbn}")
        books = db.execute("SELECT * FROM BOOKS WHERE ISBN =:isbn",{"isbn":isbn})
        return render_template("booksearch.html",books=books)
    #else:
    #    return render_template("searchpage.html")

#@app.route("/booksearch/<string:isbn>", methods=["POST"])
#def booksearch1(isbn):
    #id = db.execute("SELECT id FROM BOOKS WHERE ISBN = :isbn",{"isbn":isbn})
    #isbn = request.form.get("isbn")
    #print(f"isbn: {isbn}")
    #return render_template("booksearch.html",books=books)

@app.route("/reviewsubmit", methods=["POST"])
def reviewsubmit():
    headline="Thanks for submitting review"
    return render_template("logout.html",headline=headline)

@app.route("/logout")
def logout():
    headline="Thanks for Visiting"
    return render_template("logout.html",headline=headline)
