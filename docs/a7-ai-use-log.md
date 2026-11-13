# A7 AI Use Log

Scope: local A7 work only, explicitly authorized after the repository prohibition
blocked the first attempt. AGENTS.md must remain unchanged; no push or publication.

## Work and corrections

- Inspected branch/history and reused existing coverage commit fbff6bf5e and tests
  from e7257dd28. Did not invent duplicate initial work.
- Identified that pytest.ini overrides the pytest settings in pyproject.toml and
  names a missing .coveragerc. Commands explicitly select
  `--cov-config=pyproject.toml`. The configured omissions exclude test modules,
  migrations, and celerywyrm; test helpers remain in the actual XML (see correction
  below). No branch instrumentation is enabled.
- Proposed reusing import authorization, login, and RedisStore as three components.
  Added missing lookup/method boundary coverage and deferred-pipeline coverage.
  Corrected the Redis failure mock from Python's built-in ConnectionError to
  redis.exceptions.ConnectionError, the exception the real dependency raises.
- AI mistake: launched two Docker test runs concurrently against the same test
  database. Both runs were stopped; their interrupted logs are not valid evidence.
  Subsequent default-database runs are sequential; later full runs deliberately use
  xdist with distinct worker databases. The a7-interrupted-baseline-tests.txt and
  a7-interrupted-characterization-tests.txt logs document the invalid attempts.
- Automatic review rejected a proposed temporary restoration of test files to HEAD
  because it could overwrite work. No restoration occurred. The new verification
  baseline includes the three characterization additions, before the defect test
  and before production changes. Original baseline XML remains unchanged.
- AI mistake: supplied `--noinput`, a Django management-command option that this
  pytest installation does not accept. Removed it before rerunning. That failed
  invocation produced no test or coverage result.
- Earlier AI work on the login assignment initially expected `/password-reset`
  instead of the actual `/force-password-reset` redirect. That assertion was
  corrected and the then-requested 15-test run passed. This history is separate
  from the A7 full-suite evidence.

AI assistance does not establish correctness. Review actual assertions, saved
outputs, coverage scope, and the ordered local commits. Remaining outcomes are
recorded in the final wiki draft after execution.

## Verified RED and focused GREEN

- Verified full pre-fix baseline: 1,377 passed, 1 xfailed, 39 warnings; line coverage
  12,921/14,776 = 87.45%. No baseline production changes. Saved full output/XML.
- A7-Tests commit: 088310410; A7-Red commit: 0e41c9d42.
- Added 18 fakeredis state cases covering three insertion paths, capacities 1 and
  10, and below/at/above capacity. At/above capacity, the original code loses one
  entry. The failure is an actual retained-data assertion, not a missing fixture
  or exception caused by the harness.
- Updated the earlier mocked endpoint expectation in RED because it encoded the
  bug. RED: 13 failed, 9 passed (12 state failures plus one command expectation).
  Production code was unchanged when that output and failing tests were committed.
- Only then changed three inclusive trim endpoints from -N to -N-1. Focused GREEN:
  22 passed. The complete suite and refactor results are recorded separately.
- Limitation: fakeredis emulates Redis; the regression did not use a live Redis
  server. The suite's real-service/environment dependencies still need review.

## Completion evidence

- GREEN commit 06c199bc2: complete suite 1,395 passed, 1 xfailed, 41 warnings.
- Refactor commit ef8ce9a3e: one helper owns all three trim paths. No tests changed
  from GREEN. Full rerun: 1,395 passed, 1 xfailed, 41 warnings; exit 0.
- Verified line coverage: baseline 87.45%, final 87.55%, +0.10 percentage points.
  Final statements: 12,938 / 14,778. No branch coverage measured.
- A lint attempt against the already-exited test container failed with "No such
  container"; a fresh short-lived Docker invocation was used for the final check.
- Prepared wiki Markdown, testability notes, coverage provenance, this log, and
  a two-minute demo script. No wiki publication, issue filing, push, merge, or
  force-push occurred. AGENTS.md and vulnerability-scan.json hashes are unchanged.

Final Ruff check: all checks passed; output saved in `a7-lint.txt`.

- AI reporting mistake: initially claimed all test files were excluded and that
  the historical report had a different file scope. The early path check searched
  for `/tests/` but new XML paths begin with `tests/`, so it missed helper files.
  A stricter final integrity assertion caught this before the documentation commit.
  Corrected scope: all reports include 20 test helper/package files contributing
  45 statements (43 covered), while test_*.py modules are excluded. Reported total
  counts and percentages were accurate; the scope description was corrected.
  No failed integrity assertion or lint invocation is presented as a test failure.
