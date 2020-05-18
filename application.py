from flask import Flask,render_template,request

app=Flask(__name__)

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


@app.route("/searchpage", methods=["POST"])
def searchpage():
    name = request.form.get("name")
    return render_template("searchpage.html", name=name)


@app.route("/logout")
def logout():
    headline="Thanks for Visiting"
    return render_template("logout.html",headline=headline)
