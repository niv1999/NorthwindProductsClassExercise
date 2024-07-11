from flask import Blueprint, render_template, send_file, redirect, url_for, request
from facades.products_facade import ProductsFacade
from facades.auth_facade import AuthFacade
from utils.image_handler import ImageHandler
from models.client_errors import ResourceNotFoundError, ValidationError, AuthError

# Managing the entire view
products_blueprint = Blueprint("products_view", __name__) 

products_facade = ProductsFacade()
auth_facade = AuthFacade()

# Display all products:
@products_blueprint.route("/products")
def list():
    all_products = products_facade.get_all_products()
    return render_template("products.html", products = all_products, active = "list")

# Display a single product:
@products_blueprint.route("/products/details/<int:id>") # <int:id> is called a route parameter
def details(id):
    try:
        one_product = products_facade.get_one_product(id)
        return render_template("details.html", product = one_product)
    except ResourceNotFoundError as err:
        return render_template("404.html", error = err.message)

# Return image file:
@products_blueprint.route("/products/images/<string:image_name>")
def get_image(image_name):
    image_path = ImageHandler.get_image_path(image_name)
    return send_file(image_path) # Returns a complete file (an image file with pixels of the image...)

# Adding new product:
@products_blueprint.route("/products/new", methods=["GET", "POST"])
def insert():
    try:
        auth_facade.block_anonymous()
        if request.method == "GET": return render_template("insert.html", active = "insert")
        products_facade.add_product()
        return redirect(url_for("products_view.list"))
    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message))
    except ValidationError as err:
        return render_template("insert.html", error = err.message)

# Updating existing product:
@products_blueprint.route("/products/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    try:
        auth_facade.block_anonymous()
        if request.method == "GET":
            product = products_facade.get_one_product(id)
            return render_template("edit.html", product = product)
        products_facade.update_product()
        return redirect(url_for("products_view.list"))
    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message))
    except ValidationError as err:
        return render_template("edit.html", error = err.message, product = err.model)

@products_blueprint.route("/products/delete/<int:id>")
def delete(id):
    try:
        auth_facade.block_anonymous()
        auth_facade.block_non_admin()
        products_facade.delete_product(id)
        return redirect(url_for("products_view.list"))
    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message))