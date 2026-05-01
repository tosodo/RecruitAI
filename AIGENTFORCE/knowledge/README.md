# AIGENTFORCE Knowledge Base

## Core Docs

| Document | Description |
|----------|-------------|
| `file '../AIGENTFORCE-org-chart.md'` | Full org chart with agent roles |
| `file '../AIGENTFORCE-memory.md'` | Project memory — what we've built |
| `file '../AIGenForce-AI-First-Blueprint.md'` | AI-first business blueprint |
| `file '../AIGenForce-AI-First-Business-Ideation.md'` | Original business ideation doc |
| `file '../../AGENTS.md'` | Workspace root memory — AIGENTFORCE context |

## Agent Memory

### Sasha (Sales Agent)
- Skills: Lead scoring, cold outreach, pipeline management
- Script: `larry_generate.py` + `larry_send_gmail.py`
- Memory: Check `leads.json` for current pipeline

### Larry (Outreach Agent)
- Skills: Follow-ups, Buffer posting, content generation
- Scripts: `larry_follow_up.py`, `larry_content_generate.py`, `larry_buffer_poster.py`
- Memory: Tracks `campaigns/*/metadata.json` for reply/bounce status

### Ava (Audit Agent)
- Skills: Website auditing, conversion analysis
- Script: `audit-booked.sh` when audit form submitted
- Memory: `audits.json` for incoming audit data

### Dex (Delivery Agent)
- Skills: Automation build, integration setup
- Scripts: `delivery-complete.sh` when delivery done
- Memory: Client folders in `/data/clients/[name]/`

## References

### Repos to Watch
- `msitarzewski/agency-agents` — Agent persona concepts (defer until 10+ clients)
- `paperclipai/paperclip` — Org-chart + heartbeat + budget concepts

### External Resources
- Articles: `/home/workspace/Articles/`
- Videos: YouTube channel research on AI assistants

## Business Plan

- **Target:** UK small business owners (1–10 employees)
- **Offer:** Free 30-min audit → identify £1,000+/month lost time
- **Deliverable:** Automations built in 48 hours
- **Pricing:** Retainer £50/month OR £297 project
- **Goal:** 5 clients × £50/month = £250/month minimum

## Contact Info

| Contact | Details |
|---------|---------|
| Founder | Osodo T — osodot@icloud.com |
| Sales Email | sales@aigentforce.io |
| Calendly | https://calendly.com/osodot/ai-audit-free |
| LinkedIn | https://www.linkedin.com/in/osodot/ |