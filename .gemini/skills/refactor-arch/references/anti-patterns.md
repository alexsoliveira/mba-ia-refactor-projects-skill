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

### 6. Tight Coupling Across Layers
- Signal: direct cross-layer calls without boundaries/abstractions.
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

## Audit Distribution Guidance

Minimum practical target for most projects:
- at least one CRITICAL or HIGH
- at least two MEDIUM
- at least two LOW

Always prioritize correctness over quotas.

## Cross-Link

Use the output structure in `references/report-template.md` for every finding.
