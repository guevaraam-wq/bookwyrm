# A7 coverage provenance

The existing A7-Coverage commit **fbff6bf5e** is reused and unchanged. Its XML
`a7-coverage-before.xml` reports **12,905 / 14,776 statements = 87.34%**
(rounded by XML). It does not contain branch measurements or test outcomes, so
it alone cannot prove that the original suite passed. Its file list includes
some test helpers and package initializers.

## Verified pre-fix baseline

Command (Docker development environment):

```sh
./bw-dev dev pytest --cov-config=pyproject.toml --cov-report=term --cov-report=xml:docs/a7-baseline-verified.xml
```

Output: `a7-baseline-sequential-tests.txt`; exit status 0.
**1,377 passed, 1 xfailed, 39 warnings; 422.44 seconds.**
Coverage: **12,921 / 14,776 = 87.45%** (XML line-rate 0.8745).

This baseline has original production code at e7257dd28 and the three new
characterization tests (missing-job lookup, GET retry rejection, deferred Redis
execution), plus the existing Redis error mock corrected to use the dependency's
exception class. It precedes the RED regression tests and all production fixes.
The original eight user-added tests and all existing history are preserved.

pytest.ini is the active pytest configuration, and references a missing
.coveragerc. Explicitly choosing pyproject.toml uses its coverage.run omission
policy: `*/test*`, `celerywyrm*`, `bookwyrm/migrations/*`. Source is `bookwyrm` via
pytest's --cov option. The resulting XML contains no tests/ files. The report is
whole-package statement/line coverage, including unexecuted production modules,
not branch coverage or a targeted-file percentage. Both verified baseline and
final use this same scope. The historical XML's file scope differs, so its
87.34% is contextual rather than the controlled before/after comparison.

The earlier interrupted baseline and characterization outputs are explicitly
invalidated because AI overlapped database test runs. They are retained for the
AI log, not used for coverage or pass/fail conclusions.

Coverage does not prove correctness: it cannot establish assertion quality,
untested combinations, correct Redis semantics, or concurrent behavior.
