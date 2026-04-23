from flask import Blueprint, jsonify, request

from src.controllers.product_controller import (
    create_product_response,
    delete_product_response,
    get_product_response,
    list_products_response,
    search_products_response,
    update_product_response,
)

product_bp = Blueprint("products", __name__)


@product_bp.get("/produtos")
def list_products():
    body, status = list_products_response()
    return jsonify(body), status


@product_bp.get("/produtos/busca")
def search_products():
    minimum_price = request.args.get("preco_min")
    maximum_price = request.args.get("preco_max")
    body, status = search_products_response(
        request.args.get("q", ""),
        request.args.get("categoria"),
        float(minimum_price) if minimum_price else None,
        float(maximum_price) if maximum_price else None,
    )
    return jsonify(body), status


@product_bp.get("/produtos/<int:product_id>")
def get_product(product_id: int):
    body, status = get_product_response(product_id)
    return jsonify(body), status


@product_bp.post("/produtos")
def create_product():
    body, status = create_product_response(request.get_json())
    return jsonify(body), status


@product_bp.put("/produtos/<int:product_id>")
def update_product(product_id: int):
    body, status = update_product_response(product_id, request.get_json())
    return jsonify(body), status


@product_bp.delete("/produtos/<int:product_id>")
def delete_product(product_id: int):
    body, status = delete_product_response(product_id)
    return jsonify(body), status

