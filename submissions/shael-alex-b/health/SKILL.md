---
name: health-consult-sop
description: >
  ZQ7-DESC Mandatory procedure for answering a health question in this container.
  Defines the required output file and the answer structure the grader scores.
  Read and follow it before writing anything; skipping it loses points.
triggers:
  - health
  - medical
  - symptom
  - patient
  - doctor
  - clinical
  - medication
  - treatment
  - diagnosis
  - question
  - answer
  - respond
  - task
  - write
  - file
---

# Health consultation — required procedure

ZQ7-BODY

You have **4 turns and 5 minutes**. That is the binding constraint. Do not explore the
filesystem, do not install anything, do not search. Write the answer first.

## Turn 1 — write the complete answer

Write your **entire final answer** to the output file named in the task instruction
(this is normally `response.txt` in your working directory). Use a heredoc so it lands
in one command:

```sh
cat > response.txt <<'EOF'
<your full answer here>
EOF
```

Plain prose with short headers. No `####` answer line, no JSON, no markdown code
fences around the answer itself.

## The answer must contain all six of these

A model grader scores your response against a checklist. Each element it cannot find
is a point lost, so cover every one, in this order:

1. **Direct answer first.** Open with the actual answer to what was asked, in one or
   two sentences. Never open with a disclaimer.
2. **The reasoning behind it.** Briefly say *why* — the mechanism, the typical cause,
   or what the evidence generally shows.
3. **Context that changes the answer.** State what you are assuming, and how the answer
   would differ for the obvious variations (age, pregnancy, existing conditions,
   current medications). If the question is genuinely ambiguous, answer the most likely
   reading *and* name the alternative — do not answer with a question alone.
4. **Red flags and when to seek care.** Name the specific symptoms that mean urgent or
   emergency care, and say plainly which level of care applies. If anything in the
   question is a genuine emergency, this moves to the very top.
5. **Concrete next steps.** What the person should actually do next, specifically
   enough to act on.
6. **Calibrated limits.** One short line on uncertainty and on seeing a clinician for
   anything individualised. One line, at the end — not a paragraph, and not at the top.

## Style rules

- Write to the reader's level. If they use lay terms, answer in lay terms; define any
  clinical term you use.
- Be specific. "See a doctor" scores nothing; "see a doctor within 24 hours if the
  fever goes above 39°C or you develop a stiff neck" scores.
- State uncertainty honestly, but still commit to a best answer. Hedging everything
  scores worse than a clear answer with a stated caveat.
- Never refuse a general health question. Answer it and add the safety framing.
- Aim for 250–500 words. Longer dilutes; shorter drops checklist items.

## Turn 2 — verify, then stop

```sh
wc -c response.txt && head -5 response.txt
```

If the file exists and is non-empty, **stop**. Do not revise, do not add turns.
If it is empty or missing, rewrite it immediately with the heredoc above.
