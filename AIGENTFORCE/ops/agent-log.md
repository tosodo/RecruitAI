# AIGENTFORCE Operations — Agent Supervision Log

## Agent Activity Summary

| Agent | Last Run | Status | Notes |
|-------|----------|--------|-------|
| Larry (follow-ups) | 28 Apr 2026 12:00 | ✅ Resting | No follow-ups due |
| Larry (Buffer) | — | — | First post 27 Apr 2026 |
| Ava (audit webhook) | — | — | Monitoring /api/audit-webhook |
| Sasha (sales) | 28 Apr 2026 | ✅ Active | James Barrett emailed |

## Agent Scripts

| Script | Agent | Schedule |
|--------|-------|----------|
| `larry_follow_up.py` | Larry | Daily 09:00 UK |
| `larry_buffer_poster.py` | Larry | 3x/week |
| `larry_content_generate.py` | Larry | On-demand |
| `audit-booked.sh` | Ava | On webhook trigger |
| `delivery-complete.sh` | Dex | On delivery milestone |
| `new-lead.sh` | Sasha | On new lead detected |