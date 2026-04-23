from werkzeug.security import check_password_hash

from src.config.database import get_db


def _serialize_user(row, include_password: bool = True) -> dict:
    data = {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"],
    }
    if include_password:
        data["senha"] = row["senha"]
    return data


def get_all_users() -> list[dict]:
    rows = get_db().execute("SELECT * FROM usuarios").fetchall()
    return [_serialize_user(row) for row in rows]


def get_user_by_id(user_id: int) -> dict | None:
    row = get_db().execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    return _serialize_user(row) if row else None


def create_user(nome: str, email: str, senha: str, tipo: str = "cliente") -> int:
    db = get_db()
    cursor = db.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, senha, tipo),
    )
    db.commit()
    return cursor.lastrowid


def login_user(email: str, senha: str) -> dict | None:
    row = get_db().execute(
        "SELECT * FROM usuarios WHERE email = ?",
        (email,),
    ).fetchone()
    if row is None:
        return None

    stored_password = row["senha"]
    if stored_password == senha:
        return _serialize_user(row, include_password=False)
    if stored_password.startswith("scrypt:") and check_password_hash(stored_password, senha):
        return _serialize_user(row, include_password=False)
    return None
