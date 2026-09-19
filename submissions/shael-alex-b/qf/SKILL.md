---
name: qf-sandbox-sop
description: >
  ZQ7-DESC Required procedure for solving a quantitative-finance task in this
  sandbox. Gives the input and output locations, how the verifier grades, and the
  completeness checklist that decides pass or fail. Read it before writing code.
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
  - json
  - compute
  - calculate
  - python
  - pandas
  - script
  - output
  - task
  - solve
  - write
  - file
---

# Quantitative finance sandbox — required procedure

ZQ7-BODY

## How you are graded

A hidden test suite reads **the files you write**, and **every check must pass** — there
is no partial credit. Your explanation and your terminal output are not scored.

That has one dominant consequence: **a missing or misnamed output file guarantees
zero.** The verifier is deliberately forgiving about presentation — CSV row order,
JSON key order, number formatting, blank vs null are all accepted — but it cannot
forgive a file that is not there. **Completeness beats polish. Always.**

Inputs are normally under `/app/data/`. Outputs normally go to `/app/output/`, which
**you may have to create**.

## Step 1 — build the output checklist before writing any code

```sh
cat instruction.md 2>/dev/null || cat /app/instruction.md
ls -la /app/data/ 2>/dev/null
mkdir -p /app/output
```

The instruction lists the required outputs exactly. Write the list down before you
start, and for each file record:

- **The exact filename** and directory, spelled exactly as the instruction spells it.
- **Every required column**, in the order given — or **every required JSON key**.
- **Units and convention**: percent vs fraction, annualised vs periodic, basis points,
  log vs simple returns, sample vs population (`ddof`). A right number in the wrong
  convention fails.

Do not start computing until that checklist exists. Keep it visible and tick it off.

## Step 2 — look at the real data

```sh
head -5 /app/data/<file>; wc -l /app/data/<file>
```

Check the delimiter (`.tsv` is tab-separated, `.csv` is comma), the real column names,
date formats, missing values, and duplicate rows. Never assume the schema.

## Step 3 — write a script

Use the standard library plus `numpy`, `scipy`, `pandas`. **There is no network:
`pip install` will fail — do not try it.** Confirm what you have, then adapt:

```sh
python3 -c "import numpy, pandas; print('ok')"
```

Put the work in `/app/solution.py` so you can re-run it after a fix, and run it with
`python3 /app/solution.py`. Guard the usual traps: align series on keys or dates rather
than position, handle empty groups and division by zero instead of emitting `NaN` or
`inf`, and apply every filter the instruction asks for — counting each excluded row
exactly once when an audit count is required.

## Step 4 — write every required file, even the imperfect ones

Work through the checklist from Step 1 in order. If one quantity is defeating you,
**still write its file** with your best computed values and move on — an approximate
value may pass a semantic check, while an absent file cannot. Never stop after the
easy outputs. Never delete or rename an output you have already written.

## Step 5 — verify against the checklist, then stop

```sh
ls -la /app/output/
python3 - <<'PY'
import json, pathlib, pandas as pd
for p in sorted(pathlib.Path("/app/output").iterdir()):
    if p.suffix == ".csv":
        df = pd.read_csv(p)
        print(p.name, df.shape, list(df.columns))
        print("   nulls:", int(df.isnull().values.sum()))
    elif p.suffix == ".json":
        print(p.name, "keys:", sorted(json.loads(p.read_text())))
PY
```

Confirm, item by item: every file on the checklist exists, every required column or key
is present and named exactly right, row counts are sensible, no unintended `NaN`/`inf`,
and values fall in a plausible range. Fix anything that fails, re-run, re-check.

When the checklist is complete, stop. Do not refactor and do not add outputs nobody
asked for.
