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
pytest's --cov option. The policy excludes test_*.py modules but the resulting XML still includes
20 test helper/package files (45 statements, 43 covered), including conftest.py
and validate_html.py. This is whole-package statement/line coverage, including
unexecuted production modules and those helper files; it is not strictly
production-only, branch coverage, or a targeted-file percentage. The historical,
verified baseline, and final reports have the same helper-file contribution.
The controlled before/after comparison uses verified baseline and final; the
historical 87.34% is contextual because its test output was not recorded.

The earlier interrupted baseline and characterization outputs are explicitly
invalidated because AI overlapped database test runs. They are retained for the
AI log, not used for coverage or pass/fail conclusions.

Coverage does not prove correctness: it cannot establish assertion quality,
untested combinations, correct Redis semantics, or concurrent behavior.

## GREEN and final results

Both complete post-fix suites used three isolated pytest-xdist worker databases:

```sh
./bw-dev dev pytest -n 3 --cov-config=pyproject.toml --cov-report=term --cov-report=xml:docs/a7-green-coverage.xml
./bw-dev dev pytest -n 3 --cov-config=pyproject.toml --cov-report=term --cov-report=xml:docs/a7-final-coverage.xml
```

GREEN: 1,395 passed, 1 xfailed, 41 warnings; 231.95 seconds; exit 0.
Final/refactor: 1,395 passed, 1 xfailed, 41 warnings; 234.17 seconds; exit 0.
The tests are identical in GREEN and REFACTOR (verified with git diff).

| Stage | Covered / measured statements | Line coverage | Full-suite result |
| --- | --- | --- | --- |
| Verified pre-fix baseline | 12,921 / 14,776 | 87.45% | 1,377 passed; 1 xfailed; 39 warnings |
| GREEN | 12,936 / 14,776 | 87.55% | 1,395 passed; 1 xfailed; 41 warnings |
| Final after refactor | 12,938 / 14,778 | 87.55% | 1,395 passed; 1 xfailed; 41 warnings |

Final minus verified baseline: **+0.10 percentage points** (rounded).

The final covered count increases by 17 statements, while the denominator
increases by 2 because of the helper refactor. GREEN's 15 additional covered
statements come from the added regression paths. The baseline was sequential;
GREEN/final use the project's -n 3 coverage convention with the same suite
selection and omissions. Scheduler differences may affect order-sensitive tests;
no test failures were observed in either completed post-fix run.

Raw line-rate fields round to four decimals. Terminal whole-percent output is
87% at baseline and 88% after the fix, so use XML counts for the comparison.
No branch measurement was performed. Warnings and the expected failure are
recorded in the saved outputs, not suppressed or presented as passing tests.
