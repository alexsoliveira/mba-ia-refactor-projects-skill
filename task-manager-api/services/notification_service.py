import smtplib
from datetime import datetime
from threading import Thread

from config.settings import Settings
from utils.helpers import validate_email


class NotificationService:
    def __init__(self):
        self.notifications = []
        self.email_host = Settings.SMTP_HOST
        self.email_port = Settings.SMTP_PORT
        self.email_user = Settings.SMTP_USER
        self.email_password = Settings.SMTP_PASSWORD
        self.smtp_enabled = Settings.SMTP_ENABLED

    def _deliver_email(self, to, subject, body):
        try:
            server = smtplib.SMTP(self.email_host, self.email_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(self.email_user, to, message)
            server.quit()
            print(f"Email enviado para {to}")
            return True
        except Exception as exc:
            print(f"Erro ao enviar email: {exc}")
            return False

    def send_email(self, to, subject, body):
        if not self.smtp_enabled:
            print("SMTP desabilitado; notificação registrada sem envio.")
            return False
        if not validate_email(to):
            raise ValueError("Email inválido para notificação")
        if not self.email_user or not self.email_password:
            raise ValueError("Credenciais SMTP não configuradas")

        Thread(
            target=self._deliver_email,
            args=(to, subject, body),
            daemon=True,
        ).start()
        return True

    def notify_task_assigned(self, user, task):
        subject = f"Nova task atribuída: {task.title}"
        body = (
            f"Olá {user.name},\n\nA task '{task.title}' foi atribuída a você.\n\n"
            f"Prioridade: {task.priority}\nStatus: {task.status}"
        )
        self.send_email(user.email, subject, body)
        self.notifications.append(
            {
                "type": "task_assigned",
                "user_id": user.id,
                "task_id": task.id,
                "timestamp": datetime.utcnow(),
            }
        )

    def notify_task_overdue(self, user, task):
        subject = f"Task atrasada: {task.title}"
        body = f"Olá {user.name},\n\nA task '{task.title}' está atrasada!\n\nData limite: {task.due_date}"
        self.send_email(user.email, subject, body)

    def get_notifications(self, user_id):
        return [notification for notification in self.notifications if notification["user_id"] == user_id]
