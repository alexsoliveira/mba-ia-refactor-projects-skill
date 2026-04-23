from flask import Flask, jsonify
from flask_cors import CORS

from src.config.database import init_app as init_database
from src.config.settings import get_settings
from src.middlewares.error_handler import register_error_handlers
from src.routes.order_routes import order_bp
from src.routes.product_routes import product_bp
from src.routes.system_routes import system_bp
from src.routes.user_routes import user_bp


def create_app() -> Flask:
    settings = get_settings()
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=settings.secret_key,
        DEBUG=settings.debug,
        DATABASE_PATH=settings.database_path,
        ADMIN_TOKEN=settings.admin_token,
        APP_ENV=settings.environment,
        APP_VERSION=settings.version,
    )

    CORS(app)
    init_database(app)
    register_error_handlers(app)

    app.register_blueprint(product_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(system_bp)

    @app.get("/")
    def index():
        return jsonify(
            {
                "mensagem": "Bem-vindo à API da Loja",
                "versao": app.config["APP_VERSION"],
                "endpoints": {
                    "produtos": "/produtos",
                    "usuarios": "/usuarios",
                    "pedidos": "/pedidos",
                    "login": "/login",
                    "relatorios": "/relatorios/vendas",
                    "health": "/health",
                },
            }
        )

    return app

