================================
ARCHITECTURE AUDIT REPORT
================================

Project: task-manager-api
Stack:   Python + Flask 3.0.0
Files:   11 analyzed | ~1152 LOC total

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 2   |
| HIGH     | 3   |
| MEDIUM   | 2   |
| LOW      | 2   |

**Total Findings: 9**

---

## Findings

### [CRITICAL] Deprecated MD5 Password Hashing

File: models/user.py, Lines: 27-32

```python
    def set_password(self, pwd):

        self.password = hashlib.md5(pwd.encode()).hexdigest()

    def check_password(self, pwd):
        return self.password == hashlib.md5(pwd.encode()).hexdigest()
```

Impact: Password hashes are trivial to crack with modern tooling, exposing all user accounts.

---

### [CRITICAL] Hardcoded Flask Secret Key

File: app.py, Lines: 11-13

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key-123'
```

Impact: Anyone with source access can forge signed data and compromise session integrity.

---

### [HIGH] Hardcoded SMTP Credentials in Source

File: services/notification_service.py, Lines: 7-10

```python
        self.email_host = 'smtp.gmail.com'
        self.email_port = 587
        self.email_user = 'taskmanager@gmail.com'
        self.email_password = 'senha123'
```

Impact: Embedded email credentials can be leaked and abused for account takeover or spam.

---

### [HIGH] Blocking Email Delivery in Notification Flow

File: services/notification_service.py, Lines: 15-20

```python
            server = smtplib.SMTP(self.email_host, self.email_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(self.email_user, to, message)
            server.quit()
```

Impact: Every notification performs synchronous network I/O, increasing request latency and timeout risk.

---

### [HIGH] N+1 Queries While Enriching Task Listings

File: routes/task_routes.py, Lines: 41-53

```python
            if t.user_id:
                user = User.query.get(t.user_id)
                if user:
                    task_data['user_name'] = user.name
            if t.category_id:
                cat = Category.query.get(t.category_id)
                if cat:
                    task_data['category_name'] = cat.name
```

Impact: Listing tasks scales with extra per-row queries, causing avoidable database load and slower responses.

---

### [MEDIUM] Deprecated Query.get API Still Used in Routes

File: routes/task_routes.py, Lines: 65-68

```python
@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
```

Impact: Legacy ORM access patterns increase upgrade risk with SQLAlchemy 2.x and newer Flask-SQLAlchemy releases.

---

### [MEDIUM] Duplicated Task Serialization and Overdue Logic

File: routes/task_routes.py, Lines: 17-39; models/task.py, Lines: 23-36

```python
            task_data['created_at'] = str(t.created_at)
            task_data['updated_at'] = str(t.updated_at)
            task_data['due_date'] = str(t.due_date) if t.due_date else None
            task_data['tags'] = t.tags.split(',') if t.tags else []
            if t.due_date:
                if t.due_date < datetime.utcnow():
```

```python
    def to_dict(self):
        data = {}
        data['id'] = self.id
        data['title'] = self.title
        data['description'] = self.description
        data['status'] = self.status
        data['priority'] = self.priority
```

Impact: Two representations of the same entity can drift apart and create inconsistent API responses.

---

### [LOW] Generic Exception Handling Hides Root Causes

File: routes/task_routes.py, Lines: 61-63

```python
        return jsonify(result), 200
    except:
        return jsonify({'error': 'Erro interno'}), 500
```

Impact: Swallowing all exceptions removes debugging context and makes operational failures harder to diagnose.

---

### [LOW] Magic Numbers for Priority Bounds and Tag Length

File: models/task.py, Lines: 18-18; utils/helpers.py, Lines: 112-115

```python
    tags = db.Column(db.String(500), nullable=True)
```

```python
MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 3
MIN_PASSWORD_LENGTH = 4
DEFAULT_PRIORITY = 3
```

Impact: Business limits are scattered as literals, making intent unclear and changes error-prone.

---

================================
PHASE 2 COMPLETE
================================

Total Findings: 9
  - CRITICAL: 2
  - HIGH: 3
  - MEDIUM: 2
  - LOW: 2

================================

Proceed with refactoring (Phase 3)? [y/n]
