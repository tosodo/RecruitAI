# AIGENTFORCE Client Delivery

## Delivery Playbook

Full delivery process: `file '../../data/DELIVERY-PLAYBOOK.md'`

## Delivery Timeline

```
Day 0  → Brief signed, client folder created at /data/clients/[name]/
Day 1  → Discovery call, requirements locked
Day 2  → Build begins (automations, integrations)
Day 3  → Build complete, internal testing
Day 4  → Training call with client,演示
Day 5  → Sign-off, handover docs, move to retainER monitoring
```

## Client Folder Structure

```
/data/clients/[CLIENT-NAME]/
├── brief.md              ← Project brief (created from audit answers)
├── delivery-log.md       ← What was built, decisions made
├── training-notes.md     ← How to use the system
├── sign-off.md           ← Client approval record
└── assets/               ← Logos, templates, credentials
```

## Onboarding Checklist

From `file '../../data/CLIENT-ONBOARDING.md'`:
- [ ] Client folder created
- [ ] Brief documented in `brief.md`
- [ ] Calendly booking confirmed
- [ ] Delivery timeline agreed
- [ ] First build kickoff scheduled

## Active Clients

| Client | Status | Start Date | Next Step |
|--------|--------|------------|-----------|
| No active clients yet | — | — | — |

First client onboarding will appear here once pipeline converts.

## Scripts

- Audit booked: `file '../scripts/audit-booked.sh'`
- Delivery complete: `file '../scripts/delivery-complete.sh'`
- New lead: `file '../scripts/new-lead.sh'`

## Pricing

| Package | Price | Description |
|---------|-------|-------------|
| **Project** | £297 one-time | Build + delivery in 48 hours |
| **Retainer** | £50/month | Ongoing monitoring + adjustments |