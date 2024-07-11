from flask import Blueprint, jsonify, make_response
from facades.products_facade import ProductsFacade
from models.client_errors import ResourceNotFoundError
from models.status_code import StatusCode

api_blueprint = Blueprint("api_view", __name__)

products_facade = ProductsFacade()

@api_blueprint.route("/api/products")
def products():
    try:
        products = products_facade.get_all_products()
        return jsonify(products)
    except Exception as err:
        json =  jsonify({"error": err.message})
        return make_response(json, StatusCode.InternalServerError.value)

@api_blueprint.route("/api/products/<int:id>")
def one_product(id):
    try:
        product = products_facade.get_one_product(id)
        return jsonify(product)
    except ResourceNotFoundError as err:
        json = jsonify({"error" : err.message})
        return make_response(json, StatusCode.NotFound.value)