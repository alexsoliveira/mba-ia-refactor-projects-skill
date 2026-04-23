from flask import jsonify, request

from src.controllers.order_controller import (
    create_order_response,
    get_all_orders_response,
    get_sales_report_response,
    get_user_orders_response,
    update_order_status_response,
)
from src.controllers.product_controller import (
    create_product_response,
    delete_product_response,
    get_product_response,
    list_products_response,
    search_products_response,
    update_product_response,
)
from src.controllers.system_controller import execute_admin_query_response, get_health_response, reset_database_response
from src.controllers.user_controller import (
    create_user_response,
    get_user_response,
    list_users_response,
    login_response,
)

def listar_produtos():
    body, status = list_products_response()
    return jsonify(body), status


def buscar_produto(id):
    body, status = get_product_response(id)
    return jsonify(body), status


def criar_produto():
    body, status = create_product_response(request.get_json())
    return jsonify(body), status


def atualizar_produto(id):
    body, status = update_product_response(id, request.get_json())
    return jsonify(body), status


def deletar_produto(id):
    body, status = delete_product_response(id)
    return jsonify(body), status


def buscar_produtos():
    minimum_price = request.args.get("preco_min")
    maximum_price = request.args.get("preco_max")
    body, status = search_products_response(
        request.args.get("q", ""),
        request.args.get("categoria"),
        float(minimum_price) if minimum_price else None,
        float(maximum_price) if maximum_price else None,
    )
    return jsonify(body), status


def listar_usuarios():
    body, status = list_users_response()
    return jsonify(body), status


def buscar_usuario(id):
    body, status = get_user_response(id)
    return jsonify(body), status


def criar_usuario():
    body, status = create_user_response(request.get_json())
    return jsonify(body), status


def login():
    body, status = login_response(request.get_json())
    return jsonify(body), status


def criar_pedido():
    body, status = create_order_response(request.get_json())
    return jsonify(body), status


def listar_pedidos_usuario(usuario_id):
    body, status = get_user_orders_response(usuario_id)
    return jsonify(body), status


def listar_todos_pedidos():
    body, status = get_all_orders_response()
    return jsonify(body), status


def atualizar_status_pedido(pedido_id):
    body, status = update_order_status_response(pedido_id, request.get_json())
    return jsonify(body), status


def relatorio_vendas():
    body, status = get_sales_report_response()
    return jsonify(body), status


def health_check():
    body, status = get_health_response()
    return jsonify(body), status


def reset_database():
    body, status = reset_database_response()
    return jsonify(body), status


def executar_query():
    body, status = execute_admin_query_response((request.get_json() or {}).get("sql", ""))
    return jsonify(body), status

__all__ = [
    "atualizar_produto",
    "atualizar_status_pedido",
    "buscar_produto",
    "buscar_produtos",
    "create_order_response",
    "create_product_response",
    "create_user_response",
    "criar_pedido",
    "criar_produto",
    "criar_usuario",
    "delete_product_response",
    "deletar_produto",
    "executar_query",
    "get_all_orders_response",
    "get_health_response",
    "get_product_response",
    "get_sales_report_response",
    "get_user_orders_response",
    "get_user_response",
    "health_check",
    "listar_pedidos_usuario",
    "listar_produtos",
    "listar_todos_pedidos",
    "listar_usuarios",
    "list_products_response",
    "list_users_response",
    "login_response",
    "login",
    "relatorio_vendas",
    "reset_database",
    "search_products_response",
    "buscar_usuario",
    "update_product_response",
    "update_order_status_response",
    "atualizar_status_pedido",
]
