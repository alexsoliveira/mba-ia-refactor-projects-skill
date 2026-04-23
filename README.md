# Criação de Skills — Refatoração Arquitetural Automatizada

Ao longo do curso você aprendeu o que são Skills e como elas permitem que um agente de IA atue como um especialista em tarefas específicas. Agora imagine o seguinte cenário: você herdou 3 projetos legados com problemas de arquitetura, segurança e qualidade de código. Revisar e corrigir tudo manualmente levaria dias.

Neste desafio, você vai criar uma Skill que automatiza esse processo — analisando, auditando e refatorando qualquer projeto para o padrão MVC, independente da tecnologia.

## Objetivo

Você deve entregar uma Skill capaz de:

- Analisar uma codebase detectando linguagem, framework e arquitetura atual
- Identificar anti-patterns e code smells, classificando por severidade com arquivo e linha exatos
- Gerar um relatório de auditoria estruturado com todos os achados
- Refatorar o projeto para o padrão MVC (Model-View-Controller), eliminando os problemas encontrados
- Validar o resultado garantindo que a aplicação continua funcionando após as mudanças

A skill deve ser agnóstica de tecnologia, funcionando com diferentes linguagens e frameworks.

## Contexto

### Definição de Severidades

Para padronizar a sua auditoria e os relatórios gerados pela IA, utilize a seguinte escala de classificação baseada em problemas de MVC e SOLID:

- **CRITICAL:** Falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis (ex: credenciais hardcoded, SQL Injection) ou violam completamente a separação de responsabilidades (ex: "God Class" contendo banco de dados, lógicas complexas e roteamento no mesmo arquivo).
- **HIGH:** Fortes violações do padrão MVC ou princípios SOLID que dificultam muito a manutenção e testes (ex: lógicas de negócio pesadas presas dentro de Controllers, forte acoplamento sem Injeção de Dependência, ou uso de estado global mutável em toda a aplicação).
- **MEDIUM:** Problemas de padronização, duplicação de código ou gargalos de performance moderada (ex: Queries N+1 no banco de dados, uso inadequado de middlewares, validações ausentes nas rotas).
- **LOW:** Melhorias de legibilidade, nomenclatura de variáveis ruins, ou "magic numbers" soltos pelo código.

### Exemplo de Uso no CLI

```bash
# Executar a skill no projeto com problemas
cd code-smells-project
claude "/refactor-arch"
```

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:      Flask 3.1.1
Dependencies:  flask-cors
Domain:        E-commerce API (produtos, pedidos, usuários)
Architecture:  Monolítica — tudo em 4 arquivos, sem separação de camadas
Source files:  4 files analyzed
DB tables:     produtos, usuarios, pedidos, itens_pedido
================================
```

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 5 | MEDIUM: 2 | LOW: 3

## Findings

### [CRITICAL] God Class / God Method
File: models.py:1-350
Description: Arquivo único contém toda lógica de negócio, queries SQL, validação e formatação para 4 domínios diferentes.
Impact: Impossível testar em isolamento, qualquer mudança afeta tudo.
Recommendation: Separar em models e controllers por domínio.

### [CRITICAL] Hardcoded Credentials
File: app.py:8
Description: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123'
...

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```

