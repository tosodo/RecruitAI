---
name: lead_scoring
description: Score inbound leads 0-100 and assign A/B/C tier. Uses audit form answers to determine urgency, budget, and fit. Sasha runs this on every new audit submission before alerting Osodo. T.
compatibility: Zo Computer, Python 3
metadata:
  author: tee.zo.computer
  category: Sales Intelligence
  display-name: Lead Scoring Engine
  tags: lead_scoring, CRM, triage, sales, AIGENTFORCE
---

# Lead Scoring Engine — Sasha's Brain

## What This Skill Does

Every time a new audit comes in, Sasha reads the answers and produces:
1. A **numerical score** (0–100)
2. A **tier** (A / B / C)
3. A **one-line summary** for Osodo. T
4. A **recommended action** (call now / nurture / archive)
5. A **psychological read** (Bernays angle)

---

## The Scoring Matrix

### Section 1: Urgency Signal (0–30 points)

| Answer | Points | Why |
|---|---|---|
| "Immediately" (timeline) | +15 | Hot iron — strike now |
| "Within a month" | +10 | Real but not desperate |
| "3–6 months" | +5 | Explorers — nurture |
| "Just browsing" | +0 | Time-waster |

| Answer | Points | Why |
|---|---|---|
| "Manually sending emails" | +8 | Clear pain point, knows the problem |
| "Spreadsheets / no system" | +6 | Chaotic — sees the gap |
| "Already using [specific AI tool]" | +4 | Sophisticated buyer |
| "Not using any AI" | +2 | Education needed first |

### Section 2: Budget Signal (0–25 points)

| Answer | Points | Why |
|---|---|---|
| "£1,000–£5,000/month" | +15 | Real budget for our tier |
| "£500–£1,000/month" | +10 | Fits our Growth tier |
| "£100–£500/month" | +5 | Starter range |
| "I'd need to see ROI first" | +2 | Price sensitive — needs case study |
| [left blank] | +0 | No budget conversation yet |

### Section 3: Company Fit (0–25 points)

| Answer | Points | Why |
|---|---|---|
| 1–5 employees | +10 | Ideal: owner-operator, fast decisions |
| 6–10 employees | +8 | Good: has admin overhead |
| 11–50 employees | +4 | Too complex, longer sales cycle |
| 50+ employees | +0 | Enterprise — not our segment |

| Industry | Points | Why |
|---|---|---|
| Estate agents | +15 | Primary target, studied |
| Restaurants/hospitality | +10 | Secondary target, lead gen fit |
| Professional services (law, accountancy) | +8 | High admin, AI-receptive |
| Retail/e-commerce | +5 | Possible but competitive |
| Other | +3 | Case by case |

### Section 4: Engagement Quality (0–20 points)

| Signal | Points | Why |
|---|---|---|
| Provided phone number | +8 | Ready to talk = ready to buy |
| Wrote >50 words in "biggest challenge" | +7 | Genuine pain, not form-filler |
| Named a specific competitor | +5 | Shopping around — we can win |
| Works in [our postcode area] | +0 | Already handled — irrelevant |

---

## TIER ASSIGNMENT

| Score | Tier | Action | SLA |
|---|---|---|---|
| **75–100** | **A — HOT** | Call within 2 hours. Email confirmation. Sasha alerts Osodo. T immediately. | 2-hour response |
| **45–74** | **B — WARM** | Email sequence. Nurture for 7 days. Book Calendly. | 24-hour response |
| **0–44** | **C — COLD** | Archive. Add to newsletter list. Re-engage in 90 days. | No outreach |

---

## OUTPUT FORMAT

After reading audit answers, Sasha produces this response:

```
## Lead Scoring — [Company Name]

**Score: [X]/100** — Tier [A|B|C]

### One-Line Summary
[Bernays-style hook that makes Osodo. T want to call immediately]

### Psychological Read
[What they actually fear based on their answers — Bernays angle]

### The Gap They Described
[What their "biggest challenge" REALLY means in operational terms]

### Recommended Opening Line
[Exact words to use on the call — Rory Sutherland energy]

### Urgency Verdict
[How desperate are they? Scale of 1-5 and why]

### Budget Reality
[What they're likely to pay based on what they said and how they said it]

### Red Flags
[Any signals this might not close — competitive quotes, no budget, wrong size]

### Next Action
CALL NOW / EMAIL SEQUENCE / ARCHIVE
```

---

## REAL EXAMPLE — Scored Live

**Audit answers:**
- Industry: Estate agent
- Team size: 4 people
- Timeline: Immediately
- Biggest challenge: "I spend 3 hours every morning replying to the same enquiries. By the time I get to the actual property viewings, I'm exhausted. My competitors seem to be everywhere online and I'm losing instructions to them."
- Budget: "I'd need to understand the ROI first"
- AI tools: Not currently using any
- Phone: Provided

**Sasha's output:**

```
## Lead Scoring — [Estate Agent, South London]

**Score: 83/100** — Tier A

### One-Line Summary
A 4-person agency losing the morning to manual enquiries while competitors ghost them online.

### Psychological Read
He knows he's being outgunned but thinks it's a resources problem, not a systems problem. 
He's not looking for another tool — he's looking for someone to tell him it's fixable.
Bernays angle: Position as the expert who "sees what others miss" — not the vendor who sells software.

### The Gap They Described
3 hrs/day × 5 days = 15 hrs/week on admin enquiries.
If 20% of those enquiries convert to instructions at average UK fee of £1,500 — 
he's sitting on £3,000+/week in potentially lost revenue.
He's not tired. He's embarrassed.

### Recommended Opening Line
"I don't think you have a staffing problem. I think you have a filter problem — 
and we fix that in 48 hours without you changing anything you do."

### Urgency Verdict
4/5 — He's already counted the hours. He mentioned competitors by implication.
He's Googling solutions right now.

### Budget Reality
£500–£1,000/month is his real range. "ROI first" = he hasn't budgeted yet.
Frame the audit as "finding your £X00/week" not "cost of software."

### Red Flags
None significant. Small agency, direct pain, owner-operated — ideal.

### Next Action
CALL NOW — target: today before 5pm
```

---

## Edge Cases

### When phone is missing but email is detailed
→ Tier B at best. They want to research before talking.
→ Send: "Thanks — I'm reviewing your answers and will send a summary + next steps within 2 hours."

### When budget is blank AND timeline is "browsing"
→ Tier C. Archive. Add to newsletter.
→ They are in research mode, not buying mode.

### When they say "we already use [specific tool]"
→ Deduct 5 points for competitive risk.
→ Ask in call: "What would need to be true for you to switch?"
→ If answer is vague, they're not a buyer yet.

### When team size is 20+
→ Tier C automatically — too complex, too slow.
→ Reply: "Our programme is designed for teams of 1–10. I'd still love to share what we found — shall I send a summary?"

---

## Sasha's Never-Do List

1. Never score a lead without reading the "biggest challenge" field word-for-word
2. Never upgrade a Tier C to Tier B just because they have a phone number
3. Never mention competitors by name in the scoring output (they might be clients)
4. Never delay a Tier A alert — if it's past 8pm, still alert but note "call tomorrow morning first"

---

## Files Sasha Reads

- `/home/workspace/data/audits.json` — source of truth for all scores
- `/home/workspace/data/leads.json` — updated after scoring

## Files Sasha Writes

- `/home/workspace/data/leads.json` — new lead entry with score, tier, and summary
- Always append, never overwrite existing lead entries
