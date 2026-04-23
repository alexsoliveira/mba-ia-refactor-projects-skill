from datetime import datetime
import hashlib

from werkzeug.security import check_password_hash, generate_password_hash

from database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="user")
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, include_sensitive=False, include_task_count=False, include_tasks=None):
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "active": self.active,
            "created_at": str(self.created_at),
        }
        if include_sensitive:
            data["password"] = self.password
        if include_task_count:
            data["task_count"] = len(self.tasks)
        if include_tasks is not None:
            data["tasks"] = [task.to_dict(include_overdue=True) for task in include_tasks]
        return data

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        if self.password.startswith(("pbkdf2:", "scrypt:")):
            return check_password_hash(self.password, pwd)
        return self.password == hashlib.md5(pwd.encode()).hexdigest()

    def is_admin(self):
        return self.role == "admin"
