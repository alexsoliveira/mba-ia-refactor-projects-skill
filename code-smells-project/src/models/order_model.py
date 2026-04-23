from collections import defaultdict

from src.config.database import get_db
from src.utils.constants import DESCONTO_PROGRESSIVO


def create_order(usuario_id: int, items: list[dict]) -> dict:
    db = get_db()
    product_ids = [item["produto_id"] for item in items]
    placeholders = ",".join("?" for _ in product_ids)
    rows = db.execute(
        f"SELECT * FROM produtos WHERE id IN ({placeholders})",
        tuple(product_ids),
    ).fetchall()
    products_by_id = {row["id"]: row for row in rows}

    total = 0.0
    for item in items:
        product = products_by_id.get(item["produto_id"])
        if product is None:
            return {"erro": f'Produto {item["produto_id"]} não encontrado'}
        if product["estoque"] < item["quantidade"]:
            return {"erro": f'Estoque insuficiente para {product["nome"]}'}
        total += product["preco"] * item["quantidade"]

    cursor = db.execute(
        "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, ?, ?)",
        (usuario_id, "pendente", total),
    )
    order_id = cursor.lastrowid

    for item in items:
        product = products_by_id[item["produto_id"]]
        db.execute(
            """
            INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
            VALUES (?, ?, ?, ?)
            """,
            (order_id, item["produto_id"], item["quantidade"], product["preco"]),
        )
        db.execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            (item["quantidade"], item["produto_id"]),
        )

    db.commit()
    return {"pedido_id": order_id, "total": total}


def _serialize_orders(rows) -> list[dict]:
    order_ids = [row["id"] for row in rows]
    if not order_ids:
        return []

    placeholders = ",".join("?" for _ in order_ids)
    item_rows = get_db().execute(
        f"""
        SELECT ip.pedido_id, ip.produto_id, ip.quantidade, ip.preco_unitario, p.nome AS produto_nome
        FROM itens_pedido ip
        LEFT JOIN produtos p ON p.id = ip.produto_id
        WHERE ip.pedido_id IN ({placeholders})
        ORDER BY ip.pedido_id, ip.id
        """,
        tuple(order_ids),
    ).fetchall()

    items_by_order = defaultdict(list)
    for item in item_rows:
        items_by_order[item["pedido_id"]].append(
            {
                "produto_id": item["produto_id"],
                "produto_nome": item["produto_nome"] or "Desconhecido",
                "quantidade": item["quantidade"],
                "preco_unitario": item["preco_unitario"],
            }
        )

    return [
        {
            "id": row["id"],
            "usuario_id": row["usuario_id"],
            "status": row["status"],
            "total": row["total"],
            "criado_em": row["criado_em"],
            "itens": items_by_order[row["id"]],
        }
        for row in rows
    ]


def get_orders_by_user(usuario_id: int) -> list[dict]:
    rows = get_db().execute(
        "SELECT * FROM pedidos WHERE usuario_id = ? ORDER BY id",
        (usuario_id,),
    ).fetchall()
    return _serialize_orders(rows)


def get_all_orders() -> list[dict]:
    rows = get_db().execute("SELECT * FROM pedidos ORDER BY id").fetchall()
    return _serialize_orders(rows)


def get_sales_report() -> dict:
    db = get_db()
    total_orders = db.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
    gross_revenue = db.execute("SELECT COALESCE(SUM(total), 0) FROM pedidos").fetchone()[0]
    pending_orders = db.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", ("pendente",)).fetchone()[0]
    approved_orders = db.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", ("aprovado",)).fetchone()[0]
    canceled_orders = db.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", ("cancelado",)).fetchone()[0]

    discount = 0.0
    for minimum_total, percentage in DESCONTO_PROGRESSIVO:
        if gross_revenue > minimum_total:
            discount = gross_revenue * percentage
            break

    return {
        "total_pedidos": total_orders,
        "faturamento_bruto": round(gross_revenue, 2),
        "desconto_aplicavel": round(discount, 2),
        "faturamento_liquido": round(gross_revenue - discount, 2),
        "pedidos_pendentes": pending_orders,
        "pedidos_aprovados": approved_orders,
        "pedidos_cancelados": canceled_orders,
        "ticket_medio": round(gross_revenue / total_orders, 2) if total_orders > 0 else 0,
    }


def update_order_status(order_id: int, new_status: str) -> None:
    db = get_db()
    db.execute("UPDATE pedidos SET status = ? WHERE id = ?", (new_status, order_id))
    db.commit()

