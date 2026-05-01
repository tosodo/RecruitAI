# AIGENTFORCE Technical Resources

## Website

| Property | Value |
|----------|-------|
| **Live URL** | https://tee.zo.space |
| **Custom Domain** | https://aigentforce.io (redirects to tee.zo.space) |
| **DNS** | Cloudflare → tee.zo.space |
| **Tech Stack** | React + Tailwind CSS on Zo Space |

### Routes
| Path | Type | Description |
|------|------|-------------|
| `/` | Page | Homepage |
| `/features` | Page | Feature list |
| `/pricing` | Page | Pricing (£297 project / £50/mo) |
| `/about` | Page | About AIGENTFORCE |
| `/contact` | Page | Contact form |
| `/audit` | Page | Free AI audit quiz |
| `/chatbot` | Page | AI chatbot demo |
| `/privacy` | Page | Privacy policy |
| `/terms` | Page | Terms of service |
| `/api/audit-webhook` | API | Stripe webhook handler |

### Integrations
- **Stripe:** Connected — payments processed
- **Calendly:** https://calendly.com/osodot/ai-audit-free (embedded on /audit)
- **Email:** sales@aigentforce.io (Namecheap cPanel, port 587)

## Zo Space Management

```bash
# List all routes
list_space_routes()

# Check for errors
get_space_errors()

# View route code
get_space_route(path="/audit")

# Edit route
edit_space_route(path="/audit", code_edit="...", edit_instructions="...")
```

## Scripts

| Script | Purpose |
|--------|---------|
| `larry_follow_up.py` | Day 3/7/14 follow-up scheduler |
| `outreach_engine.py` | Lead generation + campaign builder |
| `larry_content_generate.py` | LinkedIn ad/copy generator |
| `larry_buffer_poster.py` | Auto-post to Buffer |
| `larry_send_gmail.py` | Gmail email sender |
| `outreach_log.md` | Outreach activity log |

## Skills

| Skill | Path | Purpose |
|-------|------|---------|
| AIGENTFORCE Agents | `file '../../Skills/aigentforce-agents/SKILL.md'` | 3-agent playbook |
| Lead Scoring | `file '../../Skills/lead_scoring/SKILL.md'` | Score 0-100, assign A/B/C |
| Outreach Generation | `file '../../Skills/outreach_generation/SKILL.md'` | Cold email + LinkedIn |
| Website Audit | `file '../../Skills/website_audit/SKILL.md'` | Analyse conversion issues |
| Skill Optimizer | `file '../../Skills/skill_optimizer/SKILL.md'` | Improve skill performance |

## External Services

| Service | Status | Notes |
|---------|--------|-------|
| Zo Space | ✅ Active | tee.zo.space |
| Gmail | ✅ Connected | sales@aigentforce.io |
| Buffer | ✅ Connected | ragwetee@gmail.com |
| Stripe | ✅ Connected | Payments active |
| LinkedIn | ✅ Active | Osodo T profile |

## DNS / Known Issues

- `app.aigentforce.io` → 522 error (A record misconfigured)
- `aigentforce.io` → 404 (redirect needed)
- SSL error on `aigentforce.io` — Flexible SSL mode in Cloudflare recommended

## API Keys (Zo Settings > Advanced)

All secrets stored in Settings > Advanced:
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `ZO_API_KEY`
- SMTP credentials for mail.aigentforce.io