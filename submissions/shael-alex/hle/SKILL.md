---
name: hle-exact-answer-sop
description: >
  ZQ7-DESC Mandatory procedure for answering an expert exam question in this
  container. Defines the exact answer format the grader matches against and the
  turn budget. Read and follow it before answering; the wrong format scores zero.
triggers:
  - question
  - answer
  - exam
  - problem
  - solve
  - prove
  - compute
  - calculate
  - task
  - respond
  - write
  - file
  - image
---

# Expert exam question — required procedure

ZQ7-BODY

One question, one answer. A model grader compares your **final answer only** against a
reference answer. Your reasoning is not scored; an answer in the wrong format scores
zero even when the reasoning is right.

## Step 1 — read the question, and check for an image

```sh
cat instruction.md 2>/dev/null; cat question.txt 2>/dev/null; ls /app 2>/dev/null
```

**You cannot see images.** If the question depends on an image (`/app/image.png` or
similar) and the text alone is not sufficient, do not burn turns trying to decode it.
Reason from whatever the text does say, commit to your single best guess, write it in
the required format, and stop. A guess scores sometimes; no answer scores never.

## Step 2 — solve it

- Identify what kind of answer is wanted **before** solving: a number, an exact
  expression, a single word or name, a multiple-choice letter, a chemical formula.
- Work the problem out in your response. Use the terminal for any arithmetic rather
  than doing it in your head:

```sh
python3 -c "import math; print(...)"
```

- Check units, and check that the magnitude is plausible.
- If you get stuck, do not stall and do not run out of turns. Narrow it down, pick the
  most defensible candidate, and answer. **Never end without an answer.**

## Step 3 — output in exactly this format

Follow whatever format the task instruction specifies. If it specifies none, use:

```
Explanation: <two or three sentences, the key steps only>

Exact Answer: <the answer, and nothing else>

Confidence: <0-100>%
```

Rules for the `Exact Answer` line:

- The answer alone. No restated question, no units unless the question asked for
  units, no "approximately", no trailing sentence.
- Multiple choice → the letter only.
- A number → match the precision the question asked for. Give exact form
  (fraction, surd, symbolic constant) when the question is exact; round only when
  asked to.
- A name or term → the standard form, spelled as the field spells it.
- One answer. If the question asks for several, give them in the order asked,
  separated by commas.

## Step 4 — verify, then stop

Re-read the `Exact Answer` line against the question one last time: does it answer
*what was asked*, in *the form asked for*? Fix it if not. Then stop — do not keep
working after the answer is written.
