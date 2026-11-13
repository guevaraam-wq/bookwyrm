# A7 testability findings

## Database and model side effects

Import views require Django users, jobs, permissions, and PostgreSQL. User creation
also schedules activity and suggestion tasks, so tests patch several task entry
points even when exercising authorization. This increases setup cost and coupling.
Keep integration tests for ORM ownership checks. To improve **Low Coupling**, move
external scheduling behind a narrow service boundary and arrange task dispatch
only after transaction commit. **Protected Variations** suggests replacing that
boundary with an in-memory recorder in unit tests, while retaining integration
coverage for the production scheduler.

## Redis and command semantics

RedisStore uses a module-level `r`, constructed from settings during import.
Command-only mocks can verify calls but cannot verify Redis's inclusive negative
rank endpoints. A client supplied to RedisStore would reduce coupling and protect
against variation between a real Redis client and a test implementation. Use
fakeredis for deterministic state assertions, and retain a small real-Redis
contract suite for differences the emulator may not reproduce. This is **Protected
Variations** at the persistence boundary and **Low Coupling** to infrastructure.
The store itself owns ranking and capacity policy (**Information Expert**).

## Global cache, time, and sessions

Login rate limiting depends on Django's global cache and current time. DummyCache
cannot characterize throttling; LoginViews overrides it with LocMemCache and clears
it before/after each test. Time patches establish expiry boundaries without sleeps.
A clock and rate-limit storage adapter would isolate policy from backend behavior
(**Protected Variations**) and reduce global-state coupling (**Low Coupling**).
LocMemCache tests do not prove cross-process atomicity or proxy configuration.

## Test execution environment

The suite needs a compatible Python/Django environment, PostgreSQL, Redis-related
configuration, and HTML validation libraries. Docker supplies those dependencies,
but concurrent default database tests interfere with each other. Run sequentially
or use deliberately isolated xdist database workers. Do not silently deselect failed
areas to make the full suite look green. Explicit coverage configuration is needed
because pytest.ini references a missing .coveragerc; pyproject.toml contains the
available coverage omission policy. No environment or architecture redesign is
part of this assignment's production fix.

The package report counts executed statements (including retained test helpers),
not successful assertions or
correctness. Mocks, missing combinations, concurrency, and emulator differences
remain limits even when line coverage is high.
