---
name: rsiteam-hle
description: Procedure for expert-level exam questions graded on the exact final answer. Rule 0 - your hidden reasoning counts toward a ~4,000-token turn limit and the server aborts long calls, so never solve the whole problem in your head - write a real best-guess answer file on the FIRST action, break the problem into small sub-steps, compute with Python, and rewrite the file whenever the answer improves.
---

# Expert question procedure

The grader reads only `/logs/agent/response.txt` and compares the `Answer:`
line to a reference. A missing file, a wrong format, or a vague answer scores
zero. Reasoning quality earns nothing on its own. A committed best guess
sometimes scores; an empty file never does.

## Rule 0 — the turn limit that kills most attempts

Everything you produce in one turn, INCLUDING your hidden reasoning, is cut
off at about 4,000 tokens, and the server aborts a call that runs longer than
a few minutes. If you try to think the whole problem through before acting,
the turn returns NOTHING (no tool call, no text), four minutes are gone, and
the environment replies "your last response did not include a function call".
Two or three such turns end the task with an empty file and a zero.

So:

- **Never solve the whole question in your head.** Decide the next small step
  in a few seconds and take it. Think in files and tool calls, not silently.
- **If the environment says your last response had no function call, you
  overthought.** Your next action must be trivial (rewrite the answer file
  with your current best guess), then continue with a smaller sub-step.
- **Anything computable goes to Python** (`python3 -c` or a short script):
  arithmetic, algebra, combinatorics, probability, matrices, series,
  simulation, unit and base conversion, date math, string and cipher
  manipulation, brute-force enumeration of small cases, testing a claimed
  complexity or grammar on a tiny program. Do not do multi-step arithmetic in
  your head. Only the standard library is guaranteed (`fractions`,
  `itertools`, `math`, `decimal`, `re`, `statistics`).

## Step 1 — FIRST action, no deliberation: write a real best guess

Use the file editor `create` command on `/logs/agent/response.txt`:

```
Explanation: <one sentence>
Answer: <your single best guess right now>
Confidence: <percent>
```

The guess must be a real candidate, never "pending", "unknown", "TBD" or a
question. Multiple choice → one letter (the most plausible). Numeric → a
number with the unit the question uses. Name / term → your best term.
Yes/no → one of them. You will overwrite it later if you improve it.

## Step 2 — pin down the answer type (part of the same first look)

- a number (with the unit the question uses, and the precision it implies),
- a closed-form expression,
- a name, term, sequence, or string,
- a multiple-choice letter (give the letter AND the option text),
- yes / no / true / false,
- a list (every item, in the order asked, separated by commas).

If the question defines its own notation or conventions, use exactly those.

## Step 3 — break the problem into 3–6 small sub-questions

Write them to `/app/plan.md` in one short tool call (under 20 lines). Then
answer ONE sub-question per turn. Each turn must end in a tool call: a Python
computation, a note appended to `/app/plan.md`, or a rewrite of the answer
file. A sub-question that would need long thought is too big: split it again
or replace it with a computation.

- Multiple choice: eliminate options one at a time with a concrete reason
  (a counterexample, a computed value, a definition). Commit to the survivor.
- Enumerate small cases by brute force to check a formula before trusting it.
- Ciphers and puzzles: code the transformation, test it on the given example,
  then apply it.
- Chemistry, physics, engineering: list every given quantity with units in
  the plan file, pick the governing equation, compute numerically in Python,
  check dimensions and order of magnitude.
- Computer science / AI: reason about the definition literally; when a claim
  can be tested with a tiny program, test it.
- Keep exact forms when the question is exact (fractions, radicals, symbolic
  constants). Round only when a decimal is requested; keep at least the
  precision the question shows.

## Step 4 — rewrite the answer file whenever the answer improves

After any sub-step that changes or confirms your answer, `create`
`/logs/agent/response.txt` again with the updated guess (same three-line
format). This costs one short turn and protects you if the task dies later.

## Step 5 — check once, commit, stop

- Re-read the question. Did you answer what was asked, not a neighbouring
  question? Every condition used? Edge cases (zero, empty, boundary)?
- Recompute the final number a second way if cheap (different formula,
  brute force on a smaller instance).
- If two candidates remain, pick the one that satisfies more of the stated
  constraints. Never hedge with "either A or B" — one answer only.
- Aim to be done within about 10 tool calls. Final write, exactly:

```
Explanation: <short reasoning, the key step>
Answer: <final answer only>
Confidence: <percent>
```

No markdown, headings, or extra lines after `Confidence`. Do not print the
answer only in chat. Do not spend remaining turns re-checking the file.
