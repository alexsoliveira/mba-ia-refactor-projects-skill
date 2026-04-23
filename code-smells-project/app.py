from src.app import create_app
from src.config.settings import get_settings

app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print(f"Rodando em http://localhost:{settings.port}")
    print("=" * 50)
    app.run(host=settings.host, port=settings.port, debug=settings.debug)
