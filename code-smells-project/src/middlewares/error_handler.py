from flask import Flask, jsonify

from src.utils.validators import ValidationError


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({"erro": str(error), "sucesso": False}), 400

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        return jsonify({"erro": str(error), "sucesso": False}), 500

