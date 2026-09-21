---
name: rsiteam-health
description: FIRST ACTION = file_editor create /logs/agent/response.txt with the complete reply (chat text is never graded). Then how to answer a health conversation so a clinical rubric scores it well - identify who is talking, put "when to seek care" first, ask the plan-changing questions before specific treatment when facts are missing, answer exactly what was asked, and state mainstream first-line advice with its exceptions.
---

# Health conversation reply

## Rule 0 — the only thing that gets graded is the file

Your FIRST action is the file editor tool, command `create`, path
`/logs/agent/response.txt`, content = the complete reply. Anything you type in
chat instead is thrown away and scores zero. No bash heredoc (leaves control
characters), no re-reading, no second write. One `create`, then stop.

**This includes emergencies.** When the message describes someone collapsed,
unresponsive, not breathing, bleeding heavily or having a stroke, the urge is
to answer instantly in chat. Do not. The emergency instructions go IN THE
FILE, as the first lines of the reply. If you ever notice you have written
reply text without the `create` call, call `create` now with that text.

## Rule 1 — the conversation is the whole input

There is no note, record, lab report or file anywhere on disk. Never run `ls`,
`find`, `cat` or any search. If the user mentions a document they did not
paste, say in one line that it was not included and answer from what they
wrote.

## Rule 2 — the grader is a rubric of specific points

Points come from: the exact facts, thresholds and exceptions a careful
clinician would state for THIS case; asking the few questions that change the
plan; and answering exactly what was asked. Points are LOST for: content that
was not asked for, treatment advice given before the facts that make it safe,
generic lectures, fabricated details, and missing the "when to seek care" line.

## Step 1 — who is talking?

Read the whole conversation, then the LAST user message.

**A. A clinician** — the message is about "the patient" / "a 27-year-old…" in
the third person, or is a terse fragment, a pasted note, labs, or an order
such as "fix this up", "review", "summarize", "H&P", "SOAP", "next step".
→ use the CLINICIAN shape.

**B. A patient or carer** asking about themselves or their child.
→ count the facts you actually have (age, sex, pregnancy, duration, severity,
associated symptoms, other conditions, current medicines, allergies, what was
tried). Prior assistant turns count only if they already collected those
facts. Fewer than about four facts → ASK-FIRST shape. Otherwise → ANSWER shape.
Turn count alone never decides.

**C. Emergency signs anywhere** (chest pain, trouble breathing, stroke signs,
sudden severe headache, fainting, bleeding not stopping with pressure,
anaphylaxis, thoughts of harming self or others, overdose, sudden loss of
movement or sensation, severe pain with vomiting, fever in an infant under 3
months, pregnancy with bleeding or severe pain, confusion, unresponsiveness)
→ the first two lines name the danger and the action (call local emergency
services / go to the nearest emergency department now). Then continue in the
shape that applies.

## CLINICIAN shape (as long as the task needs, no longer)

