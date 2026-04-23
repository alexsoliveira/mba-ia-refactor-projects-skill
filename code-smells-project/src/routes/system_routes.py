from hmac import compare_digest

from flask import Blueprint, current_app, jsonify, request

from src.controllers.system_controller import (
    execute_admin_query_response,
    get_health_response,
    reset_database_response,
)

system_bp = Blueprint("system", __name__)


def _admin_enabled() -> bool:
    return bool(current_app.config.get("ADMIN_TOKEN"))


def _is_authorized() -> bool:
    token = current_app.config.get("ADMIN_TOKEN")
    provided = request.headers.get("X-Admin-Token", "")
    return bool(token) and compare_digest(token, provided)


@system_bp.get("/health")
def health_check():
    body, status = get_health_response()
    return jsonify(body), status


@system_bp.post("/admin/reset-db")
def reset_database():
    if not _admin_enabled() or not _is_authorized():
        return jsonify({"erro": "Acesso administrativo não autorizado", "sucesso": False}), 403

    body, status = reset_database_response()
    return jsonify(body), status


@system_bp.post("/admin/query")
def execute_admin_query():
    if not _admin_enabled() or not _is_authorized():
        return jsonify({"erro": "Acesso administrativo não autorizado", "sucesso": False}), 403

    body, status = execute_admin_query_response((request.get_json() or {}).get("sql", ""))
    return jsonify(body), status
