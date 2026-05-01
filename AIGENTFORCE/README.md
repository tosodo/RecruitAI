# AIGENTFORCE Operations Hub

Central resource for all AIGENTFORCE project assets, agents, and operations.

## 📁 Workspace Structure

```
AIGENTFORCE/
├── ops/              ← Admin hub — org chart, agent briefs, schedules
├── sales/            ← Pipeline, leads, campaigns, outreach
├── marketing/        ← Content, ads, Buffer scheduling
├── delivery/         ← Client onboarding, playbook, delivery templates
├── technical/        ← Scripts, integrations, zo.space configuration
└── knowledge/        ← Memory, blueprints, reference docs
```

## 🏢 Org Chart

| Agent | Role | Status |
|-------|------|--------|
| **Sasha** | Sales Agent — qualifies leads, sends first emails | Active |
| **Larry** | Outreach Agent — follows up, posts to Buffer/LinkedIn | Active |
| **Ava** | Audit Agent — processes inbound audits, qualifies urgency | Active |
| **Dex** | Delivery Agent — builds automations, manages client delivery | Pending |

→ Full org chart: `file 'AIGENTFORCE-org-chart.md'`

## 🔑 Quick Access Links

### Data Files
- Leads: `file 'data/leads.json'`
- Audits: `file 'data/audits.json'`
- Campaigns: `file 'data/campaigns/'`
- Outreach log: `file 'data/outreach_log.jsonl'`

### Key Websites
- **Zo Space (live site):** https://tee.zo.space
- **AIGENTFORCE.io:** https://aigentforce.io
- **Calendly (booking):** https://calendly.com/osodot/ai-audit-free

### Scripts
- Follow-up scheduler: `file 'scripts/larry_follow_up.py'`
- Outreach engine: `file 'scripts/outreach_engine.py'`
- Content generator: `file 'scripts/larry_content_generate.py'`
- Buffer poster: `file 'scripts/larry_buffer_poster.py'`

### Skills
- AIGENTFORCE Agents: `file 'Skills/aigentforce-agents/SKILL.md'`
- Lead Scoring: `file 'Skills/lead_scoring/SKILL.md'`
- Outreach Generation: `file 'Skills/outreach_generation/SKILL.md'`
- Website Audit: `file 'Skills/website_audit/SKILL.md'`

## 📅 Daily Operations

### Morning Check (run daily)
```
python3 /home/workspace/scripts/larry_follow_up.py
# → checks leads.json, sends day 3/7/14 follow-ups if due
# → surfaces new Tier A leads
# → checks for warm replies and bounces
# → emails osodot@icloud.com with urgent actions
```

### Weekly Buffer Posts
- 3x/week to LinkedIn via Buffer
- Larry generates content automatically

## 📊 Current Pipeline

- **Tier A:** James Barrett (Barrett & Associates) — emailed 28 Apr, awaiting reply
- **Tier B:** 10 estate agents (Dexters, Hudsons, Aston Chase, etc.) — all emailed day 1, awaiting replies
- **Tier C:** 1 (Test Client) — score 50, not actioned

## 🆘 Escalation Rules

| Trigger | Action |
|---------|--------|
| Tier A lead replied | Email osodot@icloud.com immediately with reply + suggested response |
| Warm reply on any campaign | Email osodot@icloud.com immediately |
| Bounce detected | Mark lead status=bounced in leads.json, do not contact again |
| Audit score 80+ | Alert osodot@icloud.com — high-intent lead |
| Script failure | Log error, skip affected item, continue |

## 🔐 Credentials & Access

| Service | Access |
|---------|--------|
| Zo Space | https://tee.zo.space |
| Gmail (sales@aigentforce.io) | Connected via Zo |
| Buffer | Connected (ragwetee@gmail.com) |
| Stripe | Connected — payments active |
| LinkedIn | https://www.linkedin.com/in/osodot/ |

*API keys stored in Zo Settings > Advanced (Secrets)*