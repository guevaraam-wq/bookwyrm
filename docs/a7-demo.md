# A7 two-minute demonstration

Prepare the local commit history and saved outputs before recording. Run Docker
tests beforehand; database initialization is too slow for a two-minute live demo.
Do not checkout the RED commit in the working tree or modify preserved files.

## 0:00–0:20 — Assignment and evidence

Show `git log --oneline --grep='A7-'` and explain that the original coverage commit
is reused. Open the baseline/final coverage comparison in the wiki draft.
Coverage is execution evidence, not proof that behavior is correct.

## 0:20–0:50 — RED

Open `docs/a7-red-tests.txt` and the state-based Redis regression test. Show an
assertion that the store retains exactly the highest-ranked entries up to capacity.
Explain that Redis rank endpoints are inclusive: trimming through `-N` removes
the Nth-from-last entry too, leaving only N−1 entries. At capacity 1, it removes
the sole entry. Show the A7-Red commit before the production fix.

## 0:50–1:15 — GREEN and refactor

Show the A7-Green diff changing the endpoint to `-N - 1` in all three insertion
paths. Open `docs/a7-green-tests.txt` and the full-suite result. Show the refactor
extracting one shared trim helper, with unchanged tests and another recorded run.

## 1:15–1:40 — One characterization test

Open `test_retry_item_get_does_not_schedule_task` in the import tests. It asserts
405, the POST Allow header, and that no background task is scheduled. Mention
that existing cross-user denial tests are preserved. These characterize existing
behavior; production authorization was not changed.

## 1:40–2:00 — AI mistake and limits

Show the AI Use Log and the interrupted baseline output. AI launched two test
runs against the same database; both were stopped and replaced by sequential
runs. Those interrupted outputs are not evidence of a passing or failing suite.
Also explain that the existing Redis mock encoded the faulty endpoint, while
state assertions check retained data. Finish with actual suite counts and state
that wiki publication and pushing require approval.

## Evidence to have open

- RED commit `0e41c9d42`: 13 failed, 9 passed; `docs/a7-red-tests.txt`.
- GREEN commit `06c199bc2`: 22 focused tests passed; full suite 1,395 passed,
  1 xfailed; `docs/a7-green-full-tests.txt`.
- REFACTOR commit `ef8ce9a3e`: tests unchanged; full suite 1,395 passed,
  1 xfailed; `docs/a7-refactor-full-tests.txt`.
- Characterization commit `088310410`: import lookup/method boundaries and
  deferred Redis execution; `docs/a7-characterization.md`.
- AI mistake: `docs/a7-interrupted-baseline-tests.txt` and
  `docs/a7-interrupted-characterization-tests.txt`, explicitly invalid evidence.
- Controlled line coverage comparison: 87.45% to 87.55% (+0.10 percentage points).

Optional focused replay after the demonstration (no checkout required):

```sh
./bw-dev dev pytest bookwyrm/tests/test_redis_store.py bookwyrm/tests/test_redis_store_capacity.py --no-cov -v
./bw-dev dev pytest bookwyrm/tests/views/imports/test_import.py -k test_retry_item_get_does_not_schedule_task --no-cov -v
```

The saved RED output and `git show 0e41c9d42` demonstrate the original failure;
a current-tree replay should pass because the fix is present.
