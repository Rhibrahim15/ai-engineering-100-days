# Day 01 â€” Baseline and Python Functions

Status: Not started

## Objective
Practise functions, basic calculations, edge cases, and automated testing.

## Exercise
Create `code/baseline.py` with a function named `analyze_numbers(numbers)`.
It must return a dictionary containing `count`, `sum`, and `average`.

Expected behaviour:
- `[2, 4, 6]` -> count 3, sum 12, average 4.0
- `[5]` -> count 1, sum 5, average 5.0
- `[]` -> count 0, sum 0, average None

Use Python built-ins only. Handle the empty list without crashing.

Create `code/test_baseline.py` with at least four automated tests:
the three cases above and one additional useful case.

## Run the tests
From the repository root, run:

`python -m unittest discover -s day01/code -p "test_*.py" -v`

## Evidence required
- Implementation
- At least four tests
- Test output
- A short explanation of the empty-list edge case

Do not mark this day complete until the implementation and tests have
been reviewed.
