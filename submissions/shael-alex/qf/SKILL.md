---
name: qf-sandbox-sop
description: >
  ZQ7-DESC Mandatory procedure for solving a quantitative-finance task in this
  sandbox. Defines the output contract, the offline library set, and the
  self-check to run before finishing. Read it before writing any code.
triggers:
  - finance
  - quantitative
  - portfolio
  - option
  - pricing
  - volatility
  - returns
  - risk
  - data
  - csv
  - compute
  - calculate
  - python
  - script
  - test
  - task
  - solve
  - write
  - file
---

# Quantitative finance sandbox — required procedure

ZQ7-BODY

A hidden test suite reads the **files you write**. Nothing else is scored — not your
explanation, not what you print to the terminal. Getting the output contract right is
most of the score.

## Step 1 — extract the output contract before writing any code

```sh
cat instruction.md
ls -la
```

Write down, explicitly, before you start:

- **Every output file**: its exact name and directory.
- **Its format**: CSV (which column names, which order, is there a header?), JSON
  (which keys?), or a plain number.
- **Precision and units**: decimal places, percent vs fraction, basis points,
  annualised vs periodic. This is the most common silent failure — a correct number in
  the wrong unit scores zero.
- **Index/ordering**: sort order, date format, whether an index column is included.

If the instruction is ambiguous about format, mirror the format of the **input** data.

## Step 2 — inspect the real data before computing on it

```sh
head -5 <input-file>; wc -l <input-file>
```

Check for: missing values, non-trading days, date parsing, the column you actually
need versus the one with a similar name. Never assume the schema.

## Step 3 — write a script, do not compute in your head

Available offline: the **standard library**, plus `numpy`, `scipy`, `pandas` if the
image has them. **There is no network — `pip install` will fail. Do not attempt it.**
Check first and adapt rather than fail:

```sh
python3 -c "import numpy, pandas, scipy; print('ok')"
```

Put the work in a file (`solution.py`), not a one-liner, so you can re-run it after a
fix. Guard the maths explicitly:

- Use the sample vs population convention the task asks for (`ddof`).
- Annualise with the right period count (252 trading days, 12 months, 4 quarters) —
  and only if asked.
- Use log vs simple returns as specified; do not substitute one for the other.
- Align series on dates before any pairwise computation; never rely on positional
  alignment.
- Handle division by zero and empty windows rather than emitting `nan` or `inf`.

## Step 4 — test your own output before finishing

Write a small check and run it. This is the step that converts a near-miss into a pass:

```sh
python3 solution.py
cat <output-file>
python3 - <<'PY'
# re-read the output exactly as a grader would, and assert its shape
import pandas as pd
df = pd.read_csv("<output-file>")
print(df.columns.tolist(), df.shape)
print(df.head())
assert not df.isnull().values.any(), "output contains nulls"
PY
```

Confirm, item by item, against the contract from Step 1: file exists at the right
path, correct columns in the correct order, correct row count, no `NaN`/`inf`, values
in a plausible range, precision as specified.

## Step 5 — stop

Once the output file exists and passes your own check, stop. Do not refactor, do not
add features the task did not ask for, and do not delete or rename the output file.