```
[... refatoração executada ...]

================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
src/
├── config/settings.py
├── models/
│   ├── produto_model.py
│   └── usuario_model.py
├── views/
│   └── routes.py
├── controllers/
│   ├── produto_controller.py
│   └── pedido_controller.py
├── middlewares/error_handler.py
└── app.py (composition root)

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

## Tecnologias obrigatórias

- **Ferramenta:** uma das três opções abaixo (não são aceitas outras ferramentas):
  - Claude Code
  - Gemini CLI
  - OpenAI Codex
- **Recurso:** Custom Skills (ou o equivalente na ferramenta escolhida)
- **Formato dos arquivos de referência:** Markdown
- **Projetos-alvo:** Python/Flask (2 projetos) e Node.js/Express (1 projeto) (fornecidos no repositório base)

> **Nota sobre a ferramenta:** Os exemplos deste documento usam o Claude Code (`.claude/skills/`) como referência, pois é a ferramenta utilizada no curso. Se você optar por Gemini CLI ou Codex, adapte o nome da pasta e o comando de invocação conforme a convenção dela — o conceito de skill e a estrutura interna (SKILL.md + arquivos de referência) permanecem os mesmos.

## Requisitos

### 1. Análise Manual dos Projetos

Antes de criar a skill, você deve entender os problemas que ela vai resolver.

**Tarefas:**

- Analisar o projeto `code-smells-project/` (Python/Flask — API de E-commerce)
- Analisar o projeto `ecommerce-api-legacy/` (Node.js/Express — LMS API com fluxo de checkout)
- Analisar o projeto `task-manager-api/` (Python/Flask — API de Task Manager)

Para cada projeto, identificar e documentar no mínimo 5 problemas, incluindo pelo menos:

- 1 de severidade CRITICAL ou HIGH
- 2 de severidade MEDIUM
- 2 de severidade LOW

Documentar os achados na seção "Análise Manual" do seu `README.md`

> **Dica:** Não precisa encontrar todos os problemas — foque nos que têm maior impacto arquitetural. Use os projetos como insumo para entender quais padrões sua skill precisa detectar.

> **Por que 3 projetos?** Dois são Python/Flask (com níveis de organização diferentes) e um é Node.js/Express. Sua skill precisa funcionar nos 3 para provar que é verdadeiramente agnóstica de tecnologia — lidando tanto com código completamente desestruturado quanto com projetos que já possuem alguma separação de camadas.

### 2. Criação da Skill

Agora que você conhece os problemas, crie uma skill que os detecte, gere um relatório de auditoria e corrija automaticamente.

**Tarefas:**

Criar a skill dentro do projeto `code-smells-project/` e implementar o SKILL.md com 3 fases sequenciais:

- **Fase 1 — Análise:** Detectar stack, mapear arquitetura atual, imprimir resumo
- **Fase 2 — Auditoria:** Cruzar código contra catálogo de anti-patterns, gerar relatório, pedir confirmação
- **Fase 3 — Refatoração:** Reestruturar para o padrão MVC, validar que funciona

Criar arquivos de referência em Markdown que forneçam à skill o conhecimento necessário para executar as 3 fases. Os arquivos devem cobrir **obrigatoriamente** as seguintes áreas de conhecimento:

| Área de conhecimento | O que deve conter |
|---|---|
| Análise de projeto | Heurísticas para detecção de linguagem, framework, banco de dados e mapeamento de arquitetura |
| Catálogo de anti-patterns | Anti-patterns com sinais de detecção e classificação de severidade |
| Template de relatório | Formato padronizado do relatório de auditoria (Fase 2) |
| Guidelines de arquitetura | Regras do padrão MVC alvo (camadas Models, Views/Routes e Controllers, responsabilidades de cada uma) |
| Playbook de refatoração | Padrões concretos de transformação para cada anti-pattern (com exemplos de código) |

> **Nota:** Você tem liberdade para organizar os arquivos de referência como preferir — pode usar os nomes e a quantidade de arquivos que fizer sentido para sua skill. O importante é que todas as 5 áreas de conhecimento estejam cobertas. O nome da skill (`refactor-arch`) e o arquivo `SKILL.md` são obrigatórios e não devem ser alterados. O path da skill segue a convenção da ferramenta escolhida (no Claude Code, por exemplo, é `.claude/skills/refactor-arch/`).

**Requisitos da skill:**

- Deve ser agnóstica de tecnologia — deve funcionar corretamente nos 3 projetos fornecidos, independente da stack ou nível de organização
- O catálogo de anti-patterns deve conter no mínimo 8 anti-patterns com severidade distribuída (CRITICAL, HIGH, MEDIUM, LOW)
- O catálogo deve incluir detecção de APIs deprecated — identificar uso de APIs obsoletas e recomendar o equivalente moderno
- O playbook deve ter no mínimo 8 padrões de transformação com exemplos de código antes/depois
- A Fase 2 deve pausar e pedir confirmação antes de modificar qualquer arquivo
- A Fase 3 deve validar o resultado (boot da aplicação + endpoints funcionando)

### 3. Execução da Skill

Execute sua skill nos 3 projetos e valide que ela funciona em todas as stacks.

#### Projeto 1 — code-smells-project (Python/Flask)

Invocar a skill no Claude Code:

```bash
claude "/refactor-arch"
```

> **Nota:** O comando acima é o exemplo com Claude Code. Se você estiver usando Gemini CLI ou Codex, utilize o comando equivalente para invocar uma skill na sua ferramenta.

- Verificar que a Fase 1 detecta corretamente a stack e imprime o resumo
- Verificar que a Fase 2 encontra no mínimo 5 dos problemas documentados na sua análise manual
- Confirmar a execução da Fase 3
- Verificar que a Fase 3:
  - Cria a estrutura de diretórios baseada em MVC
  - A aplicação inicia sem erros
  - Os endpoints originais continuam respondendo
- Salvar o relatório de auditoria (output da Fase 2) em `reports/audit-project-1.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 2 — ecommerce-api-legacy (Node.js/Express)

Prove que sua skill é reutilizável em outro projeto de backend, mas com stack diferente.

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `ecommerce-api-legacy/`
- Invocar a skill:

```bash
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

- Verificar que as 3 fases executam corretamente neste projeto
- Salvar o relatório em `reports/audit-project-2.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 3 — task-manager-api (Python/Flask)

Agora o teste com um projeto Python/Flask que já possui alguma organização de camadas (models, routes, services, utils).

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `task-manager-api/`
- Invocar a skill:

```bash
cd ../task-manager-api
claude "/refactor-arch"
```

- Verificar que:
  - A Fase 1 detecta corretamente Python/Flask como stack e identifica o domínio de Task Manager
  - A Fase 2 identifica problemas mesmo em um projeto parcialmente organizado
  - A Fase 3 melhora a estrutura sem quebrar a aplicação (todos os endpoints devem continuar respondendo)
