# Refactoring Playbook

Purpose: concrete Phase 3 transformations with before/after guidance.

Use these patterns to fix Phase 2 findings while preserving behavior.

## 1) Monolith Split into MVC
Before: one module mixes routes, business logic, and SQL.
After: move route mapping to `routes`, orchestration to `controllers`, SQL to `models`.

## 2) Hardcoded Secrets -> Config
Before: `SECRET_KEY = "..."` in app source.
After: read from environment-backed config module.

## 3) Raw SQL Concat -> Parameterized Queries
Before: `"... WHERE id = " + str(id)`.
After: parameter placeholders (`?`, `%s`) with bound values.

## 4) Arbitrary SQL Endpoint -> Remove/Restrict
Before: generic `/admin/query` executes any SQL body.
After: remove endpoint or secure with strict auth and query allowlist.

## 5) Business Logic in Routes -> Controller/Service
Before: route computes discounts, stock, and side effects.
After: route delegates to controller/service use case.

## 6) N+1 Queries -> Join/Batch
Before: loop with per-item SQL calls.
After: join query or batch fetch and in-memory map.

## 7) Duplicate Mapping/Validation -> Shared Utilities
Before: repeated row-to-dict and payload checks in many files.
After: common serializer/validator helpers reused across handlers.

## 8) Global Mutable State -> Scoped Dependency Management
Before: shared mutable globals for DB/session/cache.
After: scoped lifecycle or injected dependency per request/app context.

## 9) Magic Strings/Numbers -> Constants/Enums
Before: repeated status literals and numeric thresholds.
After: centralized constants/enums/config.

## 10) Deprecated APIs -> Modern Equivalents
Before: deprecated imports/methods.
After: framework-supported modern APIs and package versions.

## Execution Notes

- Apply smallest safe change set first.
- Keep endpoint contract stable.
- Validate boot and key endpoints after each major transformation group.
- After successful validation, synchronize the repository root `README.md` so challenge deliverables and evidence stay consistent with the refactored code and saved audit report.

## Cross-Link

Target design constraints are defined in `references/mvc-guidelines.md`.
