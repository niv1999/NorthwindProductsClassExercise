from flask import Blueprint, render_template

# Managing the entire view
home_blueprint = Blueprint("home_view", __name__) #"home_view" is the name of the view

@home_blueprint.route("/")
@home_blueprint.route("/home") # Route
def home(): # View function
    return render_template("home.html", active = "home")