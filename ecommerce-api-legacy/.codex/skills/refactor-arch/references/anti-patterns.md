# Anti-Patterns Catalog

Purpose: support Phase 2 audit and severity classification from `SKILL.md`.

Each finding should include:
- What was detected
- Detection signal
- Severity
- Impact
- Recommended remediation

## CRITICAL

### 1. SQL Injection via String Concatenation
- Signal: SQL query assembled with string concat/interpolation using user data.
- Impact: arbitrary data exposure or destructive SQL execution.
- Remediation: parameterized queries or ORM-safe APIs.

### 2. Arbitrary SQL Execution Endpoint
- Signal: endpoint executes raw SQL payload from request body.
- Impact: full database compromise.
- Remediation: remove endpoint or restrict/admin-auth + allowlist operations.

### 3. Hardcoded Secrets/Credentials
- Signal: literals such as `SECRET_KEY`, DB passwords, API keys in source.
- Impact: credential leakage and account/session compromise.
- Remediation: move to environment/config management.

### 4. Broken Layer Separation (God Module)
- Signal: same file contains routing, DB access, and business rules.
- Impact: untestable system, high regression risk.
- Remediation: split into MVC layers and optionally service layer.

## HIGH

### 5. Business Logic in Route/Controller Handlers
- Signal: heavy calculations/transactions directly in handlers.
- Impact: poor reuse, weak testability.
- Remediation: move business logic to controller/service layer.

### 6. Tight Coupling Across Layers / Missing Service Layer
- Signal: direct controller-to-model calls, no service layer, or business rules scattered across handlers and persistence modules.
- Impact: fragile changes and hidden side effects.
- Remediation: establish layer contracts and dependency direction.

### 7. Global Mutable Shared State
- Signal: global DB or cache objects with broad mutable access.
- Impact: concurrency/data consistency issues.
- Remediation: scope dependencies, use request/context lifecycle.

## MEDIUM

### 8. N+1 Query Pattern
- Signal: DB queries inside loops for related entities.
- Impact: significant performance degradation.
- Remediation: use joins/batching/eager loading.

### 9. Code Duplication (DRY Violation)
- Signal: repeated validation/serialization/business fragments.
- Impact: inconsistent fixes and maintenance overhead.
- Remediation: extract reusable helpers/services.

Typical overlap examples for this challenge:
- duplicated request validation across multiple endpoints
- duplicated `dict(row)` / DTO / serialization logic across modules
- repeated response shaping for the same entity

### 10. Missing Input Validation
- Signal: endpoints accept payloads without schema/type checks.
- Impact: runtime errors and inconsistent data.
- Remediation: central request validation.

### 11. Deprecated API Usage
- Signal: obsolete imports/functions/deprecated framework APIs.
- Impact: upgrade fragility and security/runtime risk.
- Remediation: migrate to modern equivalent and version-safe APIs.

## LOW

### 12. Magic Strings/Numbers
- Signal: repeated literals for status/thresholds.
- Impact: typo risk and unclear intent.
- Remediation: constants/enums/config values.

### 13. Inconsistent Naming/Readability Issues
- Signal: mixed naming conventions, unclear identifiers.
- Impact: slower onboarding and higher review cost.
- Remediation: normalize naming and improve clarity.

## Challenge README Alignment

When auditing this repository's 3 target projects, maximize overlap with the manual-analysis section in the root `README.md` before adding supplemental findings.
This alignment is challenge-specific and must remain technology-agnostic:
- do not search only for Flask/Express-specific tokens
- do not force exact README wording when the stack expresses the same issue differently
- match by architectural/security category first, then by repository-specific overlap

Priority overlap targets by project:
- `code-smells-project`:
  - hardcoded credentials/insecure config
  - N+1 query pattern
  - missing service layer / broken layer separation
  - duplicated validation or serialization
  - magic strings/numbers
  - naming inconsistency
- `ecommerce-api-legacy`:
  - hardcoded credentials
  - weak crypto
  - missing auth on critical endpoints
  - callback hell / inline business logic
  - mutable global state
  - magic strings/naming issues
- `task-manager-api`:
  - deprecated hashing
  - hardcoded secrets/credentials
  - blocking notification flow
  - N+1 query pattern
  - duplicated serialization
  - generic exception handling / magic numbers

Rule:
- If a README-listed issue is still present in source, prefer reporting it over an equally valid supplemental issue that is not part of the manual analysis.
- If the README wording is slightly stale, map to the closest source-true issue in the same category instead of inventing an exact outdated implementation detail.
- Keep detections stack-agnostic: identify the anti-pattern from source behavior and architecture, not from language-specific assumptions alone.
- After satisfying the minimum severity distribution, prefer using available README-overlap findings to fill the report before adding extra supplemental findings.

## Snippet Quality Rules

For every finding snippet:
- include the exact line or lines that demonstrate the issue itself
- do not stop before the dangerous call, duplicated branch, magic literal, or naming inconsistency becomes visible
- prefer the smallest snippet that still proves the finding directly

Examples:
- for arbitrary SQL execution, include `cursor.execute(query)`
- for N+1, include both the loop context and the nested query line when possible
- for duplicated validation, include the repeated validation statements rather than unrelated handler setup
- for magic strings/numbers, include the literal values themselves

## Encoding Quality Rules

- Preserve source text in readable UTF-8 form.
- Do not emit mojibake such as `invÃ¡lido`, `obrigatÃ³rio` rendered as broken bytes, or similar decoding artifacts.
- If the model is unsure about a non-ASCII string, it should prefer a verified exact source excerpt over a paraphrased corrupted rendering.

## Audit Distribution Guidance

Minimum practical target for most projects:
- at least one CRITICAL or HIGH
- at least two MEDIUM
- at least two LOW

Always prioritize correctness over quotas.

## Cross-Link

Use the output structure in `references/report-template.md` for every finding.
