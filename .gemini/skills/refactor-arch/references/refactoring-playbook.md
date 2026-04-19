# Refactoring Playbook

## Objetivo

Este playbook define **padrões concretos de refatoração** para transformar codebases legadas em uma arquitetura **MVC (Model-View-Controller)**, eliminando anti-patterns e melhorando qualidade, segurança e manutenibilidade.

Cada padrão contém:

* Sinais de detecção
* Estratégia de refatoração
* Exemplo antes/depois

---

# 1. God Class → Separação em MVC

## Sinais

* Arquivo com múltiplas responsabilidades:

  * lógica de negócio
  * acesso a banco
  * rotas/endpoints

## Estratégia

* Extrair:

  * Models → acesso a dados
  * Controllers → regras de negócio
  * Routes/Views → endpoints

## Antes (Python Flask)

```python
# models.py
def criar_usuario(data):
    conn.execute("INSERT INTO users ...")
    return {"status": "ok"}

@app.route("/users", methods=["POST"])
def route():
    return criar_usuario(request.json)
```

## Depois

```python
# models/user_model.py
def insert_user(data):
    conn.execute("INSERT INTO users ...")

# controllers/user_controller.py
def create_user(data):
    insert_user(data)
    return {"status": "ok"}

# routes/user_routes.py
@app.route("/users", methods=["POST"])
def create():
    return create_user(request.json)
```

---

# 2. Hardcoded Credentials → Configuração Centralizada

## Sinais

* Senhas, tokens ou chaves no código

## Estratégia

* Extrair para arquivo de config/env
* Usar variáveis de ambiente

## Antes

```python
SECRET_KEY = "123456"
DB_URL = "postgres://user:pass@localhost"
```

## Depois

```python
# config/settings.py
import os

SECRET_KEY = os.getenv("SECRET_KEY")
DB_URL = os.getenv("DB_URL")
```

---

# 3. Business Logic em Controller → Service Layer

## Sinais

* Controllers com regras complexas

## Estratégia

* Criar camada de serviço

## Antes

```javascript
app.post("/order", (req, res) => {
  if(req.body.total > 100){
    // desconto
  }
});
```

## Depois

```javascript
// services/orderService.js
function processOrder(data){
  if(data.total > 100){
    // desconto
  }
}

// controller
app.post("/order", (req, res) => {
  processOrder(req.body);
});
```

---

# 4. SQL Inline → Model Abstraction

## Sinais

* Queries SQL espalhadas

## Estratégia

* Centralizar em models

## Antes

```python
def get_users():
    return conn.execute("SELECT * FROM users")
```

## Depois

```python
# models/user_model.py
def find_all():
    return conn.execute("SELECT * FROM users")

# controller
def get_users():
    return find_all()
```

---

# 5. Falta de Error Handling → Middleware Global

## Sinais

* try/catch repetido ou inexistente

## Estratégia

* Criar handler central

## Antes

```python
@app.route("/users")
def get_users():
    try:
        ...
    except:
        return "error"
```

## Depois

```python
# middlewares/error_handler.py
def handle_error(e):
    return {"error": str(e)}, 500
```

---

# 6. Rotas Misturadas → Modularização de Routes

## Sinais

* Todas rotas em um único arquivo

## Estratégia

* Separar por domínio

## Antes

```python
@app.route("/users")
@app.route("/orders")
@app.route("/products")
```

## Depois

```
routes/
  user_routes.py
  order_routes.py
  product_routes.py
```

---

# 7. Estado Global Mutável → Injeção de Dependência

## Sinais

* Variáveis globais compartilhadas

## Estratégia

* Passar dependências explicitamente

## Antes

```python
db = Database()
```

## Depois

```python
def create_user(db, data):
    db.insert(data)
```

---

# 8. APIs Deprecated → Substituição Moderna

## Sinais

* Uso de APIs obsoletas

## Estratégia

* Substituir por versão atual

## Antes (Flask antigo)

```python
from flask.ext.sqlalchemy import SQLAlchemy
```

## Depois

```python
from flask_sqlalchemy import SQLAlchemy
```

---

# 9. Código Duplicado → Funções Reutilizáveis

## Sinais

* Blocos repetidos

## Estratégia

* Extrair função comum

## Antes

```python
if not user:
    return {"error": "not found"}
```

## Depois

```python
def validate_user(user):
    if not user:
        raise Exception("not found")
```

---

# 10. Falta de Entry Point → Composition Root

## Sinais

* Inicialização espalhada

## Estratégia

* Criar ponto único de inicialização

## Depois (estrutura final)

```
src/
  config/
  models/
  controllers/
  routes/
  middlewares/
  app.py
```

---

# Regras Gerais de Refatoração

* Nunca quebrar contratos de API existentes
* Preservar endpoints originais
* Refatorar incrementalmente
* Validar após cada mudança
* Priorizar problemas CRITICAL → LOW

---

# Checklist de Aplicação

Antes de finalizar:

* [ ] Nenhuma lógica de negócio em routes
* [ ] Nenhuma query SQL fora de models
* [ ] Configuração externalizada
* [ ] Controllers organizados por domínio
* [ ] Error handling centralizado
* [ ] Estrutura MVC aplicada
* [ ] Código duplicado removido

---

# Resultado Esperado

Uma codebase com:

* Separação clara de responsabilidades
* Alta coesão e baixo acoplamento
* Estrutura previsível e escalável
* Pronta para testes e evolução
