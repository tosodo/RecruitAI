# AIGENTFORCE — Company Memory
> Last updated: 2026-04-29 | Status: LIVE — IRIS BUILT + OPERATIONAL

---

## 🏢 Business Overview

**What:** AI-powered automation services for UK small businesses (1-10 employees)
**Who:** Osodo. T (founder, sole operator)
**Mission:** Help UK small business owners reclaim 10+ hours/week by automating admin, outreach, and lead gen with AI
**Tagline:** "Stop Working Harder. Make AI Work Harder."
**Target:** UK small business owners struggling with manual admin and missed leads
**Phase:** Getting first paying clients — outreach running, audit loop live

---

## 🤖 ORG CHART — AI Employees

```
              ATLAS (CEO Coordinator)
                 | 15-min heartbeat
       ┌─────────┴─────────┐
       |                  |
   SASHA              LARRY
  (Sales Ops)     (Outreach Engine)
   3x daily            Daily
       |                  |
   ALEX              IRIS
(Research)      (Audit & Delivery)
   8am daily       Every 3 hours
```

### ATLAS — CEO Coordinator
- **Role:** Watches everything. Routes work. Flags issues. 15-min heartbeat.
- **Status:** Design phase — not yet deployed
- **Files:** /home/workspace/scripts/atlas_coordinator.py

### SASHA — Sales Ops Automation
- **Role:** Digests, lead alerts, pipeline tracking. Runs 3x daily (8am, 2pm, 8pm).
- **Files:** /home/workspace/scripts/sasha_alert.py
- **Automation:** FREQ=DAILY;BYHOUR=8,14,20 → combined with IRIS in one session

### LARRY — Outreach Engine
- **Role:** Finds leads, generates personalised outreach, sends via Gmail, follows up. Daily at 9am.
- **Files:**
  - /home/workspace/scripts/larry_generate.py
  - /home/workspace/scripts/larry_send_gmail.py
  - /home/workspace/scripts/larry_follow_up.py
  - /home/workspace/scripts/larry_content_generator.py
  - /home/workspace/scripts/larry_buffer_poster.py
- **Campaigns:** /home/workspace/data/campaigns/[id]/
- **Automation:** FREQ=DAILY;INTERVAL=3 (every 3 days)

### ALEX — Research & Content
- **Role:** Morning brief (8am), market intel, content angles, lead research.
- **Files:** /home/workspace/scripts/alex_supervisor.py
- **Automation:** FREQ=DAILY;BYHOUR=8 → 8am every day

### IRIS — Audit & Delivery Agent (BUILT ✅)
- **Role:** Processes audit form submissions → scores lead → sends personalised email with score + 3 opportunities → Calendly link → creates client brief for Tier A → alerts Osodo. T
- **Trigger:** Every 3 hours via automation (heartbeat). Also triggered by /api/audit-webhook
- **Scoring:** 0-100 based on budget, timeline, team size, AI tools tried, challenge alignment
- **Email flow:** Lead receives their score + top 3 AI opportunities + Calendly booking link
- **Files:**
  - /home/workspace/scripts/iris_audit.py (BUILT)
  - /home/workspace/data/audits.json
  - /home/workspace/data/client-briefs/[company-slug].md
- **Automation:** FREQ=HOURLY;INTERVAL=3 → every 3 hours

---

## ⚙️ AUTOMATED AUDIT FLOW (Iris-led) ✅ LIVE

```
Prospect fills /audit form
         ↓
/api/audit-webhook fires
         ↓
IRIS activates (every 3 hours):
  1. Saves to audits.json
  2. Scores lead (0-100)
  3. Assigns Tier A/B/C
  4. Sends email WITH:
     → Their audit score (e.g. "78/100 — You're close")
     → Top 3 AI opportunities (personalised)
     → Calendly booking link
     → "Your report" preview
         ↓
  Tier A: Client brief created + Osodo. T alerted
  Tier B/C: Nurtured via Larry
         ↓
Prospect books Calendly
         ↓
Client onboarding begins
```

---

## 📊 Lead Scoring Matrix (Iris)

| Score | Tier | Action |
|---|---|---|
| 75-100 | **A** | Immediate Calendly + client brief + Osodo alert |
| 50-74 | **B** | Nurture sequence via Larry |
| 0-49 | **C** | Content follow-up only |

---

## 💰 Pricing (Live)

| Tier | Price | What's Included |
|---|---|---|
| **Starter** | £50/month | AI chatbot + email automation |
| **Growth** | £150/month | Starter + lead generation + outreach |
| **Scale** | £297/month | Growth + dedicated AI agent + weekly strategy calls |

---

## 🌐 Infrastructure

