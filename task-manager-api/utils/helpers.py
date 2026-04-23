from datetime import datetime
import re


VALID_STATUSES = ["pending", "in_progress", "done", "cancelled"]
VALID_ROLES = ["user", "admin", "manager"]
MAX_TITLE_LENGTH = 200
MAX_TAG_LENGTH = 500
MIN_TITLE_LENGTH = 3
MIN_PASSWORD_LENGTH = 4
DEFAULT_PRIORITY = 3
DEFAULT_COLOR = "#000000"


def format_date(date_obj):
    if date_obj:
        return str(date_obj)
    return None


def calculate_percentage(part, total):
    if total == 0:
        return 0
    return round((part / total) * 100, 2)


def validate_email(email):
    if re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", email):
        return True
    return False


def sanitize_string(value):
    if value:
        return value.strip()
    return value


def generate_id():
    import uuid

    return str(uuid.uuid4())


def log_action(action, details=None):
    timestamp = datetime.utcnow()
    print(f"[{timestamp}] ACTION: {action}")
    if details:
        print(f"  DETAILS: {details}")


def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_string, "%d/%m/%Y")
        except ValueError:
            return None


def is_valid_color(color):
    return bool(color and len(color) == 7 and color[0] == "#")


def process_task_data(data, existing_task=None):
    result = {}

    if "title" in data:
        title = sanitize_string(data["title"])
        if not title:
            return None, "Título não pode ser vazio"
        if len(title) < MIN_TITLE_LENGTH or len(title) > MAX_TITLE_LENGTH:
            return None, f"Título deve ter entre {MIN_TITLE_LENGTH} e {MAX_TITLE_LENGTH} caracteres"
        result["title"] = title

    if "description" in data:
        result["description"] = data["description"]

    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return None, "Status inválido"
        result["status"] = data["status"]
    elif existing_task is None:
        result["status"] = "pending"

    if "priority" in data:
        try:
            priority = int(data["priority"])
        except (TypeError, ValueError):
            return None, "Prioridade inválida"
        if priority < 1 or priority > 5:
            return None, "Prioridade deve ser entre 1 e 5"
        result["priority"] = priority
    elif existing_task is None:
        result["priority"] = DEFAULT_PRIORITY

    if "due_date" in data:
        if data["due_date"]:
            parsed = parse_date(data["due_date"])
            if not parsed:
                return None, "Data inválida"
            result["due_date"] = parsed
        else:
            result["due_date"] = None

    if "tags" in data:
        tags = data["tags"]
        if isinstance(tags, list):
            result["tags"] = ",".join(tags)
        else:
            result["tags"] = tags

    return result, None
