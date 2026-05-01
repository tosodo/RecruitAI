# AIGENTFORCE — AI Team Org Chart

## 👤 The Boss
**Osodo. T** — Founder, decision-maker, revenue owner

---

## 🏢 The AI Team (Your Employees)

```
                    ┌─────────────────────┐
                    │   ALEX (Supervisor)  │
                    │   Reports to: Osodo │
                    └──────────┬──────────┘
                               │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
   ┌──────▼──────┐     ┌──────▼──────┐      ┌──────▼──────┐
   │ SASHA       │     │ LARRY       │      │ MARCUS      │
   │ Sales Ops   │     │ Outreach    │      │ Research    │
   │ Reports to: │     │ Reports to: │      │ Reports to: │
   │ Alex       │     │ Alex       │      │ Alex       │
   └──────┬──────┘     └──────┬──────┘      └──────┬──────┘
          │                     │                     │
          ▼                     ▼                     ▼
   Monitors leads         Sends emails          Finds new
   Alerts on Tier A       Follow-up sequences   businesses
   Scores audits          LinkedIn posts       to target
   Routes to you          Buffer posts
```

---

## 👤 ALEX — Supervisor Agent
**Reports to:** Osodo. T  
**Role:** CEO of the AI team — coordinates, briefs, escalates  
**Does:**
- Generates morning brief every 24 hours
- Routes leads to right agents
- Flags urgent items
- Tracks team performance
- Prepares Osodo. T for meetings

**Files:**
- `/home/workspace/scripts/alex_supervisor.py`

---

## 👤 SASHA — Sales Operations Agent
**Reports to:** Alex  
**Role:** Lead intelligence & alert system  
**Does:**
- Reads `leads.json` + `audits.json` every hour
- Scores new leads (Tier A/B/C)
- Alerts Osodo. T on Tier A leads
- Routes audit submissions to CRM
- Tracks pipeline status

**Trigger:** Every hour (Zo automation)  
**Never emails same lead twice** — tracked in leads.json

---

## 👤 LARRY — Outreach Agent
**Reports to:** Alex  
**Role:** Demand generation engine  
**Does:**
- Generates cold outreach campaigns from leads.json
- Sends day 1 emails via Gmail
- Schedules follow-ups (day 3/5/7)
- Generates LinkedIn content for Buffer
- Posts to Buffer (LinkedIn connected)

**Trigger:** Daily  
**Key files:**
- `larry_generate.py` — creates campaigns
- `larry_send_gmail.py` — sends emails
- `larry_follow_up.py` — runs day 3/5/7 follow-ups
- `larry_content_generate.py` — generates LinkedIn posts
- `larry_buffer_poster.py` — posts to Buffer/LinkedIn

---

## 👤 MARCUS — Research Agent
**Reports to:** Alex  
**Role:** Business discovery & target generation  
**Does:**
- Finds UK businesses (Maps search)
- Researches company details
- Adds qualified leads to leads.json
- Identifies decision-makers
- Scores leads for Larry

**Trigger:** On demand  
**Key file:** `Skills/lead_research/`

---

## 📊 Workflow Between Agents

```
Osodo. T
    ↑ (approves, decides, closes)
    │
ALEX (Morning Brief)
    │
    ├──→ SASHA ──→ [leads.json] ──→ Alert to Osodo. T
    │
    ├──→ LARRY ──→ [campaigns/] ──→ Buffer ──→ LinkedIn
    │                    │
    │                    └──→ Gmail ──→ sales@aigentforce.io
    │
    └──→ MARCUS ──→ [leads.json] (new leads)
               │
               └──→ (triggers Sasha to score & alert)
```

---

## ⚡ How It Works in Practice

**Morning:** Alex generates brief → emailed to you  
**Day:** Sasha monitors leads, alerts on Tier A  
**Day:** Larry runs campaigns, posts to LinkedIn  
**You:** Read brief → Take action on flagged items → Close clients  

**No micromanaging — trust the team**

---

## 🎯 The Compounding Effect

Every client delivered = SOP = Larry gets better
Every lead scored = data = Sasha gets smarter  
Every business found = target = Marcus sharpens  

**Your team works while you sleep. You wake up to closable leads.**

---

*Last updated: 2026-04-28 | Status: LIVE & OPERATIONAL*
