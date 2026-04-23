================================
ARCHITECTURE AUDIT REPORT
================================

Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 analyzed | ~780 LOC total

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 2     |
| HIGH     | 2     |
| MEDIUM   | 2     |
| LOW      | 3     |

**Total Findings: 9**

---

## Findings

### [CRITICAL] Hardcoded Secret And Forced Debug Mode

File: app.py, Lines: 6-8

```python
app = Flask(__name__)
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
app.config["DEBUG"] = True
CORS(app)
```

Impact: Secrets are exposed in source and debug mode increases the risk of sensitive runtime disclosure.

---

### [CRITICAL] Arbitrary SQL Execution Endpoint

File: app.py, Lines: 61-69

```python
    dados = request.get_json()
    query = dados.get("sql", "")
    if not query:
        return jsonify({"erro": "Query não informada"}), 400
    cursor.execute(query)
```

Impact: Any caller can execute raw SQL against the database and fully compromise application data.

---

### [HIGH] Inline Order Workflow Without Service Boundary

File: controllers.py, Lines: 203-210

```python
        resultado = models.criar_pedido(usuario_id, itens)
        if "erro" in resultado:
            return jsonify({"erro": resultado["erro"], "sucesso": False}), 400
        print("ENVIANDO EMAIL: Pedido " + str(resultado["pedido_id"]) + " criado para usuario " + str(usuario_id))
        print("ENVIANDO SMS: Seu pedido foi recebido!")
```

Impact: The HTTP layer is directly orchestrating persistence outcomes and operational side effects, making order changes fragile and hard to test.

---

### [HIGH] Global Shared Database Connection

File: database.py, Lines: 4-10

```python
db_connection = None
db_path = "loja.db"

def get_db():
    global db_connection
    if db_connection is None:
```

Impact: A mutable process-wide SQLite connection couples requests together and increases concurrency and lifecycle risks.

---

### [MEDIUM] N+1 Queries During Order Hydration

File: models.py, Lines: 187-193

```python
        cursor2 = db.cursor()
        cursor2.execute("SELECT * FROM itens_pedido WHERE pedido_id = " + str(row["id"]))
        itens = cursor2.fetchall()
        for item in itens:
            cursor3.execute("SELECT nome FROM produtos WHERE id = " + str(item["produto_id"]))
```

Impact: Order listing cost grows with the number of rows and items, degrading performance as the dataset expands.

---

### [MEDIUM] Duplicated Product Validation Rules

File: controllers.py, Lines: 28-35, 72-79

```python
        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400
        if "nome" not in dados:
            return jsonify({"erro": "Nome é obrigatório"}), 400
        if "preco" not in dados:
```

Impact: Validation logic is maintained in more than one handler, which makes future rule changes drift between create and update flows.

---

### [LOW] Discount Thresholds Hardcoded As Magic Numbers

File: models.py, Lines: 256-262

```python
    desconto = 0
    if faturamento > 10000:
        desconto = faturamento * 0.1
    elif faturamento > 5000:
        desconto = faturamento * 0.05
```

Impact: Business thresholds are opaque and require editing core logic instead of changing named constants or configuration.

---

### [LOW] Order Status Values Scattered As Magic Strings

File: controllers.py, Lines: 240-247

```python
        novo_status = dados.get("status", "")
        if novo_status not in ["pendente", "aprovado", "enviado", "entregue", "cancelado"]:
            return jsonify({"erro": "Status inválido"}), 400
        models.atualizar_status_pedido(pedido_id, novo_status)
        if novo_status == "aprovado":
```

Impact: Repeated literal status values invite typos and make workflow changes harder to coordinate.

---

### [LOW] Inconsistent Identifier Language In Core Database Module

File: database.py, Lines: 4-8

```python
db_connection = None
db_path = "loja.db"

def get_db():
    global db_connection
```

Impact: Mixing English infrastructure names with Portuguese domain naming reduces consistency and slows maintenance.

---

================================
PHASE 2 COMPLETE
================================

Total Findings: 9
  - CRITICAL: 2
  - HIGH: 2
  - MEDIUM: 2
  - LOW: 3

================================

Proceed with refactoring (Phase 3)? [y/n]
