from sqlalchemy.orm import joinedload

from database import db
from models.task import Task
from models.user import User
from utils.helpers import VALID_ROLES, MIN_PASSWORD_LENGTH, validate_email


def list_users():
    users = db.session.query(User).options(joinedload(User.tasks)).all()
    return [user.to_dict(include_task_count=True) for user in users], 200


def get_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return {"error": "Usuário não encontrado"}, 404

    tasks = db.session.query(Task).filter_by(user_id=user_id).all()
    return user.to_dict(include_tasks=tasks), 200


def create_user(payload):
    if not payload:
        return {"error": "Dados inválidos"}, 400

    name = payload.get("name")
    email = payload.get("email")
    password = payload.get("password")
    role = payload.get("role", "user")

    if not name:
        return {"error": "Nome é obrigatório"}, 400
    if not email:
        return {"error": "Email é obrigatório"}, 400
    if not password:
        return {"error": "Senha é obrigatória"}, 400
    if not validate_email(email):
        return {"error": "Email inválido"}, 400
    if len(password) < MIN_PASSWORD_LENGTH:
        return {"error": f"Senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres"}, 400
    if role not in VALID_ROLES:
        return {"error": "Role inválido"}, 400

    existing = db.session.query(User).filter_by(email=email).first()
    if existing:
        return {"error": "Email já cadastrado"}, 409

    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), 201


def update_user(user_id, payload):
    user = db.session.get(User, user_id)
    if user is None:
        return {"error": "Usuário não encontrado"}, 404
    if not payload:
        return {"error": "Dados inválidos"}, 400

    if "name" in payload:
        user.name = payload["name"]

    if "email" in payload:
        if not validate_email(payload["email"]):
            return {"error": "Email inválido"}, 400
        existing = db.session.query(User).filter_by(email=payload["email"]).first()
        if existing and existing.id != user_id:
            return {"error": "Email já cadastrado"}, 409
        user.email = payload["email"]

    if "password" in payload:
        if len(payload["password"]) < MIN_PASSWORD_LENGTH:
            return {"error": "Senha muito curta"}, 400
        user.set_password(payload["password"])

    if "role" in payload:
        if payload["role"] not in VALID_ROLES:
            return {"error": "Role inválido"}, 400
        user.role = payload["role"]

    if "active" in payload:
        user.active = bool(payload["active"])

    db.session.commit()
    return user.to_dict(), 200


def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return {"error": "Usuário não encontrado"}, 404

    db.session.query(Task).filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    return {"message": "Usuário deletado com sucesso"}, 200


def get_user_tasks(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return {"error": "Usuário não encontrado"}, 404

    tasks = db.session.query(Task).filter_by(user_id=user_id).all()
    return [task.to_dict(include_overdue=True) for task in tasks], 200


def login(payload):
    if not payload:
        return {"error": "Dados inválidos"}, 400

    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        return {"error": "Email e senha são obrigatórios"}, 400

    user = db.session.query(User).filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return {"error": "Credenciais inválidas"}, 401
    if not user.active:
        return {"error": "Usuário inativo"}, 403

    return {
        "message": "Login realizado com sucesso",
        "user": user.to_dict(),
        "token": f"fake-jwt-token-{user.id}",
    }, 200
