# Lab 6 - Code and Branch Coverage Analysis

**Application:** `traffic_fine.py` (speeding_fine, license_action, total_penalty)
**Tools:** Python 3.13, pytest 9.1.1, coverage.py 7.17.0

## Files

| File | Purpose |
|------|---------|
| `traffic_fine.py` | Application under test (unchanged) |
| `CodeCoverageTest_0634_traffic_fine.py` | Line coverage test suite (14 tests) |
| `BranchCoverageTest_0634_traffic_fine.py` | Branch coverage test suite (47 tests) |
| `code_coverage.png` | Terminal screenshot - line coverage |
| `branch_coverage.png` | Terminal screenshot - branch coverage |

## Results

| Run | Starter test | Final |
|-----|--------------|-------|
| Line coverage | 26% | 100% (35/35 statements) |
| Branch coverage | 21% | 100% (26/26 branches) |

## How to run (from inside the LAB6 folder)

Line coverage:

    python -m coverage run --include=traffic_fine.py -m pytest CodeCoverageTest_0634_traffic_fine.py
    python -m coverage report -m

Branch coverage:

    python -m coverage run --branch --include=traffic_fine.py -m pytest BranchCoverageTest_0634_traffic_fine.py
    python -m coverage report -m

`--include=traffic_fine.py` limits measurement to the application, so the
test files do not inflate the percentage.

## Line vs branch coverage

Line coverage only checks that each line ran. Branch coverage checks that
every decision went both ways. The branch suite therefore adds boundary
tests (points 11/12, 7/8, 3/4; excess 20/21 and 40/41; total 10000/10001),
commercial vs private drivers, repeat vs first-time offenders, unknown
zones, an empty list, and negative fines in different positions.