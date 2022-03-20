from webbrowser import get
from flask import Flask, request, render_template, session
from flask import redirect, make_response, jsonify
from functools import wraps
import os

from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, verify_jwt_in_request
from flask_jwt_extended import JWTManager, get_jwt_identity, get_jwt
from flask_jwt_extended import set_access_cookies


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secretkey"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
jwt = JWTManager(app)
jwt.init_app(app)
app = Flask(__name__)
app.secret_key = "secretkey"
app.config["UPLOADED_PHOTOS_DEST"] = "static"
app.config["JWT_SECRET_KEY"] = "secretkey"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)
jwt.init_app(app)

books = [
    {
        "id": 1,
        "author": "Douglas Preston & Licoln Child",
        "country": "USA",
        "language": "English",
        "title": "Riptide",
        "year": 2005,
    },
    {
        "id": 2,
        "author": "Timothy Zahn",
        "country": "USA",
        "language": "English",
        "title": "Heir to the Empire",
        "year": 1992,
    },
    {
        "id": 3,
        "author": "Bill Hybels",
        "country": "USA",
        "language": "English",
        "title": "Simplify: Ten Practices to Unclutter Your Soul",
        "year": 2015,
    },
    {
        "id": 4,
        "author": "Michael Crichton",
        "country": "USA",
        "language": "English",
        "title": "Jurassic Park",
        "year": 1990,
    },
    {
        "id": 5,
        "author": "David Barton & Tim Barton",
        "country": "USA",
        "language": "English",
        "title": "The American Story: The Beginnings",
        "year": 2020,
    },
]

users = [
    {"username": "Adam", "password": "Adam", "role": "admin"},
    {"username": "Luke", "password": "Luke", "role": "reader"},
    {"username": "Obi-Wan", "password": "Obi-Wan", "role": "admin"},
    {"username": "Han", "password": "Han", "role": "reader"},
    {"username": "Leia", "password": "Leia", "role": "reader"},
    {"username": "testuser", "password": "testuser", "role": "admin"}
   ]


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] != 'admin':
            return jsonify(msg='Admins Only!'), 403
        else:
            return fn(*args, **kwargs)
    
    return wrapper


    


def checkUser(username, password):
    for user in users:
        if username in user["username"] and password in user["password"]:
            return {"username": user["username"], "role": user["role"]}
    return None


@app.route("/", methods=["GET"])
def firstRoute():
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        validUser = checkUser(username, password)
        if validUser != None:
            # set JWT token

            user_claims = {"role": validUser["role"]}
            access_token = create_access_token(
                username, additional_claims=user_claims)

            response = make_response(
                render_template(
                    "index.html", title="books", username=username, books=books
                )
            )
            response.status_code = 200
            # add jwt-token to response headers
            response.headers.extend({"jwt-token": access_token})
            set_access_cookies(response, access_token)
            return response

    return render_template("register.html")


@app.route("/logout")
def logout():
    # invalidate the JWT token

    return "Logged Out of Books"


@app.route("/books", methods=["GET"])
@jwt_required()
def getBooks():
    try:
        username = get_jwt_identity()
        return render_template('books.html', username=username, books=books)
    except:
        return render_template("register.html")


@app.route("/addbook", methods=["GET", "POST"])
@jwt_required()
@admin_required
def addBook():
    username = get_jwt_identity()
    if request.method == "GET":
        return render_template("addBook.html", username=username)
    if request.method == "POST":
        # expects pure json with quotes everywheree
        author = request.form.get("author")
        title = request.form.get("title")
        year = request.form.get("year")
        language = request.form.get("language")
        country = request.form.get("country")
        id = int(books[-1]['id'])
        newbook = {"id":id+1,"author": author, "title": title, "country":country, "year":year, "language":language}
        books.append(newbook)
        return render_template(
            "books.html", books=books, username=username, title="books"
        )
    else:
        return 400


@app.route("/addimage", methods=["GET", "POST"])
@jwt_required()
@admin_required
def addimage():
    if request.method == "GET":
        return render_template("addimage.html")
    elif request.method == "POST":
        image = request.files["image"]
        id = request.form.get("number")  # use id to number the image
        imagename = "image" + id + ".png"
        image.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], imagename))
        print(image.filename)
        return "image loaded"

    return "all done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
