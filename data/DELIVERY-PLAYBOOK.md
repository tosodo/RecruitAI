# AIGENTFORCE — Client Delivery Playbook

## The 5-Phase Delivery Model

### Phase 1 — Onboarding (Day 1)
- [ ] Send welcome email FROM sales@aigentforce.io
- [ ] Create client brief: /home/workspace/data/client-briefs/[slug].md
- [ ] Set up client folder: /home/workspace/clients/[client-name]/
- [ ] Schedule discovery call (30 min)
- [ ] Create Calendly event type for client
- [ ] Add client to CRM

### Phase 2 — Discovery (Day 2-7)
- [ ] Discovery call: understand business, pain points, goals
- [ ] Complete Discovery Form: industry, team size, current tools, biggest frustrations
- [ ] Map manual workflows (what they do manually every day)
- [ ] Identify 3 quick wins (low-hanging fruit that saves 2+ hours)
- [ ] Agree on success metrics (what does "winning" look like?)

### Phase 3 — Audit & Strategy (Day 8-14)
- [ ] Run website audit (Skills/website_audit/)
- [ ] Run lead research (Skills/lead_research/)
- [ ] Identify automation opportunities (ranked by impact)
- [ ] Build 90-day AI roadmap (what gets automated when)
- [ ] Present audit report to client
- [ ] Agree scope + confirm pricing

### Phase 4 — Build & Implement (Day 15-45)
#### Week 1-2: Quick Wins
- [ ] Set up AI chatbot (Zo chatbot on their website)
- [ ] Configure email automation (auto-replies, follow-ups)
- [ ] Set up Calendly booking system
- [ ] Connect Google Workspace / email

#### Week 3-4: Core Automation
- [ ] Build lead capture form → CRM pipeline
- [ ] Set up outreach sequences (Larry-style for client)
- [ ] Configure CRM (leads.json or upgrade to proper CRM)
- [ ] Set up Buffer/LinkedIn scheduling

#### Week 5-6: Advanced
- [ ] Custom automations (specific to client's workflows)
- [ ] AI voice/phone assistant (if applicable)
- [ ] Analytics dashboard setup
- [ ] Team training session (30 min, how to use the tools)

### Phase 5 — Deliver & Grow (Ongoing)
#### Monthly Retainer (£50/£150/£297)
- [ ] Monthly performance review (email report)
- [ ] Optimise automations (based on data)
- [ ] Add new automations as business evolves
- [ ] Quarterly strategy call
- [ ] Upsell: Starter → Growth → Scale

---

## File Structure Per Client

```
/home/workspace/clients/[client-slug]/
  client-brief.md        # Discovery notes
  audit-report.md        # What we found
  roadmap.md             # 90-day plan
  automations/
    [automation-1].md    # Setup notes for each tool
    [automation-2].md
  reports/
    month-1.md
    month-2.md
  messages/
    outreach-v1.txt
    follow-up-day3.txt
    follow-up-day5.txt
```

## Pricing Delivery Checklist

### Starter (£50/month)
- AI chatbot on website
- Email auto-replies
- Calendly booking
- Basic lead capture form
- Monthly report

### Growth (£150/month)
- Everything in Starter +
- Automated outreach sequences
- LinkedIn + social scheduling
- CRM setup
- Lead scoring
- Weekly email reports
- Bi-weekly call

### Scale (£297/month)
- Everything in Growth +
- Dedicated AI agent (Marcus-style research)
- Full outreach engine
- Custom automations (unlimited)
- Daily Slack/email briefings
- Weekly strategy calls
- Quarterly business review
