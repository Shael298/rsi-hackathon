---
name: rsiteam-qf
description: Working method for quantitative-finance sandbox tasks graded by hidden tests on output files. Rule 0 - your hidden reasoning counts toward a ~4,000-token turn limit and the server aborts long calls, so decide the next small action fast, write code in pieces of at most 80 lines, and create every output file (placeholder values) within the first few turns. Then spec, data inspection, one function per turn, and a mandatory output check.
---

# Quant-finance task method

The grader is a hidden pytest suite that reads the files you write. It checks
exact filenames, exact column names, exact JSON keys, value types, row counts,
and numbers within tolerance. Most failures are not math errors. They are a
missing file, a misspelled column, a wrong type, or a NaN where a number was
expected. Work in this order.

## 0. Two limits that silently kill tasks (read first)

**Limit 1 — thinking.** Everything you produce in one turn, INCLUDING your
hidden reasoning, is cut off at about 4,000 tokens, and the server aborts a
call that runs longer than a few minutes. A turn where you deliberate at
length returns NOTHING: no tool call, no text, four minutes gone, and the
environment replies "your last response did not include a function call".
Three such turns in a row usually end the whole task with zero files.

- Never plan the whole solution in your head. Decide the NEXT small action in
  a few seconds and take it. Think in the files, not in your head: write the
  plan to `/app/spec.md`, write code, run it, read the output.
- If the environment ever tells you your last response had no function call,
  you overthought. Your next action must be trivial (`ls /app`, `head -3` of a
  file), then continue with a smaller step than the one you were attempting.
- Anything that needs arithmetic, a formula check or a data look: run Python.
  Never compute in your head.

**Limit 2 — output size.** A `file_editor create` whose text is longer than
about 120 lines arrives truncated: the tool rejects it with `Field required:
path` or a JSON/validation error, and NOTHING is written. Retrying the same
long write fails the same way every time.

- Never put more than ~80 lines of code in one tool call. Build
  `/app/solve.py` in pieces: first `create` the file with imports, constants,
  paths and an empty `main()` (under 40 lines); then add ONE function per call
  with `str_replace` on a marker comment or `insert` at a line number, each
  piece under 80 lines; or split into `/app/load.py`, `/app/compute.py`,
  `/app/write.py` imported by a 20-line `solve.py`.
- If any tool call fails with "Field required" or "validation error", your
  write was too long. Do not repeat it. Cut it in half.
- Never paste data, long dataframes, tracebacks or logs into a message or a
  file. Print `head()`, `shape`, `dtypes`, a few numbers.

## Tools in this folder (use them; they save turns and prevent the failures above)

All live in `/harbor/skills/stbench-skill/` and run offline.

| tool | one call does |
|---|---|
| `scaffold.py` | turns a 10-line `spec.json` into `/app/solve.py` that already writes EVERY output file with the right names, columns, keys and types (placeholders). `--run` executes it once so the files exist immediately. |
| `qflib.py` | vetted formulas: `log_returns`, `simple_returns`, `annualized_vol`, `sharpe`, `max_drawdown`, `historical_var_es`, `parametric_var`, `ewma_cov`, `ewma_vol_series`, `hhi`, `turnover`, `lagged_corr` / `lead_lag_table` (lag>0 = x leads y), `fisher_z_pvalue`, `kendall_to_copula`, `bs_price`, `bs_greeks`, `bs_implied_vol`, `first_passage_prob_bm/_gbm`, `expected_first_passage_time_bm`, `simulate_gbm_paths`, `nelson_siegel`, `discount_factor`, `bootstrap_ci`, `to_jsonable`, `write_json`, `write_csv`. Each docstring states its convention; if the task defines it differently, follow the task. |
| `run.py` | runs `solve.py` and then `check_outputs.py` on the output folder in one call. |
| `check_outputs.py` | lists every output file with columns / keys / types, flags NaN, inf, empty files. |

Fast path (about 6 turns to a fully-shaped output set):

1. Write `/app/spec.json` (one short `create`): `{"output_dir": "...", "csv": {"file.csv": ["col1", "col2"]}, "json": {"file.json": {"key": "int|float|bool|str|list|object"}}}`
2. `python /harbor/skills/stbench-skill/scaffold.py /app/spec.json --run`
3. Fill `load_inputs()` (one `str_replace`), run `python /harbor/skills/stbench-skill/run.py`.
4. Replace one placeholder in `compute()` per turn, using `q.<function>` where a formula is standard; `run.py` after each.

In `solve.py` the library is already imported as `q` (`import qflib as q`). In a one-off
script: `import sys; sys.path.insert(0, "/harbor/skills/stbench-skill"); import qflib as q`.

## 1. Extract the spec (one or two turns)

