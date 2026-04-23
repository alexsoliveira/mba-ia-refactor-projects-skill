from src.config.database import get_db


def _serialize_product(row) -> dict:
    return {
        "id": row["id"],
        "nome": row["nome"],
        "descricao": row["descricao"],
        "preco": row["preco"],
        "estoque": row["estoque"],
        "categoria": row["categoria"],
        "ativo": row["ativo"],
        "criado_em": row["criado_em"],
    }


def get_all_products() -> list[dict]:
    rows = get_db().execute("SELECT * FROM produtos").fetchall()
    return [_serialize_product(row) for row in rows]


def get_product_by_id(product_id: int) -> dict | None:
    row = get_db().execute("SELECT * FROM produtos WHERE id = ?", (product_id,)).fetchone()
    return _serialize_product(row) if row else None


def create_product(nome: str, descricao: str, preco: float, estoque: int, categoria: str) -> int:
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nome, descricao, preco, estoque, categoria),
    )
    db.commit()
    return cursor.lastrowid


def update_product(product_id: int, nome: str, descricao: str, preco: float, estoque: int, categoria: str) -> None:
    db = get_db()
    db.execute(
        """
        UPDATE produtos
        SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ?
        WHERE id = ?
        """,
        (nome, descricao, preco, estoque, categoria, product_id),
    )
    db.commit()


def delete_product(product_id: int) -> None:
    db = get_db()
    db.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
    db.commit()


def search_products(term: str, category: str | None = None, minimum_price: float | None = None, maximum_price: float | None = None) -> list[dict]:
    query = "SELECT * FROM produtos WHERE 1=1"
    params: list[object] = []

    if term:
        query += " AND (nome LIKE ? OR descricao LIKE ?)"
        like_value = f"%{term}%"
        params.extend([like_value, like_value])
    if category:
        query += " AND categoria = ?"
        params.append(category)
    if minimum_price is not None:
        query += " AND preco >= ?"
        params.append(minimum_price)
    if maximum_price is not None:
        query += " AND preco <= ?"
        params.append(maximum_price)

    rows = get_db().execute(query, tuple(params)).fetchall()
    return [_serialize_product(row) for row in rows]

