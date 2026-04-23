from flask import Blueprint, jsonify, request

from src.controllers.user_controller import (
    create_user_response,
    get_user_response,
    list_users_response,
    login_response,
)

user_bp = Blueprint("users", __name__)


@user_bp.get("/usuarios")
def list_users():
    body, status = list_users_response()
    return jsonify(body), status


@user_bp.get("/usuarios/<int:user_id>")
def get_user(user_id: int):
    body, status = get_user_response(user_id)
    return jsonify(body), status


@user_bp.post("/usuarios")
def create_user():
    body, status = create_user_response(request.get_json())
    return jsonify(body), status


@user_bp.post("/login")
def login():
    body, status = login_response(request.get_json())
    return jsonify(body), status

