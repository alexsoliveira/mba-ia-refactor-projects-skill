from datetime import datetime

from database import db


class Category(db.Model):
    __tablename__ = "categories"
    DEFAULT_COLOR = "#000000"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    color = db.Column(db.String(7), default=DEFAULT_COLOR)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, include_task_count=False):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "created_at": str(self.created_at),
        }
        if include_task_count:
            data["task_count"] = len(self.tasks)
        return data