- Salvar o relatório em `reports/audit-project-3.md`
- Commitar o código refatorado do projeto no repositório

> **Nota:** Este projeto já possui alguma separação de camadas, mas isso não significa que a arquitetura está adequada. A skill deve identificar tanto problemas de código (segurança, performance, qualidade) quanto oportunidades de melhoria arquitetural. Se houver mudanças estruturais necessárias, a skill deve propô-las e executá-las.

#### Validação

Para cada projeto refatorado, valide o seguinte checklist:

```markdown
## Checklist de Validação

### Fase 1 — Análise
- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [ ] Relatório segue o template definido nos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Mínimo de 5 findings identificados
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para visualização ou roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente
```

> **Dica:** Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Análise Manual dos Projetos

### Projeto 1: code-smells-project (Python/Flask — API de E-commerce)

#### [CRITICAL] Segredos Hardcoded e Debug Ativado em Runtime
- **Arquivo:** [code-smells-project/app.py](code-smells-project/app.py#L6-L8)
- **Linhas:** 6-8
- **Problema:** A aplicação fixa `SECRET_KEY` no código e força `DEBUG = True` em runtime:
  ```python
  app = Flask(__name__)
  app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
  app.config["DEBUG"] = True
  ```
- **Impacto:** Facilita exposição indevida em ambientes produtivos e enfraquece a proteção de sessão
- **Classificação:** CRITICAL

#### [CRITICAL] Consultas SQL em Loop (N+1 Query Problem)
- **Arquivo:** [code-smells-project/models.py](code-smells-project/models.py#L187-L193)
- **Linhas:** 187-193
- **Problema:** A hidratação dos pedidos faz queries adicionais para itens e nomes de produtos dentro de loops, ampliando o número de acessos ao banco conforme a resposta cresce
- **Código:**
  ```python
  cursor2 = db.cursor()
  cursor2.execute("SELECT * FROM itens_pedido WHERE pedido_id = " + str(row["id"]))
  itens = cursor2.fetchall()
  for item in itens:
      cursor3 = db.cursor()
  ```
- **Impacto:** O tempo de resposta cresce com quantidade de pedidos e itens, degradando performance sob carga
- **Classificação:** CRITICAL

#### [HIGH] Lógica de Negócio Desestruturada — Sem Camada Service
- **Arquivo:** [code-smells-project/controllers.py](code-smells-project/controllers.py#L203-L210)
- **Linhas:** 203-210
- **Problema:** O fluxo de criação de pedido acopla diretamente controller, persistência e side effects operacionais, sem uma camada intermediária para orquestração
- **Impacto:** A manutenção do fluxo HTTP fica frágil e os testes ficam mais difíceis de isolar
- **Classificação:** HIGH

#### [MEDIUM] Magic Numbers e Strings Sem Constantes
- **Arquivo:** [code-smells-project/models.py](code-smells-project/models.py#L256-L262)
- **Linhas:** 256-262
- **Problema:** Regras de desconto usam limiares e percentuais hardcoded (10000, 5000, 1000, 10%, 5%, 2%) sem extração para constantes
  ```python
  if faturamento > 10000:
      desconto = faturamento * 0.1
  ```
- **Impacto:** As regras ficam opacas e qualquer ajuste exige edição direta da lógica
- **Classificação:** MEDIUM

#### [MEDIUM] Duplicação de Validação Entre Criação e Atualização de Produto
- **Arquivo:** [code-smells-project/controllers.py](code-smells-project/controllers.py#L28-L35) + [code-smells-project/controllers.py](code-smells-project/controllers.py#L72-L79)
- **Linhas:** 28-35 e 72-79
- **Problema:** As validações de produto são repetidas entre handlers de criação e atualização, exigindo manutenção paralela
- **Impacto:** Regras podem divergir ao longo do tempo e introduzir comportamento inconsistente
- **Classificação:** MEDIUM

#### [LOW] Status como Magic Strings
- **Arquivo:** [code-smells-project/controllers.py](code-smells-project/controllers.py#L240-L247)
- **Linhas:** 240-247
- **Problema:** O fluxo de atualização de pedido usa strings literais como `"pendente"`, `"aprovado"`, `"enviado"`, `"entregue"` e `"cancelado"` em vez de centralizar esses valores
- **Impacto:** A lógica fica mais suscetível a typos e a mudanças manuais espalhadas
- **Classificação:** LOW

#### [LOW] Inconsistência na Nomenclatura
- **Arquivo:** [code-smells-project/database.py](code-smells-project/database.py#L4-L8)
- **Linhas:** 4-8
- **Problema:** A base mistura termos em português e inglês, por exemplo `db_connection`, `db_path` e `get_db()` convivendo com rotas e funções nomeadas em português
- **Impacto:** A leitura da base fica menos consistente e o onboarding mais custoso
- **Classificação:** LOW

---

### Projeto 2: ecommerce-api-legacy (Node.js/Express — LMS API com Checkout)

#### [CRITICAL] Credenciais Sensíveis Hardcoded em Produção
- **Arquivo:** [src/utils.js](src/utils.js#L1-L5)
- **Linhas:** 1-5
- **Problema:** Production API keys e senhas visíveis no código fonte:
  ```javascript
  dbUser: "admin_master",
  dbPass: "senha_super_secreta_prod_123", 
  paymentGatewayKey: "pk_live_1234567890abcdef",
  ```
- **Impacto:** Acesso não autorizado ao banco de dados e gateway de pagamento; exposição de dados sensíveis
- **Classificação:** CRITICAL

#### [CRITICAL] Criptografia Fraca (Non-Encryption)
- **Arquivo:** [src/utils.js](src/utils.js#L19-L25)
- **Linhas:** 19-25
- **Problema:** Função `badCrypto()` não é criptografia — apenas concatenação de Base64:
  ```javascript
  function badCrypto(pwd) {
      let hash = "";
      for(let i = 0; i < 10000; i++) {
          hash += Buffer.from(pwd).toString('base64').substring(0, 2);
      }
      return hash.substring(0, 10);
  }
  ```
  Base64 é reversível e determinístico (mesmo password = mesmo hash sempre)
- **Impacto:** Senhas não são seguras; atacante pode fazer força bruta facilmente
- **Classificação:** CRITICAL

#### [CRITICAL] Falta de Autenticação/Autorização em Endpoints Críticos
- **Arquivo:** [src/AppManager.js](src/AppManager.js#L93-L120)
- **Linhas:** 93-120
- **Problema:** Endpoint `/api/admin/financial-report` sem proteção — qualquer pessoa pode acessar relatório financeiro
- **Impacto:** Exposição de dados financeiros confidenciais; violação de confidencialidade
- **Classificação:** CRITICAL

#### [HIGH] Callback Hell com Tratamento de Erro Deficiente
- **Arquivo:** [src/AppManager.js](src/AppManager.js#L20-L80)
- **Linhas:** 20-80
- **Problema:** Callbacks aninhados progressivamente (pyramid of doom) com error handling inadequado:
  ```javascript
  this.db.get(..., (err, user) => {
      if (err) return ...;
      let processPaymentAndEnroll = (userId) => {
          this.db.run(..., function(err) {
              if (err) return ...;
              self.db.run(..., function(err) {
                  if (err) return ...;
                  // ... mais níveis
              });
          });
      };
  });
  ```
- **Impacto:** Impossível ler código; erros não propagam corretamente; testes complexos
- **Classificação:** HIGH

#### [HIGH] Lógica de Processamento de Pagamento Inline na Route Handler
- **Arquivo:** [src/AppManager.js](src/AppManager.js#L20-L80)
- **Linhas:** 20-80
- **Problema:** Toda transformação de pagamento, criação de usuário, e lógica de matrícula dentro de `setupRoutes()` — sem Service Layer ou Controllers
- **Impacto:** Impossível testar lógica de pagamento isoladamente; mudanças arriscadas; sem reutilização
- **Classificação:** HIGH

#### [MEDIUM] Estado Global Mutável
- **Arquivo:** [src/utils.js](src/utils.js#L7-L8)
- **Linhas:** 7-8
- **Problema:** `globalCache` e `totalRevenue` são variáveis globais compartilhadas:
  ```javascript
  let globalCache = {};
  let totalRevenue = 0;
  ```
- **Impacto:** Race conditions em concorrência; estado imprevisível; testes não-isolados
- **Classificação:** MEDIUM

#### [MEDIUM] Banco de Dados Em Memória (Não Persistente)
- **Arquivo:** [src/AppManager.js](src/AppManager.js#L11)
- **Linhas:** 11
- **Problema:** `this.db = new sqlite3.Database(':memory:')` — banco de dados perde todos os dados ao reiniciar a aplicação
- **Impacto:** Perda de dados; inadequado para produção; testes não realistas
- **Classificação:** MEDIUM

#### [LOW] Nomenclatura de Variáveis Abreviada
- **Arquivo:** [src/AppManager.js](src/AppManager.js#L23-L25)
- **Linhas:** 23-25
- **Problema:** Variáveis com nomes cryptografados: `u`, `e`, `p`, `cid`, `cc`, `enrId`
  ```javascript
  let u = req.body.usr;      // username?
  let e = req.body.eml;      // email?
  let p = req.body.pwd;      // password?
  let cid = req.body.c_id;   // course_id?
  ```
- **Impacto:** Reduz legibilidade; dificulta manutenção
- **Classificação:** LOW

#### [LOW] Magic Strings para Status
- **Arquivo:** [src/AppManager.js](src/AppManager.js#L32)
- **Linhas:** 32
- **Problema:** Status de pagamento como strings simples ("PAID", "DENIED") sem constantes:
  ```javascript
  let status = cc.startsWith("4") ? "PAID" : "DENIED";
  ```
- **Impacto:** Erros de digitação; sem validação consistente
- **Classificação:** LOW

---

### Projeto 3: task-manager-api (Python/Flask — API de Task Manager)

#### [CRITICAL] Hashing de Senhas com MD5 (Deprecated)
- **Arquivo:** [models/user.py](models/user.py#L23-L27)
- **Linhas:** 23-27
- **Problema:** MD5 é criptograficamente quebrado desde 1996. Implementação:
  ```python
  def set_password(self, pwd):
      self.password = hashlib.md5(pwd.encode()).hexdigest()
  ```
- **Impacto:** Senhas podem ser quebradas com tabelas hash (rainbow tables); não seguro para produção
- **Classificação:** CRITICAL

#### [CRITICAL] Chave Secreta Hardcoded
- **Arquivo:** [app.py](app.py#L12)
- **Linhas:** 12
- **Problema:** `app.config['SECRET_KEY'] = 'super-secret-key-123'` — hardcoded em produção
- **Impacto:** Session hijacking; falsificação de CSRF tokens
- **Classificação:** CRITICAL

#### [HIGH] Credenciais de Email Hardcoded
- **Arquivo:** [services/notification_service.py](services/notification_service.py#L8-L9)
- **Linhas:** 8-9
- **Problema:** Email e senha visíveis no código fonte:
  ```python
  self.email_user = 'taskmanager@gmail.com'
  self.email_password = 'senha123'
  ```
- **Impacto:** Acesso não autorizado à conta de email; spam de e-mails
- **Classificação:** HIGH

#### [HIGH] Operação Síncrona de Email Dentro de Request Handler
- **Arquivo:** [services/notification_service.py](services/notification_service.py#L12-L19)
- **Linhas:** 12-19
- **Problema:** `send_email()` bloqueia requisição HTTP enquanto envia email (`starttls()`, `login()`, `sendmail()`)
- **Impacto:** Requisições lentas; timeout em rede lenta; má experiência do usuário
- **Classificação:** HIGH

#### [HIGH] Problema N+1 Query em Listagem de Tasks
- **Arquivo:** [routes/task_routes.py](routes/task_routes.py#L12-L50)
- **Linhas:** 12-50
- **Problema:** Loop por tasks com queries individuais dentro do loop:
  ```python
  for t in tasks:  # Query 1: pega todas tasks
      if t.user_id:
          user = User.query.get(t.user_id)  # Query N+1
      if t.category_id:
          cat = Category.query.get(t.category_id)  # Query N+2
  ```
- **Impacto:** Performance degradada; 1 query raiz + 2N queries adicionais
- **Classificação:** HIGH

#### [MEDIUM] Duplicação de Lógica de Serialização
- **Arquivo:** [models/task.py](models/task.py#L28-L40) vs [routes/task_routes.py](routes/task_routes.py#L12-L50)
- **Linhas:** Vários
- **Problema:** Mesma lógica `to_dict()` implementada em dois lugares:
- **Impacto:** Manutenção duplicada; inconsistências de formato
- **Classificação:** MEDIUM

#### [MEDIUM] Falta de Validação em NotificationService
- **Arquivo:** [services/notification_service.py](services/notification_service.py#L12-L20)
- **Linhas:** 12-20
- **Problema:** Não valida formato de email, se destinatário existe, etc. Apenas tenta enviar
- **Impacto:** Emailsfalham silenciosamente; nenhuma retroação ao usuário
- **Classificação:** MEDIUM

#### [LOW] Handling de Exceção Genérica Demais
- **Arquivo:** [services/notification_service.py](services/notification_service.py#L16)
- **Linhas:** 16
- **Problema:** `except Exception as e:` muito genérica — pega todas exceções sem distinção
- **Impacto:** Difícil debugar; logs pouco informativos
- **Classificação:** LOW

#### [LOW] Magic Number para Campos de Texto
- **Arquivo:** [models/task.py](models/task.py#L12)
- **Linhas:** 12
- **Problema:** `tags = db.Column(db.String(500), nullable=True)` — 500 é magic number sem constante
- **Impacto:** Sem documentação do motivo da escolha
- **Classificação:** LOW

---

## Resumo da Análise Manual

| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---------|----------|------|--------|-----|-------|
| code-smells-project | 2 | 1 | 2 | 2 | **7** |
| ecommerce-api-legacy | 3 | 2 | 3 | 2 | **10** |
| task-manager-api | 2 | 3 | 3 | 2 | **10** |

**Total de problemas identificados: 27**

---

## Entregável

Repositório público no GitHub (fork do repositório base) contendo:

- Skill completa em `.claude/skills/refactor-arch/` (dentro dos 3 projetos)
- Código refatorado dos 3 projetos (resultado da execução da Fase 3, commitado no repositório)
- Relatórios de auditoria em `reports/` (3 arquivos)
- `README.md` atualizado

### Estrutura do repositório

Faça um fork do repositório base contendo os três projetos com code smells.

> **Nota:** A estrutura abaixo usa Claude Code como exemplo (`.claude/skills/`). Se estiver usando outra ferramenta, adapte os caminhos conforme a convenção dela.

```
desafio-skills/
├── README.md                              # Sua documentação
│
├── code-smells-project/                   # Projeto 1 — Python/Flask (API de E-commerce)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← SUA SKILL AQUI
│   │           ├── SKILL.md
│   │           └── (arquivos de referência)
│   ├── app.py
│   ├── controllers.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt
│
├── ecommerce-api-legacy/                  # Projeto 2 — Node.js/Express (LMS API com checkout)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── src/
│   │   ├── app.js
│   │   ├── AppManager.js
│   │   └── utils.js
│   ├── api.http
│   └── package.json
│
├── task-manager-api/                      # Projeto 3 — Python/Flask (API de Task Manager)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── app.py
│   ├── database.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
│
└── reports/                               # Relatórios gerados
    ├── audit-project-1.md                 # Saída da Fase 2 no projeto 1
    ├── audit-project-2.md                 # Saída da Fase 2 no projeto 2
    └── audit-project-3.md                 # Saída da Fase 2 no projeto 3
```

**O que você vai criar:**

- `.claude/skills/refactor-arch/` — A skill completa (SKILL.md + arquivos de referência)
- Código refatorado dos 3 projetos — resultado da execução da Fase 3, commitado no repositório
- `reports/audit-project-{1,2,3}.md` — Relatório de auditoria de cada projeto
- `README.md` — Documentação do seu processo

**O que já vem pronto:**

- `code-smells-project/` — API de E-commerce Python/Flask com code smells intencionais
- `ecommerce-api-legacy/` — LMS API Node.js/Express (com fluxo de checkout) e problemas de implementação
- `task-manager-api/` — API de Task Manager Python/Flask com organização parcial e problemas de segurança/qualidade

> **Dica:** Cada projeto contém problemas intencionais de diferentes severidades (CRITICAL, HIGH, MEDIUM, LOW), incluindo falhas de segurança, violações arquiteturais e problemas de qualidade de código. Parte do desafio é identificá-los por conta própria através da análise manual do código.

### README.md deve conter

**A) Seção "Análise Manual":**

- Lista dos problemas identificados manualmente em cada projeto
- Classificação por severidade
- Justificativa de por que cada problema é relevante

**B) Seção "Construção da Skill":**

- Decisões de design: como estruturou o SKILL.md e os arquivos de referência
- Quais anti-patterns incluiu no catálogo e por quê
- Como garantiu que a skill é agnóstica de tecnologia
- Desafios encontrados e como resolveu

**C) Seção "Resultados":**

- Resumo dos relatórios de auditoria dos 3 projetos (quantos findings por severidade em cada)
- Comparação antes/depois da estrutura de cada projeto
- Checklist de validação preenchido para cada projeto
- Screenshots ou logs mostrando as aplicações rodando após refatoração
- Observações sobre como a skill se comportou em stacks diferentes

**D) Seção "Como Executar":**

- Pré-requisitos (a ferramenta escolhida — Claude Code, Gemini CLI ou Codex — instalada e configurada)
- Comandos para executar a skill em cada projeto
- Como validar que a refatoração funcionou

## Construção da Skill

A skill `refactor-arch` foi desenhada para operar sempre em 3 fases sequenciais e determinísticas: análise, auditoria e refatoração. O `SKILL.md` impõe a ordem das fases, o formato exato de saída da Fase 1, o template literal da Fase 2, a pausa obrigatória antes de qualquer mutação e as validações mínimas para considerar a execução válida.

### Estrutura do SKILL.md

O arquivo principal centraliza o contrato de execução:

- Fase 1 detecta linguagem, framework, dependências, domínio, arquitetura, arquivos executáveis e tabelas do banco.
- Fase 2 cruza o código com um catálogo explícito de anti-patterns, exige no mínimo 5 findings e força alinhamento com a análise manual do `README.md`.
- Fase 3 só pode começar após confirmação humana e deve preservar boot, rotas e comportamento funcional do projeto atual.

### Arquivos de Referência

Os arquivos em `.codex/skills/refactor-arch/references/` foram separados por responsabilidade:

- `analysis.md`: heurísticas de detecção de stack, arquitetura e contagem correta de arquivos-fonte.
- `anti-patterns.md`: catálogo de sinais, severidades e exemplos de overlap esperados para cada projeto.
- `report-template.md`: contrato literal do relatório da Fase 2, incluindo cabeçalho, tabela resumo, findings e footer.
- `mvc-guidelines.md`: definição do alvo arquitetural com direção de dependências `Routes -> Controllers -> Models/Repositories`.
- `refactoring-playbook.md`: transformações concretas para remover hardcoded config, SQL concatenado, N+1, duplicação e acoplamento excessivo.
- `readme-update.md`: regras para sincronizar este `README.md` sem sobrescrever conteúdo útil e sem inventar evidências não verificadas.

### Catálogo de Anti-Patterns

A skill cobre principalmente:

- segredos hardcoded e configuração insegura
- SQL injection, execução arbitrária de SQL e concatenação de query
- ausência de separação de camadas e falta de service layer
- estado global mutável
- N+1 query pattern
- duplicação de validação e serialização
- magic strings, magic numbers e inconsistências de nomenclatura
- uso de APIs obsoletas quando aplicável

Essas famílias foram escolhidas porque aparecem nos 3 projetos-alvo e representam problemas de segurança, arquitetura e manutenção que o desafio pede para detectar e corrigir.

### Estratégia Agnóstica de Tecnologia

A skill evita depender de nomes de arquivos ou convenções específicas de Flask ou Express. A análise parte de sinais observáveis no código e nos manifests do projeto atual, depois adapta o playbook para a maturidade da base:

- no `code-smells-project`, a refatoração foi mais estrutural por se tratar de um monólito
- no `task-manager-api`, a expectativa é preservar mais da organização existente
- no `ecommerce-api-legacy`, a mesma lógica de severidade e separação de responsabilidades continua válida, mesmo com Node.js/Express

### Salvaguardas e Compliance

Foram implementadas salvaguardas específicas para o desafio:

- escopo de execução restrito ao projeto atual por invocação
- persistência do relatório apenas em `reports/audit-project-<N>.md` na raiz do repositório
- alinhamento obrigatório com a seção `## Análise Manual dos Projetos`
- bloqueio da Fase 3 até resposta explícita `y` ou `yes`
- atualização incremental deste `README.md`, preservando seções concretas já existentes

### Desafios Encontrados

Os principais desafios foram manter a saída da Fase 2 estritamente aderente ao template, garantir overlap real com a análise manual sem inventar findings e refatorar o projeto 1 para MVC sem quebrar as rotas já existentes. Também foi necessário validar a refatoração contra o estado real do banco SQLite presente no repositório, em vez de assumir apenas o cenário de seed inicial.

## Resultados

### Projeto 1 - code-smells-project

#### Resumo da Auditoria

Relatório salvo em `reports/audit-project-1.md`.

- CRITICAL: 2
- HIGH: 2
- MEDIUM: 2
- LOW: 3
- Total: 9 findings

#### Antes e Depois

Antes:
- `app.py` concentrava registro de rotas, configuração sensível e endpoints administrativos inseguros.
- `controllers.py` misturava HTTP, validação, orquestração de pedidos e side effects.
- `models.py` concentrava acesso ao SQLite com concatenação de SQL e hidratação N+1.
- `database.py` mantinha conexão global mutável.

Depois:
- `src/config/` centraliza settings e ciclo de vida do banco.
- `src/routes/` faz apenas o binding HTTP.
- `src/controllers/` concentra a orquestração dos casos de uso.
- `src/services/` isola o workflow de pedidos.
- `src/models/` encapsula queries e serialização.
- `src/middlewares/error_handler.py` centraliza respostas de erro.

#### Checklist de Validação

- [x] Estrutura MVC criada em `src/config`, `src/routes`, `src/controllers`, `src/services`, `src/models` e `src/middlewares`
- [x] Configuração sensível removida do código-fonte e lida a partir de ambiente/config
- [x] Endpoint inseguro de SQL arbitrário deixou de executar SQL livre; agora exige token administrativo e allowlist read-only
- [x] Queries principais migradas para parâmetros em vez de concatenação de strings
- [x] Hidratação de pedidos deixou de usar N+1 para buscar itens e nomes de produtos
- [x] Validação duplicada de produto foi consolidada em `src/utils/validators.py`
- [x] `python app.py` inicia sem erro
- [x] Endpoints principais respondem após a refatoração
- [ ] Todos os endpoints do projeto foram exercitados manualmente nesta execução

#### Evidências

Evidências verificadas nesta execução:

- `venv\Scripts\python.exe app.py` permaneceu em execução após o boot, confirmando que o entrypoint real sobe sem erro.
- Via `Flask.test_client()`, os endpoints `GET /`, `GET /health`, `GET /produtos`, `POST /login`, `POST /pedidos`, `GET /pedidos` e `GET /relatorios/vendas` responderam com sucesso.
- `POST /admin/query` retornou `403`, confirmando que o endpoint administrativo não executa mais SQL arbitrário sem autenticação.
- O endpoint `/health` continua funcional, mas não expõe mais `secret_key` nem `db_path`.

#### Observações

Este projeto exigiu refatoração mais profunda do que os demais porque a base original era essencialmente monolítica. Para preservar compatibilidade, os arquivos-raiz (`app.py`, `models.py`, `database.py` e `controllers.py`) foram mantidos como entrypoints ou wrappers finos enquanto a implementação real passou para `src/`.

### Projeto 2 - ecommerce-api-legacy

#### Resumo da Auditoria

Ainda não executado nesta fase do desafio.

#### Antes e Depois

Pendente.

#### Checklist de Validação

- [ ] Auditoria executada
- [ ] Refatoração executada
- [ ] Aplicação validada

#### Evidências

Sem evidências nesta execução.

#### Observações

Subseção reservada para atualização incremental na execução do projeto 2.

### Projeto 3 - task-manager-api

#### Resumo da Auditoria

Ainda não executado nesta fase do desafio.

#### Antes e Depois

Pendente.

#### Checklist de Validação

- [ ] Auditoria executada
- [ ] Refatoração executada
- [ ] Aplicação validada

#### Evidências

Sem evidências nesta execução.

#### Observações

Subseção reservada para atualização incremental na execução do projeto 3.

## Como Executar

### Pré-requisitos

- Codex, Claude Code ou Gemini CLI com suporte a skills/comandos equivalentes
- Python para os projetos Flask e Node.js para o projeto Express
- Dependências instaladas em cada projeto antes da execução

Para o projeto 1:

```bash
cd code-smells-project
pip install -r requirements.txt
```

### Execução por Projeto

Exemplos com a invocação usada neste repositório:

```bash
# Projeto 1
cd code-smells-project
/refactor-arch

# Projeto 2
cd ../ecommerce-api-legacy
/refactor-arch

# Projeto 3
cd ../task-manager-api
/refactor-arch
```

Se estiver usando outra ferramenta, substitua a forma de invocação da skill, mas mantenha o mesmo escopo: um projeto por vez.

### Relatórios Gerados

Os relatórios da Fase 2 devem ser salvos na raiz do repositório:

- `reports/audit-project-1.md`
- `reports/audit-project-2.md`
- `reports/audit-project-3.md`

### Como Validar

Após a Fase 3, valide sempre:

```bash
# Projeto 1
cd code-smells-project
python app.py

# Projeto 2
cd ../ecommerce-api-legacy
npm start

# Projeto 3
cd ../task-manager-api
python app.py
```

Além do boot, exercite endpoints principais do projeto atual. No projeto 1, esta execução validou `GET /`, `GET /health`, `GET /produtos`, `POST /login`, `POST /pedidos`, `GET /pedidos` e `GET /relatorios/vendas`.

### Ordem de execução sugerida

**1. Analisar os projetos manualmente**

Leia o código dos três projetos e documente os problemas encontrados.

**2. Criar a skill**

Escreva o SKILL.md e os arquivos de referência.

**3. Executar nos 3 projetos**

```bash
# Projeto 1
cd code-smells-project
claude "/refactor-arch"

# Projeto 2
cd ../ecommerce-api-legacy
claude "/refactor-arch"

# Projeto 3
cd ../task-manager-api
claude "/refactor-arch"
```

Salve a saída da Fase 2 de cada projeto em `reports/audit-project-{1,2,3}.md`.

**4. Iterar**

Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Critérios de Aceite

A skill deve atingir os seguintes mínimos em **todos os 3 projetos**:

| Critério | Requisito |
|---|---|
| Fase 1 detecta stack corretamente | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 encontra >= 5 findings | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 inclui pelo menos 1 CRITICAL ou HIGH | OBRIGATÓRIO (3/3 projetos) |
| Fase 3 aplicação funciona após refatoração | OBRIGATÓRIO (3/3 projetos) |

**IMPORTANTE:** Todos os critérios devem ser atingidos nos 3 projetos, não apenas em um!

> **Sobre o projeto 3 (task-manager-api):** Este projeto já possui alguma organização. "aplicação funciona" significa que a API inicia sem erros e todos os endpoints continuam respondendo corretamente.

## Referências

- [Claude Code: Skills](https://docs.anthropic.com/en/docs/claude-code/skills) — Documentação oficial sobre como criar e estruturar Skills
- [Claude Code: Overview](https://docs.anthropic.com/en/docs/claude-code/overview) — Visão geral do Claude Code e suas capacidades
- [The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) — Guia completo da Anthropic sobre construção de Skills
- [Equipping Agents for the Real World with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) — Blog oficial da Anthropic sobre Agent Skills

---

## Dicas Finais

- **Comece pela análise manual** — entender os problemas profundamente é essencial para criar uma skill que os detecte.
- **O SKILL.md é um prompt** — ele instrui o agente sobre o que fazer, enquanto os arquivos de referência fornecem o conhecimento de domínio.
- **Seja específico nos sinais de detecção** — "código ruim" não ajuda; "query SQL dentro de loop for" é acionável.
- **Teste incrementalmente** — não tente criar a skill perfeita de primeira.
- **A skill deve ser copiável** — se ela só funciona em um projeto específico, está acoplada demais. Teste nos 3 projetos para validar.
- **Projetos diferentes exigem adaptação** — a Fase 3 de um projeto já parcialmente organizado não vai ter as mesmas transformações de um monolito. Sua skill deve se adaptar ao contexto.
- **Pedir confirmação na Fase 2 é obrigatório** — o humano deve revisar o relatório antes de qualquer modificação.
- **Consulte as referências do curso** — revise a documentação oficial da ferramenta escolhida e os materiais das aulas para relembrar a estrutura e anatomia de uma skill.
