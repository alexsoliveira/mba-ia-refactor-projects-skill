from flask import current_app

from src.config.database import get_db
from src.models.product_model import get_all_products
from src.models.user_model import get_all_users
from src.models.order_model import get_all_orders

ALLOWED_ADMIN_QUERIES = {
    "SELECT 1": lambda db: db.execute("SELECT 1").fetchall(),
    "SELECT COUNT(*) FROM produtos": lambda db: db.execute("SELECT COUNT(*) FROM produtos").fetchall(),
    "SELECT COUNT(*) FROM usuarios": lambda db: db.execute("SELECT COUNT(*) FROM usuarios").fetchall(),
    "SELECT COUNT(*) FROM pedidos": lambda db: db.execute("SELECT COUNT(*) FROM pedidos").fetchall(),
    "SELECT COUNT(*) FROM itens_pedido": lambda db: db.execute("SELECT COUNT(*) FROM itens_pedido").fetchall(),
}


def get_health_response() -> tuple[dict, int]:
    db = get_db()
    db.execute("SELECT 1")
    return {
        "status": "ok",
        "database": "connected",
        "counts": {
            "produtos": len(get_all_products()),
            "usuarios": len(get_all_users()),
            "pedidos": len(get_all_orders()),
        },
        "versao": current_app.config["APP_VERSION"],
        "ambiente": current_app.config["APP_ENV"],
        "debug": current_app.config["DEBUG"],
    }, 200


def reset_database_response() -> tuple[dict, int]:
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM produtos")
    cursor.execute("DELETE FROM usuarios")
    db.commit()
    return {"mensagem": "Banco de dados resetado", "sucesso": True}, 200


def execute_admin_query_response(query: str) -> tuple[dict, int]:
    normalized_query = query.strip()
    if not normalized_query:
        return {"erro": "Query não informada", "sucesso": False}, 400

    executor = ALLOWED_ADMIN_QUERIES.get(normalized_query)
    if executor is None:
        return {"erro": "Query administrativa não permitida", "sucesso": False}, 403

    rows = executor(get_db())
    return {"dados": [dict(row) for row in rows], "sucesso": True}, 200