### Domain & DNS
- **Domain:** aigentforce.io (Namecheap)
- **DNS:** Cloudflare (zone ID: 49fe9e7ec54c8ce23054b31d2e088a31)
- **Nameservers:** dion.ns.cloudflare.com + sonia.ns.cloudflare.com
- **MX:** 209.74.74.13 (mail.aigentforce.io) ✅
- **SPF:** v=spf1 include:_spf.google.com ~all ✅

### Subdomain
- **app.aigentforce.io** → Cloudflare redirect → https://tee.zo.space/$1
- **ssl mode:** Flexible

### Website (Zo Space)
- **URL:** https://tee.zo.space via app.aigentforce.io redirect
- **Pages live (24):** / /features /pricing /about /contact /audit /chatbot /privacy /terms /mission-control + API routes

### Email
- **All emails forwarded to:** ragwetee@gmail.com ✅
- **Team:** alex@, contact@, info@, support@, careers@ (all forwarding to Gmail)
- **Webmail:** Roundcube (server801.web-hosting.com:2096)
- **Gmail:** ragwetee@gmail.com connected to Zo ✅

### Calendly
- **URL:** https://calendly.com/osodot/ai-audit-free
- **Event:** "30 Minute Meeting" / "AI Audit Free"

### Buffer
- **Connected:** ragwetee@gmail.com → LinkedIn (osodot profile)
- **Session:** Active — LinkedIn posting automated

---

## 📁 Data Files

| File | Purpose |
|---|---|
| /home/workspace/data/leads.json | All leads (scored, tiered, tracked) |
| /home/workspace/data/audits.json | All audit submissions + scores |
| /home/workspace/data/campaigns/ | Larry's outreach campaigns |
| /home/workspace/data/client-briefs/ | Client onboarding docs (Tier A) |
| /home/workspace/scripts/iris_audit.py | **NEW — Audit + reply agent** |
| /home/workspace/scripts/atlas_coordinator.py | CEO agent (design phase) |
| /home/workspace/scripts/sasha_alert.py | Sales ops agent |
| /home/workspace/scripts/larry_*.py | Outreach agent scripts |
| /home/workspace/scripts/alex_supervisor.py | Research agent |
| /home/workspace/AIGENTFORCE-memory.md | This file |

---

## 🔴 Known Issues

| Issue | Impact | Workaround |
|---|---|---|
| OpenClaw can't reach server (SSH 2288 blocked) | Persistent LinkedIn agent blocked | Use Buffer for now |
| Namecheap SMTP auth failing | Can't send FROM sales@ in Gmail directly | Zo Gmail integration works |
| Zo browser resets on Cloudflare | Some tasks need manual | Use Mac agent-browser |

---

## ✅ What's Working Right Now

1. ✅ app.aigentforce.io → tee.zo.space (HTTP 301)
2. ✅ Audit form → webhook → Iris scores + replies with score + Calendly link
3. ✅ Iris sends personalised email with lead's audit score (captures email)
4. ✅ Calendly embedded on /audit page
5. ✅ SASHA + IRIS combined ops (3x daily: 8am, 2pm, 8pm)
6. ✅ Larry outreach engine (Day 1/3/7/14 emails)
7. ✅ ALEX morning brief (8am daily)
8. ✅ LinkedIn content via Buffer (automated)
9. ✅ All team emails forwarded to Gmail
10. ✅ Client briefs auto-created for Tier A leads

---

## 🎯 Current Priorities (In Order)

1. **Test the audit loop end-to-end** — fill form → receive scored reply → book call
2. **Get first paying client** — 11 leads in pipeline
3. **Scale Larry outreach** — add 20 more estate agents
4. **Deploy ATLAS** (CEO coordinator) — 15-min heartbeat supervisor
5. **Build client onboarding flow** (IRIS closes → SASHA onboards)

---

## 🧠 Strategic Decisions

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-27 | No prices on website | McKinsey psychological pricing |
| 2026-04-27 | Free audit as lead gen | Captures intent + email + qualifies |
| 2026-04-27 | £50/£150/£297 pricing | Accessible + premium |
| 2026-04-29 | Iris built — score + email reply | Closes the loop on leads automatically |
| 2026-04-29 | SASHA + IRIS combined 3x daily | One ops session = all checks done |
| 2026-04-29 | Lead gets their audit score in reply | Captures email + builds trust |

---

## 📚 References

- **McKinsey** — Problem → Solution → Proof → CTA
- **Rory Sutherland** — Behavioural economics, psychological pricing
- **Edward Bernays** — Opinion leadership, personal branding
- **Eric Siu / Singlebrain** — Fat skills, agent fleets
- **Y Combinator / Diana** — Closed-loop companies, AI as operating system
- **Paperclip AI** — Org charts, heartbeats, governance, ticket-based audit trails
- **Mastra Supervisor** — Supervisor delegates to sub-agents

---

*Update whenever a decision is made, a tool changes, or a process is refined.*
