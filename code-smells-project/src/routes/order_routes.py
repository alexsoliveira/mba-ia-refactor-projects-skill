from flask import Blueprint, jsonify, request

from src.controllers.order_controller import (
    create_order_response,
    get_all_orders_response,
    get_sales_report_response,
    get_user_orders_response,
    update_order_status_response,
)

order_bp = Blueprint("orders", __name__)


@order_bp.post("/pedidos")
def create_order():
    body, status = create_order_response(request.get_json())
    return jsonify(body), status


@order_bp.get("/pedidos")
def get_all_orders():
    body, status = get_all_orders_response()
    return jsonify(body), status


@order_bp.get("/pedidos/usuario/<int:user_id>")
def get_user_orders(user_id: int):
    body, status = get_user_orders_response(user_id)
    return jsonify(body), status


@order_bp.put("/pedidos/<int:order_id>/status")
def update_order_status(order_id: int):
    body, status = update_order_status_response(order_id, request.get_json())
    return jsonify(body), status


@order_bp.get("/relatorios/vendas")
def get_sales_report():
    body, status = get_sales_report_response()
    return jsonify(body), status

