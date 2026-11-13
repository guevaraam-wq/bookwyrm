# A7: Automated Testing

Repository: [guevaraam-wq/bookwyrm](https://github.com/guevaraam-wq/bookwyrm),
branch `assignment/a7-automated-testing`. This is Markdown prepared for the wiki;
it has not been published. Commit links will resolve on GitHub only after the
local commits are approved and pushed.

## Architecture revealed by testing

BookWyrm's Django views coordinate ORM queries, forms, session/cache state,
Redis-backed ranked stores, and Celery tasks. Authorization is enforced in the
view/lookup layer: import owners can inspect and retry their jobs, while
cross-user requests raise PermissionDenied or Http404 before scheduling work.
Even basic user fixtures schedule suggestion/activity tasks, explaining why
view tests need several patches beyond the behavior under test.

RedisStore abstracts ranking and writes into pipelines, which makes isolated
characterization possible. Its global Redis client and command-level mocks also
hide persistence semantics: a test can verify the expected command while the
command itself removes the wrong data.

## Characterization of three components

Existing tests from e7257dd28 were inspected and preserved. The required
[A7-Tests commit](https://github.com/guevaraam-wq/bookwyrm/commit/088310410)
adds the missing import boundaries and deferred Redis execution case and uses
Redis's actual ConnectionError class in the error mock. It reuses existing login
coverage rather than adding duplicate assertions.

| Component | Normal behavior | Boundary behavior | Failure/error behavior |
| --- | --- | --- | --- |
| Import authorization | Owner views status and retries an item | Missing job raises Http404; GET retry returns 405 with Allow: POST and schedules nothing | Five existing cross-user denial tests prevent viewing/mutation and verify no scheduling where relevant |
| Login | Successful username/email login, 2FA and forced-reset redirects | Five failures, sixth blocked; five-minute expiry; independent client IPs | Wrong password yields form error; blocked correct password gets 429; spoofed forwarded header cannot bypass |
| RedisStore | Ranked inserts and trims for each feed | Empty destination list; deferred execution returns unexecuted pipeline | Redis execution error propagates to caller |

The verified baseline includes these characterization additions and passes the
complete collected suite: **1,377 passed, 1 xfailed**. Production code was unchanged.

## Defect and smallest fix

A local investigation found an inclusive-rank error in `RedisStore`. With capacity
N, `ZREMRANGEBYRANK store 0 -N` deletes the Nth-from-last entry too, leaving at
most N−1. At capacity 1, the first inserted entry disappears. The same endpoint
appeared in single insert, bulk insert, and store population.

**RED:** [0e41c9d42](https://github.com/guevaraam-wq/bookwyrm/commit/0e41c9d42)
adds 18 fakeredis state cases for the three paths, capacities 1/10, and input
counts below/at/above capacity. It also corrects the earlier mock expectation
that encoded the defective endpoint. Run: **13 failed, 9 passed**; 12 failures
assert missing retained entries and one asserts the corrected command endpoint.
For example, `[] != [b'1']` at capacity 1. The production file was unchanged at
this commit. [Saved RED output](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-red-tests.txt).

**GREEN:** [06c199bc2](https://github.com/guevaraam-wq/bookwyrm/commit/06c199bc2)
changes only the three trim endpoints to `-N - 1`. The focused tests pass
(**22 passed**), followed by the full suite (**1,395 passed, 1 xfailed**).
[Focused GREEN output](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-green-tests.txt),
[full GREEN output](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-green-full-tests.txt).

**REFACTOR:** [ef8ce9a3e](https://github.com/guevaraam-wq/bookwyrm/commit/ef8ce9a3e)
extracts `_trim_store` so the inclusive endpoint and capacity guard have one
owner. Each insertion path still queues trimming at the same point; empty bulk
and population paths still skip it. Tests remain unchanged from GREEN.
The final full run passes: **1,395 passed, 1 xfailed, 41 warnings** in 234.17 seconds.
[Saved final output](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-refactor-full-tests.txt).

This is a store-trimming correction, not a redesign of Redis access or a fix for
all possible capacity configurations. Unit regression tests emulate Redis with
fakeredis and use a queryset-shaped mock; they do not exercise a live Redis server.

## Testability and GRASP

| Obstacle observed | GRASP connection | Improvement outside this small fix |
| --- | --- | --- |
| User/model setup triggers tasks; import checks require PostgreSQL | Low Coupling; Protected Variations | Keep ORM authorization integration tests; put scheduling behind a service boundary with an in-memory test recorder |
| Module-global Redis client; exact-call mocks hide rank semantics | Low Coupling; Protected Variations; Information Expert | Supply a client at the persistence boundary; keep capacity/rank policy in RedisStore; combine state tests with a small real-Redis contract suite |
| Global cache, clock, and sessions in login | Low Coupling; Protected Variations | Isolate clock/storage policy; clear cache around tests and use controlled expiry time |
| Docker services and shared default test database | Low Coupling to environment | Run database suites sequentially or use xdist's distinct worker databases; document the explicit coverage configuration |

The refactor applies Information Expert by keeping trim policy in the store and
reduces duplicated responsibility. It does not claim to introduce dependency
injection or remove the infrastructure dependencies. See
[detailed testability notes](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-testability.md).

## Before-and-after coverage

| Stage | Covered / measured statements | Line coverage | Full-suite result |
| --- | --- | --- | --- |
| Verified pre-fix baseline | 12,921 / 14,776 | 87.45% | 1,377 passed; 1 xfailed; 39 warnings |
| GREEN | 12,936 / 14,776 | 87.55% | 1,395 passed; 1 xfailed; 41 warnings |
| Final after refactor | 12,938 / 14,778 | 87.55% | 1,395 passed; 1 xfailed; 41 warnings |

Final minus verified baseline: **+0.10 percentage points** (rounded).

The existing [A7-Coverage commit fbff6bf5e](https://github.com/guevaraam-wq/bookwyrm/commit/fbff6bf5e)
is reused unchanged. Its historical XML reports **87.34%** (12,905/14,776), but
includes test helper files (as do the new reports) and does not prove a full suite passed. The controlled
comparison uses a newly verified pre-fix baseline and the final run with the same
`--cov=bookwyrm --cov-config=pyproject.toml` scope. The baseline includes the three
characterization additions, before the RED tests and production changes.

`pytest.ini` is active and references a missing `.coveragerc`, so every coverage
run explicitly selects the available TOML policy, whose configured omissions are `*/test*`, `celerywyrm*`, and
`bookwyrm/migrations/*`. The actual XML excludes test_*.py modules but includes
20 test helper/package files: 45 statements, 43 covered, in both baseline and
final. Measurements are whole-package statement/line coverage, including
unexecuted production modules and those helpers, not strictly production-only;
**branch coverage was not measured**. The baseline runs sequentially; GREEN/final use the project's three
xdist workers with isolated databases and unchanged selection/omission policy.
The scheduler change is a comparison limitation; coverage is the union of
executed lines, not a timing measurement.

The increase comes from exercising additional paths, and refactoring can also
change the statement denominator. It does not prove correctness: the old trim
line was already covered while its arithmetic was wrong. Assertions, boundary
choices, emulator differences, and concurrency still matter.

[Coverage provenance and commands](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-coverage-notes.md),
[baseline output](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-baseline-sequential-tests.txt),
[baseline XML](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-baseline-verified.xml),
[final output](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-refactor-full-tests.txt),
[final XML](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-final-coverage.xml).

## Testing Evolution

1. The existing security tests protected import ownership; the original three
   Redis tests described insert commands, empty destinations, and propagated errors.
2. Characterization filled missing boundaries and reused prior login behavior
   tests. The complete pre-fix baseline established actual execution evidence.
3. Stateful Redis checks exposed an arithmetic defect the command mocks accepted.
   The RED commit records failure before the smallest production fix.
4. GREEN verified the focused reproducer and full suite. Refactoring then gave
   the corrected trim policy one implementation, with the same tests rerun.
5. Future work should add real-Redis contract checks and concurrent throttling
   tests, and reduce model/task coupling. Those are recommendations, not work
   silently added to this assignment.

## AI assistance and mistakes

AI helped inspect configuration/history, identify missing boundaries, construct
the state-based reproducer, make the small fix, and prepare reproducible logs.
The recorded outputs and ordered commits support those results; AI confidence
alone does not.

AI also launched two database test runs concurrently, causing interference. Both
were stopped and their logs marked interrupted; neither is used as suite evidence.
It suggested an unsafe temporary restoration to HEAD, which automatic review
rejected before execution. It also supplied an unsupported `--noinput` flag,
then corrected the command. A final XML audit also corrected an overclaim that
all test helpers were excluded: the first path check missed XML filenames
beginning with `tests/`. These mistakes required correction, not concealment.
The existing Redis mock's faulty endpoint expectation was another test-quality
lesson, without claiming AI originally authored that user-provided test.

[AI Use Log](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-ai-use-log.md) and [two-minute demonstration script](https://github.com/guevaraam-wq/bookwyrm/blob/assignment/a7-automated-testing/docs/a7-demo.md).

## Upstream reporting and publication

The capacity loss merits an upstream bug report because it affects shared feed
storage rather than an assignment-only fixture. Before filing, check the current
upstream implementation and duplicate issues, then include the capacity-1
reproducer, inclusive-rank explanation, three affected paths, and minimal fix.
This investigation verified the fork's code; it did not verify current upstream
HEAD or create an issue.

No wiki publication, push, merge, or force-push is authorized by this work.
Review the local commits and Markdown before approving publication or pushing.
