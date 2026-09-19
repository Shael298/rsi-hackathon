---
name: hle-exact-answer-sop
description: >
  ZQ7-DESC Required procedure for answering an expert exam question in this
  container. Gives the exact output path and answer format the grader reads, and
  what to do when the question depends on an image you cannot see.
triggers:
  - question
  - answer
  - exam
  - problem
  - solve
  - prove
  - compute
  - calculate
  - chemistry
  - engineering
  - task
  - respond
  - write
  - file
  - image
---

# Expert exam question — required procedure

ZQ7-BODY

## The one thing that must happen

Write your answer to **`/logs/agent/response.txt`** in exactly this format:

```
Explanation: <your reasoning>
Answer: <your final answer>
Confidence: <number>%
```

The line must read `Answer:` — not `Final answer`, not `Exact Answer`, not `####`.
A grader compares **the `Answer:` line alone** against a reference. Your explanation is
not scored. A correct result in the wrong format scores zero.

```sh
mkdir -p /logs/agent && cat > /logs/agent/response.txt <<'EOF'
Explanation: ...
Answer: ...
Confidence: 70%
EOF
```

## Step 1 — read the question

```sh
cat /app/instruction.md
```

## Step 2 — check whether it needs an image

**You cannot see images.** Roughly one question in four refers to one.

If the question depends on a figure, diagram, spectrum or structure you cannot read,
**do not spend turns on it.** Answer immediately from whatever the text gives you:

- **Multiple choice → always output a letter.** Never leave it blank and never say you
  cannot see the image. A guess is worth real expected points; an abstention is worth
  zero. Use any constraint in the text to eliminate options first, then pick.
- **Open-ended → give the most probable answer** for that subject and phrasing, in the
  form the question asks for.

Then write the file and stop. Never write "I cannot see the image" as the answer.

## Step 3 — solve it

Decide the **answer type before you start**: a number, an exact expression, a name, a
formula, a single letter.

- Do arithmetic in the terminal, not in your head:
  `python3 -c "import math; print(...)"`
- Check units and whether the magnitude is plausible.
- Multiple choice: eliminate, then commit. Never answer "none of the above" unless it
  is offered and you are sure.
- If you get stuck, do **not** stall or run out of turns. Narrow it down, take the most
  defensible candidate, write it. **Never finish without an answer.**

## Step 4 — the `Answer:` line

Most answers are matched near-exactly, so the form matters as much as the content:

- The answer alone. No restated question, no "approximately", no trailing sentence,
  no units unless the question asked for units.
- Multiple choice → **the letter only** (`C`), not the letter plus the option text.
- Numbers → the precision the question asked for. Keep exact form (fraction, surd,
  symbolic constant) when the question is exact; round only when told to.
- Names and technical terms → the standard spelling used in that field.
- Chemistry → the conventional notation for what was asked (formula, IUPAC name,
  structure descriptor) — whichever the question actually requested.
- Several values asked for → in the order asked, comma-separated.

## Step 5 — verify, then stop

```sh
cat /logs/agent/response.txt
```

Confirm the file exists, has all three lines, and that `Answer:` holds the answer in
the requested form. Fix it if not, then stop.
