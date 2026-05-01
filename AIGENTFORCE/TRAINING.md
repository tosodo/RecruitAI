# AIGENTFORCE Hub — User Training Guide

**Created:** 28 Apr 2026  
**Time to complete:** ~10 minutes

---

## What Is the Hub?

A single operations centre for everything AIGENTFORCE — leads, campaigns, client delivery, technical resources, and agent supervision. Everything lives in `file 'AIGENTFORCE/'` in your workspace.

---

## Step 1 — Access the Hub

1. Open your Zo Computer workspace: [https://tee.zo.computer](https://tee.zo.computer)
2. In the **Search** bar (top left), type `AIGENTFORCE`
3. Select `AIGENTFORCE/README.md` — this is your **home base**

Or navigate directly: `/home/workspace/AIGENTFORCE/README.md`

---

## Step 2 — Understand the 6 Sections

| Section | What It's For |
|---------|--------------|
| **ops/** | Admin agent, daily checklists, error log, agent status |
| **sales/** | All leads, pipeline stages, campaign tracking |
| **marketing/** | Buffer posts, LinkedIn, ad library, content calendar |
| **delivery/** | Client onboarding, delivery checklist, pricing |
| **technical/** | Scripts, zo.space routes, integrations, DNS |
| **knowledge/** | Org chart, agent personas, business plan, references |

---

## Step 3 — Run a Daily Check (5 minutes)

Open `file 'AIGENTFORCE/ops/checklist.md'` and work through each step:

```
Daily Checklist (run before 09:30 UK)
- [ ] Run larry_follow_up.py — any follow-ups due?
- [ ] Check leads.json — new leads, score 80+?
- [ ] Check audits.json — new audit submissions?
- [ ] Scan campaigns/*/metadata.json — any replies or bounces?
- [ ] If Tier A lead found → Email osodot@icloud.com
- [ ] If warm reply → respond immediately
- [ ] If bounced → mark as bounced in leads.json
```

---

## Step 4 — Managing Leads

### Where leads live
- **CRM file:** `/home/workspace/data/leads.json`
- **Pipeline view:** `file 'AIGENTFORCE/sales/PIPELINE.md'`

### Lead Status Flow
```
new → emails_ready → contacted → replied → qualified → won/lost
                         ↘ bounced
```

### How to update a lead
1. Open `leads.json`
2. Find the lead by name/email
3. Change `status` to the appropriate stage
4. Add a `lastContactedAt` timestamp

Example — James Barrett replied:
```json
"status": "replied",
"lastContactedAt": "2026-04-28T12:00:00Z"
```

---

## Step 5 — Sending Campaign Emails

### Pre-written campaigns already exist
Campaigns are stored in `/home/workspace/data/campaigns/[id]/`:
- `email_v1.txt` — Day 1 email (already personalised)
- `follow_up_day3.txt` — Day 3 follow-up
- `follow_up_day7.txt` — Day 7 follow-up
- `follow_up_day14.txt` — Day 14 final follow-up
- `metadata.json` — Status tracker

### To manually send a Day 1 email
1. Open the campaign folder → read `email_v1.txt`
2. Copy the content and subject
3. Go to **Settings → Integrations → Gmail** and send

### Larry handles follow-ups automatically
- `python3 /home/workspace/scripts/larry_follow_up.py` sends day 3/7/14 emails **only if they're due**
- Check the output — "✅ No follow-ups due. Larry is resting." = nothing to do

---

## Step 6 — Checking Campaign Status

### Quick status scan
```bash
find /home/workspace/data/campaigns -name 'metadata.json' -exec grep -l 'replied.*true\|bounced.*true' {} \;
```

### What each status means
| Flag | Meaning | Action |
|------|---------|--------|
| `replied: true` | Lead replied — warm lead | Draft and send a response immediately |
| `bounced: true` | Email undelivered | Mark `status: bounced` in leads.json, stop all outreach |
| `sent_day1: true` | Day 1 email sent | Wait for reply or day 3 follow-up |
| `sent_day14: true` + no reply | End of sequence | Archive or mark `lost` |

---

## Step 7 — Monitoring Agents

Open `file 'AIGENTFORCE/ops/agent-log.md'`

| Agent | Job |
|-------|-----|
| **Larry** | Sends follow-up emails (day 3/7/14) |
| **Sasha** | Sales — qualifies leads, sends Tier A outreach |
| **Ava** | Audit — processes inbound audit form submissions |
| **Dex** | Delivery — manages client onboarding and delivery |

Each agent has a skill in `/home/workspace/Skills/`. The admin agent (`c6ae68d1-dc10-4da3-aa54-6ad80ac13dae`) runs daily at 09:00 UK and reads from the ops hub automatically.

---

## Step 8 — Logging Errors

Open `file 'AIGENTFORCE/ops/errors.log'`

Add entries when something breaks:
```
[2026-04-28 12:00] Description — Resolution — Status
```

---

## Common Tasks — Quick Reference

| Task | Where to go | How |
|------|-------------|-----|
| Check all leads | `sales/PIPELINE.md` or `data/leads.json` | Read |
| Send a new campaign email | `data/campaigns/[id]/email_v1.txt` | Copy → Gmail |
| Log a new lead | `data/leads.json` | Add JSON object |
| Mark lead as bounced | `data/leads.json` | Change status to `bounced` |
| Run daily check | `ops/checklist.md` | Follow steps |
| Check agent activity | `ops/agent-log.md` | Read |
| View all campaigns | `data/campaigns/` | Browse folders |
| Get technical details | `technical/README.md` | Read |

---

## Pro Tips

1. **Start every morning at `AIGENTFORCE/ops/checklist.md`** — it tells you exactly what to check and in what order
2. **Keep `PIPELINE.md` updated** — it gives you a 30-second snapshot of the entire sales pipeline
3. **Never manually send day 3/7/14 emails** — let Larry handle it via `larry_follow_up.py`
4. **When a lead replies, respond within 2 hours** — reply speed is the #1 predictor of close rate
5. **Log everything** — if something goes wrong, the error log and agent log are your first stops for debugging

---

## Need Help?

- Full agent playbook: `file 'AIGENTFORCE/knowledge/README.md'`
- Technical issues: `file 'AIGENTFORCE/technical/README.md'`
- Delivery questions: `file 'AIGENTFORCE/delivery/README.md'`
- Or ask me directly — I'm always here
