# AIGENTFORCE — Project Memory

## What We've Built

### Website
- **URL**: `https://tee.zo.space` (live on Zo Space)
- **DNS**: `aigentforce.io` → Cloudflare → `tee.zo.space` via redirect rule on `app.aigentforce.io`
- **Tech**: React + Tailwind CSS on Zo Space
- **Pages**: Homepage `/` | Features `/features` | Pricing `/pricing` | About `/about` | Contact `/contact` | Audit `/audit` | Chatbot `/chatbot` | Privacy `/privacy` | Terms `/terms`
- **Email**: `sales@aigentforce.io` (Namecheap cPanel) — SMTP credentials: mail.aigentforce.io:587
- **Calendly**: `https://calendly.com/osodot/ai-audit-free` — embedded on `/audit`
- **Buffer**: Connected to `ragwetee@gmail.com` — first post scheduled 27/04/2026

### AIGENTFORCE Agent Playbook
Three agents: **Sasha** (Sales), **Ava** (Audit), **Dex** (Delivery)
- Skills: `/home/workspace/Skills/aigentforce-agents/SKILL.md`
- CRM leads: `/home/workspace/data/leads.json`
- Client folders: `/home/workspace/data/clients/[name]/`
- Scripts: `/home/workspace/scripts/new-lead.sh`, `audit-booked.sh`, `delivery-complete.sh`

### LinkedIn
- Profile: `https://www.linkedin.com/in/osodot/` — Osodo. T
- Banner: `/home/workspace/Images/linkedin-banner-v2.jpg`
- Buffer: Connected, posting cadence 3x/week

### DNS / SSL — Known Issues
- `app.aigentforce.io` redirect to `tee.zo.space` — 522 error (A record points to non-routable 192.0.2.1 — workaround in progress)
- SSL error on `aigentforce.io` — Flexible SSL mode recommended
- `aigentforce.io` currently 404 — needs redirect from root to `tee.zo.space`

## Business Plan

### Target Market
UK small business owners (1–10 employees)

### Value Proposition
- Free 30-min AI audit → identify £1,000+/month in lost time
- Automations built in 48 hours
- Retainer: £50/month or Project: £297 one-time

### Revenue Goal
5 clients × £50/month = £250/month recurring minimum

### Sales Process
1. Buffer posts 3x/week → LinkedIn engagement
2. Inbound audit form or Calendly booking
3. Audit call → qualify → propose Option A/B/C
4. Delivery in 48 hours → training → sign-off

## Repos to Watch
- `msitarzewski/agency-agents` — Borrow agent persona concepts. Defer full install until 10+ clients.
- `paperclipai/paperclip` — Study org-chart + heartbeat + budget concepts. Build lightweight version with Zo automations.

## Operations Hub
**All AIGENTFORCE resources consolidated at:** `file 'AIGENTFORCE/README.md'`
- ops/ — Admin hub, agent supervision, checklists
- sales/ — Pipeline, leads, campaign tracking
- marketing/ — Content, ads, Buffer/LinkedIn
- delivery/ — Client delivery, onboarding
- technical/ — Scripts, integrations, zo.space config
- knowledge/ — Memory, blueprints, reference docs

## Contact
- Email: osodot@icloud.com | sales@aigentforce.io
- LinkedIn: Osodo. T
- Calendly: `https://calendly.com/osodot/ai-audit-free`
