from flask import blueprints
hm = blueprints.Blueprint("home", __name__)

@hm.route("/index")
def index():
    return "index"

