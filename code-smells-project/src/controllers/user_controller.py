from src.models.user_model import create_user, get_all_users, get_user_by_id, login_user
from src.utils.validators import validate_login_payload, validate_user_payload


def list_users_response() -> tuple[dict, int]:
    return {"dados": get_all_users(), "sucesso": True}, 200


def get_user_response(user_id: int) -> tuple[dict, int]:
    user = get_user_by_id(user_id)
    if user:
        return {"dados": user, "sucesso": True}, 200
    return {"erro": "Usuário não encontrado"}, 404


def create_user_response(data: dict | None) -> tuple[dict, int]:
    payload = validate_user_payload(data)
    user_id = create_user(payload["nome"], payload["email"], payload["senha"])
    return {"dados": {"id": user_id}, "sucesso": True}, 201


def login_response(data: dict | None) -> tuple[dict, int]:
    payload = validate_login_payload(data)
    user = login_user(payload["email"], payload["senha"])
    if user:
        return {"dados": user, "sucesso": True, "mensagem": "Login OK"}, 200
    return {"erro": "Email ou senha inválidos", "sucesso": False}, 401

