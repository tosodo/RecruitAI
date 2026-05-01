# AIGENTFORCE Sales Pipeline

## Current Pipeline (as of 28 Apr 2026)

### Tier A — Hot Leads (Score 80+, immediate attention)
| Lead | Company | Email | Score | Status | Last Action |
|------|---------|-------|-------|--------|-------------|
| James Barrett | Barrett & Associates | james@barrettproperties.co.uk | 82 | contacted | Emailed 28 Apr — awaiting reply |

### Tier B — Warm Leads (Score 45-79, nurture pipeline)
| Lead | Company | Email | Campaign ID | Status |
|------|---------|-------|-------------|--------|
| Management Team | Dexters London Bridge | info@dexters.co.uk | 6191cba9 | emails_ready |
| Management Team | Dexters Fitzrovia | info@dexters.co.uk | e01cb327 | emails_ready |
| Management Team | Dexters Tower Bridge | info@dexters.co.uk | dcf4a8e0 | emails_ready |
| Management Team | Hudsons Property | info@hudsonsproperty.co.uk | 14b1ed78 | emails_ready |
| Management Team | Circa London Southwark | info@circalondon.co.uk | 95ed7155 | emails_ready |
| Management Team | Aston Chase | info@astonchase.com | 861ad361 | emails_ready |
| Management Team | Hyde Park Estate Agents | info@hydeparkestate.co.uk | 1f5e48a8 | emails_ready |
| Management Team | Knight Frank Mayfair | mayfair@knightfrank.com | c202aa2a | emails_ready |
| Management Team | Foxtons London Bridge | londonbridge@foxtons.co.uk | 2bafe0f9 | emails_ready |
| Management Team | Winkworth West End | westend@winkworth.co.uk | ba412a78 | emails_ready |

### Tier C — Low Priority (Score <45)
| Lead | Company | Email | Score | Notes |
|------|---------|-------|-------|-------|
| Test Client | Test Business Ltd | test@example.com | 50 | From audit form — likely not real |

---

## Campaign Performance

| Campaign | Company | Day 1 | Day 3 | Day 7 | Day 14 | Replied | Bounced |
|----------|---------|-------|-------|-------|--------|---------|---------|
| 7b3d4f7e | Barrett & Associates | ✅ | ⏳ | ⏳ | ⏳ | No | No |
| 14b1ed78 | Hudsons Property | ✅ | ⏳ | ⏳ | ⏳ | No | No |
| 6191cba9 | Dexters London Bridge | ✅ | ⏳ | ⏳ | ⏳ | No | No |
| e01cb327 | Dexters Fitzrovia | ✅ | ⏳ | ⏳ | ⏳ | No | No |
| dcf4a8e0 | Dexters Tower Bridge | ✅ | ⏳ | ⏳ | ⏳ | No | No |
| 861ad361 | Aston Chase | ✅ | ⏳ | ⏳ | ⏳ | No | No |
| 1f5e48a8 | Hyde Park Estate | ✅ | ⏳ | ⏳ | ⏳ | No | No |
| c202aa2a | Knight Frank Mayfair | ✅ | ⏳ | ⏳ | ⏳ | No | No |
| 2bafe0f9 | Foxtons London Bridge | ✅ | ⏳ | ⏳ | ⏳ | No | No |
| 95ed7155 | Circa London Southwark | ✅ | ⏳ | ⏳ | ⏳ | No | No |
| ba412a78 | Winkworth West End | ✅ | ⏳ | ⏳ | ⏳ | No | No |

---

## Follow-Up Schedule

| Lead | Day 3 Email | Day 7 Email | Day 14 Email |
|------|-------------|-------------|--------------|
| James Barrett | Pending (1 May) | Pending (5 May) | Pending (12 May) |
| All Tier B | Pending | Pending | Pending |

*Day 3/7/14 emails are triggered automatically by `larry_follow_up.py`*

---

## Key Scripts

- **Outreach engine:** `file '../scripts/outreach_engine.py'`
- **Follow-up scheduler:** `file '../scripts/larry_follow_up.py'`
- **Lead generation:** `file '../scripts/larry_generate.py'`
- **Email sender (Gmail):** `file '../scripts/larry_send_gmail.py'`

---

## Scoring Criteria

| Score | Tier | Action |
|-------|------|--------|
| 80-100 | A | Email immediately, escalate to osodot@icloud.com |
| 45-79 | B | Add to campaign, send day 1/3/7/14 sequence |
| 0-44 | C | Monitor only, no active outreach |