Read the whole task text once. Write `/app/spec.md` (under 60 lines) with:

- **Inputs**: every input path and its format (delimiter, date column, units).
- **Outputs**: every output file, its exact path, and for CSV the exact column
  list in order, for JSON the exact key list and the type of each value
  (int / float / bool / string / list / object).
- **Method**: each computation step in the order given, with every parameter
  value stated in the text (windows, thresholds, seeds, confidence levels,
  day-count, annualization factor, which price column).

Use the output directory named in the task exactly (`/app/output/`,
`/output/`, or `./output/` relative to `/app`). Create it with
`os.makedirs(..., exist_ok=True)`.

## 2. Placeholder outputs FIRST (by turn 5 at the latest)

Before any real computation, write a short `solve.py` that creates EVERY
output file from the spec with the exact names, columns / keys and types, with
placeholder values (zeros, empty strings, `False`). Run it. Then run the
checker (step 5). A file with the right shape and rough numbers can earn
partial credit; a missing file earns zero, and if the task dies later you
still have something graded.

## 3. Look at the data (one turn)

- `head`, `dtypes`, `shape`, `isna().sum()`, min/max of dates, duplicate keys.
- Parse dates explicitly (`pd.to_datetime`), sort by date, check frequency.
  Expect dirty data: stale rows, wrong delimiters, mixed types, missing
  values, duplicate ids, amendments.
- If a params file exists, load every key from it and use every key. An
  unused parameter is usually a bug the task is testing for.

## 4. Fill in the computation, one function per turn

- Pure numpy / pandas / scipy. Fixed seed if anything is random
  (`np.random.default_rng(seed)` with the seed from the task, else 42).
- Replace one placeholder at a time: add the function, run `solve.py`, look at
  the new numbers, move on. Re-run the checker after every two or three.
- Follow the task's method literally. Where the text names a standard
  formula, use the textbook definition. Common ones:
  - log return = `ln(P_t / P_{t-1})`; simple return = `P_t / P_{t-1} - 1`.
  - annualize vol with `sqrt(252)` for daily equity data unless told otherwise.
  - sample statistics use `ddof=1` unless the text says population.
  - EWMA: `S_t = lam * S_{t-1} + (1 - lam) * outer(r_{t-1}, r_{t-1})` on raw
    (not demeaned) returns unless told to demean; use `np.outer`.
  - VaR at confidence c is a positive loss number unless the text defines sign.
  - Kendall tau to copula parameter: Gaussian/t `rho = sin(pi * tau / 2)`,
    Clayton `theta = 2 tau / (1 - tau)`, Gumbel `theta = 1 / (1 - tau)`.
  - HHI = sum of squared weights; effective number of names = 1 / HHI.
  - Turnover between two weight vectors = `0.5 * sum |w_t - w_{t-1}|` unless
    defined differently.
  - Black-Scholes, Greeks, bootstrap, Nelson-Siegel, GARCH, Kalman: implement
    from the standard closed form; check one known value by hand (in Python).
- Do not silently drop rows. When the task says filter, count what you filter
  and keep the counts for the audit / summary outputs.
- Summary fields like `date_range`, `start_date`, `num_days`, `n_obs` refer to
  the raw input data unless the text says "returns" or "after filtering".
  Returns have one row fewer than prices and start one period later.
- Write every output in one place, from one dict of results. Cast types
  explicitly: `int(...)`, `float(...)`, `bool(...)`. JSON cannot hold numpy
  types or NaN; convert first (`None` only if the task allows null).

## 5. Run the checker (mandatory, repeatedly)

```
cd /app && python solve.py
python <this skill folder>/check_outputs.py /app/output   # or the task's output dir
```

`check_outputs.py` lists every file in the output folder, prints CSV columns
and row counts, JSON keys and value types, and flags NaN / inf / empty files.
Compare its printout line by line against the **Outputs** list in `spec.md`.
Fix every mismatch. A single wrong column name fails the whole task.

## 6. Sanity-check the numbers (in Python, not in your head)

- Weights sum to 1. Probabilities in [0,1]. Vols positive. Correlations in
  [-1,1]. Dates in range. Counts are integers. Row counts equal what the
  spec implies (e.g. "one row per pair" means n choose 2 rows).
- If a summary file has `*_check_passed` style booleans, compute them from
  your own outputs; do not hardcode `true`.
- Debug / fix-the-bug tasks: run the given script first, read the numeric
  logic against the standard formula, fix all bugs, keep I/O untouched, then
  re-run and re-check.

## 7. Finish

Stop when every output file from the spec exists with the exact names,
columns, keys, and types and the checker is clean. Do not stop early because
the turn count is high; do not spend turns printing large dataframes. If
something is genuinely ambiguous, pick the most standard reading, state it in
a comment, and still write every required file.
