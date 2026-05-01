# Adopting Paperclip AI — Business Operations Platform

## What is Paperclip?

Paperclip (paperclipai/paperclip) is an open-source orchestration platform for **zero-human companies**. Where OpenClaw is an employee, Paperclip is the company — org charts, budgets, governance, goal alignment, and agent coordination.

**Key concepts:**
- **Org chart** — Agents have bosses, titles, reporting lines
- **Heartbeats** — Scheduled agent wake-ups for recurring tasks
- **Governance** — You approve hires, strategies, overrides
- **Cost control** — Monthly budgets per agent; auto-stop at limits
- **Multi-company** — One deployment, unlimited businesses
- **Portable templates** — Pre-built "Clipmart" company structures

**Stack:** Node.js 20+ · TypeScript · PostgreSQL · pnpm · Docker

---

## Two Adoption Paths

### Path A — Run Caribbean Vybez on Paperclip
### Path B — Build a Paperclip-Powered Agency (using the lead gen pipeline)

---

## Path A: Caribbean Vybez AI Company

### Org Chart

```
You (Board of Directors)
└── CEO (Claude — strategic oversight)
    ├── CMO (OpenClaw — marketing & social)
    ├── CSO (Claude — sales & outreach)
    └── CTO (Claude Code — website & tools)
```

### Agent Roles

| Agent | Role | Tasks |
|-------|------|-------|
| **CEO (Claude)** | Strategy, daily decisions, board reports | Morning briefing, priority setting |
| **CMO (OpenClaw)** | Social media, content, local SEO | 3×/week posts, review responses |
| **CSO (Claude)** | Outreach, partnerships, new channels | Weekly lead gen, partnership outreach |
| **CTO (Claude Code)** | Website, automation, tools | Update menu, fix issues, add features |

### Heartbeat Schedule

| Agent | Schedule | Task |
|-------|----------|------|
| CEO | Daily 9am | Review yesterday, set today priorities |
| CMO | Mon/Wed/Fri 10am | Post to Instagram, Facebook, TikTok |
| CSO | Tue/Thu | Process orders, follow up on leads |
| CTO | Weekly | Update menu, check website, automation health |

### Governance Rules
- New menu items → CEO approves
- Partnership deals → Board (you) approve
- Marketing spend → Max £50/month
- CTO can update website autonomously

---

## Path B: Paperclip-Powered Lead Gen Agency

This is the bigger opportunity. Use Paperclip to run the entire lead gen → website → sales pipeline as an autonomous company.

### Org Chart

```
You (Board)
└── CEO (Claude)
    ├── CMO (Claude — content & strategy)
    ├── CSO (Claude — outreach & sales)
    └── CTO (Claude Code — websites & tools)
        ├── Dev1 (Claude Code — website builds)
        └── Dev2 (Claude Code — automations)
```

### Departments & Agents

**CMO Department:**
| Agent | Role | Heartbeat |
|-------|------|-----------|
| Researcher (Claude) | Find local businesses | Daily 8am |
| Auditor (Claude) | Audit websites | On demand |
| Scorer (Claude) | Score & rank leads | After each audit batch |

**CSO Department:**
| Agent | Role | Heartbeat |
|-------|------|-----------|
| Outreach (OpenClaw) | Send personalised emails/WhatsApp | Mon–Fri 9am |
| Closer (Claude) | Follow up, handle objections | On demand |
| Demo Builder (Claude Code) | Build demo homepages | On demand |

**CTO Department:**
| Agent | Role | Heartbeat |
|-------|------|-----------|
| Web Dev (Claude Code) | Build live websites | On demand |
| Auto Dev (Claude Code) | Zapier, WhatsApp, forms | Weekly |

---

## Paperclip Features We Can Use on Zo

| Paperclip Feature | Zo Equivalent | Status |
|-------------------|-------------|--------|
| Agent orchestration | Zo Agents + OpenClaw | ✅ Available |
| Heartbeats | Zo Automations | ✅ Available |
| Org chart | Manual role assignment | ✅ Achievable |
| Budget/cost control | Per-agent limits | ⚠️ Manual |
| Multi-company | Multiple Zo workspaces | ✅ Achievable |
| Governance/approval | Rules system | ✅ Available |
| Portable templates | Skill templates | ✅ Available |
| Ticket system | Not native | ⚠️ Needs building |

---

## What Exists on Zo vs What Paperclip Adds

| Need | Zo Native | Paperclip Adds |
|------|-----------|---------------|
| Lead research | ✅ maps_search | Org-level lead pipeline |
| Website building | ✅ zo.space | Per-client website agents |
| Outreach | ✅ (manual/agent) | Automated multi-channel outreach |
| CRM/ticketing | ❌ | Full ticket system |
| Cost budgets per agent | ❌ | Agent budget limits |
| Multi-company isolation | ❌ | True company-scoped data |
| Portable company templates | ⚠️ Skills | Clipmart-style templates |
| Governance/approval gates | ❌ | Board approval workflows |

---

## Implementation Plan

### Phase 1 — Install Paperclip on Zo (1 hour)
```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev
```

### Phase 2 — Design the Company (2 hours)
- Define mission: "Run local service businesses at 80% autonomy"
- Hire agents: CEO, CMO, CSO, CTO
- Set heartbeats and budgets
- Load lead gen skills into Paperclip

### Phase 3 — Connect Zo Tools (1 hour)
- mcporter bridge → Zo MCP tools for web search, email, calendar
- Each agent gets access to the tools it needs
- Configure budgets per agent

### Phase 4 — Run the Business (ongoing)
- CEO reviews daily
- Agents work on heartbeats
- Board (you) approves major decisions

---

## What to Build on Zo Right Now

The most pragmatic first step:

```
1. Install Paperclip on Zo (self-hosted)
2. Define Caribbean Vybez as first "company"
3. Hire: Researcher + CMO + CSO + CTO
4. Give each agent Zo tool access via mcporter
5. Set heartbeat schedules
6. Board approves first outreach campaign
```

---

## Clipmart Templates to Create

Once running, package as reusable templates:

| Template | Agents | Use Case |
|----------|--------|----------|
| `local-lead-gen` | Researcher + Auditor + Scorer + Outreach | Finding local business leads |
| `website-agency` | Web Dev + Closer | Building websites for clients |
| `multi-location-restaurant` | GM + Marketing + Sales + Ops | Running restaurant chains |
| `ecommerce-agent` | Buyer + Marketer + CS + Ops | Running Shopify stores |

---

## Verdict

**For Caribbean Vybez:** Paperclip is overkill today. Better to use OpenClaw + WhatsApp automation directly.

**For the agency/model:** Paperclip is the right long-term architecture. It turns the lead gen pipeline from a manual workflow into an autonomous company.

**Recommended first step:** Install Paperclip on Zo, run Caribbean Vybez as the first company, use it to prove the model. Then scale to multiple client companies.

---

## Resources
- Repo: https://github.com/paperclipai/paperclip
- Docs: https://docs.paperclip.ing
- Quickstart: `npx paperclipai onboard --yes`
- Discord: https://discord.gg/m4HZY7xNG3