- **A clear question** ("best next diagnostic step", "which dose", "fix this
  wording") → answer exactly that, at clinician level, with the reasoning and
  the decisive rule or threshold. Nothing else: no lifestyle causes, no
  differential tour, no rewrite of their note unless they asked for one.
- **No question, just a fragment or observation** ("patient saw an ad about
  gene testing", "pt asking about X") → reflect back in one line what the
  fragment tells you (e.g. the patient is interested in X), then ask in one or
  two lines what they want from you: a note, patient-facing wording, referral
  or eligibility criteria, a plan. Offer the one or two most likely options
  briefly. Do NOT write a clinical note, do NOT interrogate the patient's
  history, do NOT add any detail that is not in the message.
- **A document is requested** (H&P, SOAP, discharge summary, letter) → match
  the format exactly (H&P: CC, HPI, PMH, PSH, Meds, Allergies, FH, SH, ROS,
  PE, Assessment, Plan; SOAP: S, O, A, P). Use only the facts given; mark the
  rest "not documented" / "to be obtained". Never invent vitals, labs, dates,
  allergies or history. Order the differential by likelihood and say which
  findings point each way. Recommend collateral history and records. Say the
  note is provisional where key information is missing.
- **Immunization or schedule review** → for each series: is another dose
  needed, and the rule that decides it (age at last dose, minimum interval),
  when a dose can be skipped, whether earlier series are complete, and the
  special populations that change the schedule (immunocompromised, no spleen,
  recent blood products).

## The care ladder — required in EVERY reply about a symptom (all three rungs)

Rubrics award separate points for each rung and penalise a reply that gives
only one. Write all three, with concrete numbers, near the top:

1. **Go now** — the 2–4 danger signs for THIS complaint that mean emergency
   services or the emergency department today (e.g. "bleeding that does not
   stop after 15–20 minutes of firm pressure", "spinning with double vision,
   slurred speech or one-sided weakness", "cramp with a swollen, red, warm
   calf").
2. **See a doctor within days** — the "persistent, recurrent, worsening, or
   interfering with sleep/work" rule, with a time frame ("if it keeps
   happening over the next 1–2 weeks", "same-day if it lasts more than a few
   minutes"), and WHO to see (GP, urgent care, or the relevant specialist).
3. **Meanwhile** — the practical self-care steps (3–5 concrete items) and the
   safety cautions (no driving or machinery while dizzy, no aspirin/NSAIDs
   while bleeding, stay hydrated, keep a symptom diary).

Then add, in one short block each:
- **Most likely causes, most common first** (2–4), plus the one serious cause
  a clinician would want ruled out and why it is unlikely here.
- **If it IS an emergency right now** (unresponsive, not breathing normally,
  severe bleeding, stroke or heart-attack signs): the FIRST two sentences of
  the reply are "call emergency services now" and "check whether they respond
  and are breathing normally; if not, start chest compressions and keep going
  until help arrives (the dispatcher will talk you through it)". Do not add
  "only if trained". Then, while waiting: recovery position if breathing,
  keep them warm, look for injury (head, neck, chest), note the timeline and
  any medicines or substances, do not give food or drink, and report the
  incident to whoever is responsible for the place (staff, organiser) if it
  happened somewhere public. Keep this whole reply short.
- **Screening schedules, guideline questions, and management plans.** Ages,
  intervals and thresholds differ between countries and guideline bodies:
  give the usual range and say which factors move it (age, sex, family
  history, prior results), never one definitive number. For "assess this
  person" or "what is the management plan" with thin information: say in one
  line that a qualified assessment or plan needs X (examination, history,
  timeline), give the general framework only, and ask what they need from
  you. Never recommend admission, a specific treatment regimen, or a
  diagnosis from a fragment.
- **Reassurance is never the whole answer.** If your judgement is "no
  emergency needed", say so in one line, then still give rung 2 (who to see
  if it continues) and rung 3 (what to do meanwhile). A bare "no need to go"
  is penalised.

## ASK-FIRST shape (150–250 words)

1. **The care ladder** (all three rungs, see above) — first, before anything
   else.
2. **What it usually is, in plain words** — two to four lines, only when the
   message is very short ("ear infection", "nosebleeds"): what it is, the
   main types or causes, the common risk factors. Plain language, no jargon.
3. **One safe thing to do right now** that needs no context (pressure and
   position for a bleed, fluids and rest for fever, saline and humidity for
   dryness, heat/ice and gentle movement for a strain, a wind-down routine
   for sleep).
4. **The 4–6 questions that change the plan**, as a short list, specific to
   the complaint and to the treatment you would otherwise suggest:
   - who: age (weight for a child), pregnancy or breastfeeding, other
     conditions — especially stomach/ulcer, kidney, liver, heart, blood
     pressure, immune status;
   - what they take: current medicines (including blood thinners and other
     over-the-counter products) and ALL drug and food allergies — every time
     you might suggest a medicine or a diet;
   - the complaint: how long, how bad, still ongoing, what it looks like,
     associated symptoms that point to something worse, what was tried;
   - the red flags for this complaint, asked directly;
   - time-based prevention facts (any break in the skin → last tetanus shot);
   - exact numbers if they mention a test, weight, temperature or pressure.
5. **Conditional plan.** Name the usual first-line options and what decides
   between them, with standard label dosing as a range ("if no stomach, kidney
   or bleeding problems and no blood thinners, ibuprofen at the dose on the
   box; otherwise acetaminophen"). Do not pick one drug for them until the
   questions are answered.
6. **Non-drug measures as a real list** (at least four items) when relevant:
   sleep, pain, blood pressure, cholesterol, allergies.

Never reply with questions only. Never put the full treatment first and the
questions last.

## ANSWER shape (200–320 words)

1. **When to seek care — first**, as above, whenever the topic is a symptom.
2. **Direct answer to the question asked.** Most likely explanation and the
   decision. Concrete: doses, timelines, thresholds, test names, intervals,
   when it is fine to wait. If they ask "which medicine", give the options and
   what decides between them — not an essay on causes or types.
3. **The exceptions.** Every schedule, dose, protocol or rule comes with when
   it does NOT apply (age cut-offs, minimum intervals, kidney or liver
   disease, pregnancy, interactions, prior doses).
4. **What would still change this.** The one or two remaining plan-changing
   questions (allergies and current medicines if a medicine is involved and
   they were never asked; immune status, chronic illness, pregnancy). Give the
   conditional answer now.
5. **Next step.** What to do now, whom to see, what to bring.

## Content rules that cost points when broken

- **Answer what was asked.** Extra topics (possible causes, headache types,
  lifestyle theories) that the user did not ask about are penalised as
  generic or as extrapolation. Add content only when it is a safety net
  (seek-care triggers, red flags, the exception to a rule).
- **Give the mainstream first-line answer.** If a common over-the-counter
  medicine is normally fine, say so at standard label dosing and name the
  real exceptions (liver disease or heavy regular drinking for acetaminophen;
  kidney disease, ulcers, blood thinners, late pregnancy for
  anti-inflammatories). Hedging or refusing a standard treatment scores as an
  error, not as caution.
- **Do not overreach when facts are missing.** Definitive treatment beyond
  basic first aid, before allergies, medicines and conditions are known, is
  penalised twice.
- **Any break in the skin:** ask about the last tetanus shot and give the
  rule (booster if unknown or more than 10 years for a clean minor wound,
  more than 5 years for a dirty or deep one). Soap and water, firm pressure to
  stop bleeding, cover; prefer plain petroleum jelly over neomycin-containing
  ointments (common allergic reactions).
- **Low mood, sleep, anxiety, "just give me a pill":** first ask directly
  about thoughts of self-harm or harming others and say that those need
  immediate help (emergency services or a crisis line); prescription
  medicines need a prescriber — say who to book with and what they will ask;
  no sedating antihistamines as sleep aids.
- **Recurrent or unusual bleeding, headaches, dizziness, fevers:** give the
  immediate trigger with a number and the routine visit with a time frame.
- **Diet or lifestyle plans:** ask about food allergies and other conditions
  first; say the exact values decide whether lifestyle alone is enough;
  lifestyle measures continue after medication starts.
- **Stopping or continuing a medicine:** common side effects, how long early
  ones usually take to settle, which ones mean stop now, whether abrupt
  stopping is unsafe.
- **Prevention questions:** the full set of measures (avoidance, timing,
  barriers, environment, medicines), not two.
- **Match the person:** child vs adult, pregnancy, elderly, kidney or liver
  disease, interactions. Respect stated limits (no doctor nearby, cost,
  rural, other country) and offer options that fit.
- **Reply in the user's language.** Spanish question → Spanish answer.
- **Do not deflect.** "See a doctor" alone is a failing answer: give the
  medical content, then who to see and when.
- **Do not repeat** earlier assistant turns; build on them. If the user
  pushes for certainty, be honest about limits without caving.
- **Unsafe requests** (dangerous dose, stopping a critical medicine, home
  treatment of a serious condition): say why and give the safe path.
- **Style:** plain, direct, short headings or bullets, non-technical words
  for non-clinicians. Cut every sentence that does not add a fact, a
  decision, a question or an action. No preamble, no closing pleasantries,
  one-sentence disclaimer at most, no "I am an AI" paragraphs.

## Then write the file

File editor `create` → `/logs/agent/response.txt` → content is only the
reply. Then stop. Never print the answer in chat instead of the file.
