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

#### [CRITICAL] Hardcoded Credentials com Fallback Inseguro
- **Arquivo:** [app.py](app.py#L9)
- **Linhas:** 9
- **Problema:** `app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-keep-it-safe")` — embora use variável de ambiente, o fallback inseguro pode ser usado em produção se a env não estiver configurada, expondo credenciais
- **Impacto:** Session hijacking, falsificação de tokens
- **Classificação:** CRITICAL

#### [CRITICAL] Consultas SQL em Loop (N+1 Query Problem)
- **Arquivo:** [models.py](models.py#L98-L125)
- **Linhas:** 98-125
- **Problema:** Funções `get_pedidos_usuario()` e `get_todos_pedidos()` fazem queries por item dentro de loops aninhados
- **Código:**
  ```python
  for row in rows:  # Loop 1
      cursor_items = db.cursor()
      cursor_items.execute("SELECT ... FROM itens_pedido WHERE pedido_id = ?", ...)  # Query N
      for item in itens:  # Loop 2
          ...
  ```
- **Impacto:** Degradação severa de performance com muitos pedidos; 1 query raiz + N queries por pedido (ex: 100 pedidos = 101 queries)
- **Classificação:** CRITICAL

#### [HIGH] Lógica de Negócio Desestruturada — Sem Camada Service
- **Arquivo:** [models.py](models.py#L1-200) + [controllers.py](controllers.py#L1-200)
- **Linhas:** Vários
- **Problema:** Controllers chamam diretamente funções de models que fazem queries; não há Service Layer ou Repository Pattern. Lógica de desconto hardcoded em models.py:146-153
- **Impacto:** Impossível testar Controller sem BD; mudanças em BD quebram Controllers
- **Classificação:** HIGH

#### [MEDIUM] Magic Numbers e Strings Sem Constantes
- **Arquivo:** [models.py](models.py#L146-L153)
- **Linhas:** 146-153
- **Problema:** Descontos hardcoded (10%, 5%, 2%) e limiares (10000, 5000, 1000) sem constantes isoladas
  ```python
  if faturamento > 10000:
      desconto = faturamento * 0.1
  ```
- **Impacto:** Difícil entender regra de negócio; mudanças devem ser feitas em múltiplos lugares
- **Classificação:** MEDIUM

#### [MEDIUM] Duplicação de Serialização de Dados
- **Arquivo:** [controllers.py](controllers.py#L120-L160) + [models.py](models.py#L5-L8)
- **Linhas:** Vários
- **Problema:** Conversão `dict(row)` repetida em múltiplas funções; não há centralização de serialização
- **Impacto:** Inconsistências na serialização; mudanças devem ser propagadas em N lugares
- **Classificação:** MEDIUM

#### [LOW] Status como Magic Strings
- **Arquivo:** [controllers.py](controllers.py#L135) + [models.py](models.py#L160)
- **Linhas:** Vários
- **Problema:** Status de pedidos como strings simples ("pendente", "aprovado", "cancelado") sem enums ou constantes
- **Impacto:** Erros de digitação; sem validação em tempo de compilação
- **Classificação:** LOW

#### [LOW] Inconsistência na Nomenclatura
- **Arquivo:** [database.py](database.py#L1-80)
- **Linhas:** Vários
- **Problema:** Mistura de nomenclaturas: `get_db()`, `listar_produtos()` (português/inglês), `criar_pedido()`, `atualizar_status_pedido()`
- **Impacto:** Dificuldade manutenção; base de código confusa
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

Descreva aqui as decisões de design da skill, a organização do `SKILL.md`, dos arquivos de referência e como a solução foi mantida agnóstica de tecnologia.

## Resultados

Descreva aqui o resumo dos relatórios gerados, a comparação antes/depois das estruturas dos projetos e o checklist de validação preenchido para cada execução.

## Como Executar

Descreva aqui os pré-requisitos, os comandos para invocar a skill em cada projeto e como validar que a refatoração funcionou.

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
