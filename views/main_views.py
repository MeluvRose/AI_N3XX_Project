from flask import Blueprint, render_template, redirect, url_for
from flask.globals import request

main_bp = Blueprint('main', __name__)

# @main_bp.route('/', methods=["POST", "GET"])
# def index():
#     return render_template("index.html")

# @main_bp.route('/', defaults={ "name":"손님" })
# @main_bp.route("/<name>")
# def user(name):
#     # return render_template("index.html", content=name, r=4);
#     return render_template("menu.html", content=name);

# @main_bp.route("/admin")
# def admin():
#     # return redirect(url_for("main.index"))
#     return redirect(url_for("main.user", name='Admin?!'));

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("main.user", usr=user))
    else :
        return render_template("login_test.html")

@main_bp.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True);
