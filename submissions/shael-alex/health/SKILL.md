---
name: health-consult-sop
description: >
  ZQ7-DESC Required procedure for replying to a health conversation in this
  container. Gives the exact output path, how the rubric grader scores, and the
  three conversation types with what each one must contain. Follow it exactly.
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
  - conversation
  - reply
  - respond
  - question
  - answer
  - task
  - write
  - file
---

# Health conversation — required procedure

ZQ7-BODY

## The one thing that must happen

Write the reply to **`/logs/agent/response.txt`** — that absolute path, nothing else.
The file must contain **only the reply**: no preamble, no "Here is my response", no
markdown fences around it, no `#### answer` line.

You have **4 turns**. Write the file on turn 1. Do not explore the filesystem, do not
install anything.

```sh
mkdir -p /logs/agent && cat > /logs/agent/response.txt <<'EOF'
<the reply, and nothing else>
EOF
```

## How you are scored

A grader checks your reply against a list of independent rubric items, one at a time,
and your score is `points you earned ÷ total available points`. Three consequences,
and they drive everything below:

1. **Each item is judged separately, so coverage wins.** A reply that touches eight
   relevant things scores higher than a beautifully written one that covers three.
2. **Some items carry negative points** — being overly verbose, padding, hedging
   instead of answering, giving unsafe advice. These *subtract*. Do not inflate length
   to seem thorough; every sentence must add a distinct fact.
3. **Compound items are all-or-nothing.** If a criterion names several things, partial
   coverage scores zero for it. When you make a point, complete it.

## Step 1 — classify the conversation. This decides the shape of the reply.

Read the whole conversation, including earlier assistant turns. Then pick one:

### A. Key information is missing (the most common case)

The user's request cannot be answered safely or correctly without facts they have not
given — age, duration, severity, pregnancy, existing conditions, current medications,
what they have already tried.

**Do both of these. Doing only one loses most of the points.**
- **Ask the specific missing questions.** Not "tell me more" — name the exact facts you
  need and why each one changes the answer.
- **Give conditional guidance anyway.** Cover the likely branches: *if it's this, then
  that; if instead it's the other, then this.* Never answer with questions alone, and
  never assume a fact and answer as if it were given.

### B. There are red flags, or the user may need urgent care

**Lead with it.** State plainly what level of care is needed and how fast —
emergency services now, same-day, within a few days, routine. Name the specific
symptoms that mean escalate immediately. Do not bury this under caveats, and do not
make urgent care sound optional. Then answer the rest of the question.

### C. The user asked for a specific piece of work

A summary, a comparison, a document written for a particular reader, data interpreted,
something structured. **Follow the stated format and audience exactly** — if they asked
for a table give a table, if they asked for a patient-facing letter write it at that
reading level, if they named a length respect it. Getting the requested form right is
most of the score here.

Many conversations are more than one of these. Handle every type that applies.

## Step 2 — cover these, in a sensible order

- **Answer the actual question first.** Never open with a disclaimer.
- **Say why** — the mechanism or the usual cause, briefly.
- **State your assumptions**, and how the answer changes if they are wrong.
- **Red flags and when to seek care**, specifically enough to act on.
- **Concrete next steps** — what to do, in what order.
- **One short line on limits**, at the end. One line, never a paragraph, never at the top.

## Style

- Match the user's language and reading level. Define any clinical term you use.
- Be specific: "see a doctor" earns nothing; "see a doctor within 24 hours if the fever
  passes 39°C or a stiff neck develops" earns.
- Commit to a best answer even under uncertainty. Say what is uncertain once, plainly.
- Never refuse a general health question, and never tell the user only to see a doctor.
- Roughly 250–500 words. Shorter drops items; longer risks the verbosity penalty.

## Step 3 — verify, then stop

```sh
wc -c /logs/agent/response.txt && head -3 /logs/agent/response.txt
```

Non-empty at that exact path → **stop**. Empty or missing → rewrite immediately.
