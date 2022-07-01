from flask import blueprints, session, current_app
from flaskScript import db, models

ac = blueprints.Blueprint("ac", __name__)


@ac.route("/login/", methods=["GET", "POST"])
def login():
    current_app.auto.login("李华")
    return "Login"
