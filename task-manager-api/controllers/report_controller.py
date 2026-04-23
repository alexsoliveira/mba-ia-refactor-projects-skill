from datetime import datetime, timedelta

from sqlalchemy.orm import joinedload

from database import db
from models.category import Category
from models.task import Task
from models.user import User


def summary_report():
    total_tasks = db.session.query(Task).count()
    total_users = db.session.query(User).count()
    total_categories = db.session.query(Category).count()

    pending = db.session.query(Task).filter_by(status="pending").count()
    in_progress = db.session.query(Task).filter_by(status="in_progress").count()
    done = db.session.query(Task).filter_by(status="done").count()
    cancelled = db.session.query(Task).filter_by(status="cancelled").count()

    priorities = {
        "critical": db.session.query(Task).filter_by(priority=1).count(),
        "high": db.session.query(Task).filter_by(priority=2).count(),
        "medium": db.session.query(Task).filter_by(priority=3).count(),
        "low": db.session.query(Task).filter_by(priority=4).count(),
        "minimal": db.session.query(Task).filter_by(priority=5).count(),
    }

    all_tasks = db.session.query(Task).all()
    overdue_list = []
    for task in all_tasks:
        if task.is_overdue():
            overdue_list.append(
                {
                    "id": task.id,
                    "title": task.title,
                    "due_date": str(task.due_date),
                    "days_overdue": (datetime.utcnow() - task.due_date).days,
                }
            )

    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_tasks = db.session.query(Task).filter(Task.created_at >= seven_days_ago).count()
    recent_done = (
        db.session.query(Task)
        .filter(Task.status == "done", Task.updated_at >= seven_days_ago)
        .count()
    )

    users = db.session.query(User).options(joinedload(User.tasks)).all()
    user_stats = []
    for user in users:
        total = len(user.tasks)
        completed = sum(1 for task in user.tasks if task.status == "done")
        user_stats.append(
            {
                "user_id": user.id,
                "user_name": user.name,
                "total_tasks": total,
                "completed_tasks": completed,
                "completion_rate": round((completed / total) * 100, 2) if total > 0 else 0,
            }
        )

    return {
        "generated_at": str(datetime.utcnow()),
        "overview": {
            "total_tasks": total_tasks,
            "total_users": total_users,
            "total_categories": total_categories,
        },
        "tasks_by_status": {
            "pending": pending,
            "in_progress": in_progress,
            "done": done,
            "cancelled": cancelled,
        },
        "tasks_by_priority": priorities,
        "overdue": {
            "count": len(overdue_list),
            "tasks": overdue_list,
        },
        "recent_activity": {
            "tasks_created_last_7_days": recent_tasks,
            "tasks_completed_last_7_days": recent_done,
        },
        "user_productivity": user_stats,
    }, 200


def user_report(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return {"error": "Usuário não encontrado"}, 404

    tasks = db.session.query(Task).filter_by(user_id=user_id).all()
    total = len(tasks)
    done = sum(1 for task in tasks if task.status == "done")
    pending = sum(1 for task in tasks if task.status == "pending")
    in_progress = sum(1 for task in tasks if task.status == "in_progress")
    cancelled = sum(1 for task in tasks if task.status == "cancelled")
    overdue = sum(1 for task in tasks if task.is_overdue())
    high_priority = sum(1 for task in tasks if task.priority <= 2)

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
        "statistics": {
            "total_tasks": total,
            "done": done,
            "pending": pending,
            "in_progress": in_progress,
            "cancelled": cancelled,
            "overdue": overdue,
            "high_priority": high_priority,
            "completion_rate": round((done / total) * 100, 2) if total > 0 else 0,
        },
    }, 200


def list_categories():
    categories = db.session.query(Category).options(joinedload(Category.tasks)).all()
    return [category.to_dict(include_task_count=True) for category in categories], 200


def create_category(payload):
    if not payload:
        return {"error": "Dados inválidos"}, 400

    name = payload.get("name")
    if not name:
        return {"error": "Nome é obrigatório"}, 400

    category = Category(
        name=name,
        description=payload.get("description", ""),
        color=payload.get("color") or Category.DEFAULT_COLOR,
    )
    db.session.add(category)
    db.session.commit()
    return category.to_dict(), 201


def update_category(cat_id, payload):
    category = db.session.get(Category, cat_id)
    if category is None:
        return {"error": "Categoria não encontrada"}, 404
    if not payload:
        return {"error": "Dados inválidos"}, 400

    if "name" in payload:
        category.name = payload["name"]
    if "description" in payload:
        category.description = payload["description"]
    if "color" in payload:
        category.color = payload["color"]

    db.session.commit()
    return category.to_dict(), 200


def delete_category(cat_id):
    category = db.session.get(Category, cat_id)
    if category is None:
        return {"error": "Categoria não encontrada"}, 404

    db.session.delete(category)
    db.session.commit()
    return {"message": "Categoria deletada"}, 200
