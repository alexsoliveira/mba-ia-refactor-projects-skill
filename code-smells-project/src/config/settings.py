import os
import secrets
from dataclasses import dataclass
from pathlib import Path


TRUE_VALUES = {"1", "true", "yes", "on"}


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in TRUE_VALUES


@dataclass(frozen=True)
class Settings:
    secret_key: str
    debug: bool
    database_path: str
    host: str
    port: int
    environment: str
    admin_token: str | None
    version: str = "1.0.0"


def get_settings() -> Settings:
    _load_dotenv()
    base_dir = Path(__file__).resolve().parents[2]
    database_path = os.getenv("DATABASE_PATH", str(base_dir / "loja.db"))

    return Settings(
        secret_key=os.getenv("SECRET_KEY", secrets.token_hex(32)),
        debug=_to_bool(os.getenv("DEBUG"), default=False),
        database_path=str(Path(database_path)),
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")),
        environment=os.getenv("FLASK_ENV", "production"),
        admin_token=os.getenv("ADMIN_TOKEN"),
    )

