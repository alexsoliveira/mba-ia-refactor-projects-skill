# MVC Guidelines

Purpose: define the target architecture for Phase 3 refactoring.

## Target Layers

### Model Layer
- Owns data access and persistence concerns.
- May include entity-level invariants.
- Must not read HTTP request objects.

### View/Routes Layer
- Maps endpoints and HTTP methods.
- Extracts request parameters.
- Delegates work to controllers.
- Must not implement business workflows or raw DB queries.

### Controller Layer
- Orchestrates use cases and business workflows.
- Calls model/repository/service components.
- Returns response-ready data to routes.

## Optional Service Layer

Service layer is allowed when business logic is complex.
It should sit between controllers and models/repositories.

## Dependency Direction

Routes -> Controllers -> Models/Repositories

Do not invert this direction.

## Configuration and Security

- No hardcoded secrets in source code.
- Centralize config in environment-backed settings.
- Keep sensitive internals out of health/status endpoints.

## Error Handling

- Centralized error handling is preferred.
- Keep consistent response contracts.

## Suggested Structure

```
src/
  config/
  models/
  controllers/
  routes/    # or views/
  middlewares/
  app.*
```

## Validation After Refactor

- Application boots successfully.
- Existing endpoints preserve behavior.
- Cross-layer violations found in Phase 2 are removed or reduced.

## Cross-Link

Apply concrete transformations from `references/refactoring-playbook.md`.
