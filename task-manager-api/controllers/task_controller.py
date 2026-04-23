from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from database import db
from models.category import Category
from models.task import Task
from models.user import User
from utils.helpers import process_task_data


def list_tasks():
    tasks = (
        db.session.query(Task)
        .options(joinedload(Task.user), joinedload(Task.category))
        .all()
    )
    return [task.to_dict(include_related=True, include_overdue=True) for task in tasks], 200


def get_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return {"error": "Task não encontrada"}, 404
    return task.to_dict(include_overdue=True), 200


def create_task(payload):
    if not payload:
        return {"error": "Dados inválidos"}, 400

    if not payload.get("title"):
        return {"error": "Título é obrigatório"}, 400

    parsed_data, error = process_task_data(payload)
    if error:
        return {"error": error}, 400

    user_id = payload.get("user_id")
    category_id = payload.get("category_id")
    user = db.session.get(User, user_id) if user_id else None
    category = db.session.get(Category, category_id) if category_id else None

    if user_id and user is None:
        return {"error": "Usuário não encontrado"}, 404

    if category_id and category is None:
        return {"error": "Categoria não encontrada"}, 404

    task = Task()
    task.apply_updates(parsed_data)
    task.user_id = user_id
    task.category_id = category_id

    db.session.add(task)
    db.session.commit()
    return task.to_dict(include_overdue=True), 201


def update_task(task_id, payload):
    task = db.session.get(Task, task_id)
    if task is None:
        return {"error": "Task não encontrada"}, 404

    if not payload:
        return {"error": "Dados inválidos"}, 400

    parsed_data, error = process_task_data(payload, existing_task=task)
    if error:
        return {"error": error}, 400

    if "user_id" in payload:
        user_id = payload["user_id"]
        if user_id and db.session.get(User, user_id) is None:
            return {"error": "Usuário não encontrado"}, 404
        task.user_id = user_id

    if "category_id" in payload:
        category_id = payload["category_id"]
        if category_id and db.session.get(Category, category_id) is None:
            return {"error": "Categoria não encontrada"}, 404
        task.category_id = category_id

    task.apply_updates(parsed_data)
    db.session.commit()
    return task.to_dict(include_overdue=True), 200


def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return {"error": "Task não encontrada"}, 404

    db.session.delete(task)
    db.session.commit()
    return {"message": "Task deletada com sucesso"}, 200


def search_tasks(args):
    query = args.get("q", "")
    status = args.get("status", "")
    priority = args.get("priority", "")
    user_id = args.get("user_id", "")

    tasks = db.session.query(Task)

    if query:
        tasks = tasks.filter(
            or_(
                Task.title.like(f"%{query}%"),
                Task.description.like(f"%{query}%"),
            )
        )

    if status:
        tasks = tasks.filter(Task.status == status)

    if priority:
        tasks = tasks.filter(Task.priority == int(priority))

    if user_id:
        tasks = tasks.filter(Task.user_id == int(user_id))

    results = tasks.all()
    return [task.to_dict(include_overdue=True) for task in results], 200


def task_stats():
    total = db.session.query(Task).count()
    pending = db.session.query(Task).filter_by(status="pending").count()
    in_progress = db.session.query(Task).filter_by(status="in_progress").count()
    done = db.session.query(Task).filter_by(status="done").count()
    cancelled = db.session.query(Task).filter_by(status="cancelled").count()

    overdue_count = (
        db.session.query(Task)
        .filter(Task.due_date.is_not(None))
        .filter(Task.due_date < Task.current_utc())
        .filter(Task.status.notin_(["done", "cancelled"]))
        .count()
    )

    stats = {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "done": done,
        "cancelled": cancelled,
        "overdue": overdue_count,
        "completion_rate": round((done / total) * 100, 2) if total > 0 else 0,
    }
    return stats, 200
