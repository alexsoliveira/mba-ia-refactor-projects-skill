from datetime import datetime

from flask import Flask, jsonify
from flask_cors import CORS

from config.settings import Settings
from database import db
from routes.report_routes import report_bp
from routes.task_routes import task_bp
from routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)

    CORS(app)
    db.init_app(app)

    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)

    @app.route("/health")
    def health():
        return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

    @app.route("/")
    def index():
        return {"message": "Task Manager API", "version": "1.0"}

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unhandled application error: %s", error)
        return jsonify({"error": "Erro interno"}), 500

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=Settings.DEBUG, host=Settings.HOST, port=Settings.PORT)
