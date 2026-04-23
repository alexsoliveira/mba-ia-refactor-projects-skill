from datetime import datetime

from database import db
from utils.helpers import DEFAULT_PRIORITY, MAX_TAG_LENGTH, VALID_STATUSES


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="pending")
    priority = db.Column(db.Integer, default=DEFAULT_PRIORITY)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    tags = db.Column(db.String(MAX_TAG_LENGTH), nullable=True)

    user = db.relationship("User", backref="tasks")
    category = db.relationship("Category", backref="tasks")

    @staticmethod
    def current_utc():
        return datetime.utcnow()

    def to_dict(self, include_related=False, include_overdue=False):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "due_date": str(self.due_date) if self.due_date else None,
            "tags": self.tags.split(",") if self.tags else [],
        }
        if include_related:
            data["user_name"] = self.user.name if self.user else None
            data["category_name"] = self.category.name if self.category else None
        if include_overdue:
            data["overdue"] = self.is_overdue()
        return data

    def validate_status(self, new_status):
        return new_status in VALID_STATUSES

    def validate_priority(self, priority):
        return 1 <= priority <= 5

    def apply_updates(self, values):
        for key, value in values.items():
            setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def is_overdue(self):
        return bool(
            self.due_date
            and self.due_date < datetime.utcnow()
            and self.status not in ["done", "cancelled"]
        )
