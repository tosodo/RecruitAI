# AIGENTFORCE Operations — Admin Checklist

## Daily Checklist (run before 09:30 UK)

- [ ] Step 1: `python3 /home/workspace/scripts/larry_follow_up.py` — any follow-ups due?
- [ ] Step 2: Check leads.json — any new leads with status=new and score 80+?
- [ ] Step 3: Check audits.json — any new audit submissions?
- [ ] Step 4: Scan campaigns/*/metadata.json — any replied=true or bounced=true?
- [ ] Step 5: If Tier A lead → email osodot@icloud.com immediately
- [ ] Step 6: If warm reply → email osodot@icloud.com immediately with suggested response
- [ ] Step 7: If bounce → update leads.json status=bounced, do not contact again
- [ ] Step 8: Send daily report to osodot@icloud.com ("✅ All clear" or action required)

## Weekly Checklist (Monday)

- [ ] Review all stalled leads (no reply in 14+ days)
- [ ] Check agent logs for failures
- [ ] Review Buffer post performance
- [ ] Pipeline review — any leads to escalate or archive?
- [ ] Clean old campaign folders (archive anything 30+ days old)

## Monthly Checklist

- [ ] Full workspace audit
- [ ] Review pricing competitiveness
- [ ] Archive closed-won and closed-lost leads
- [ ] Update this checklist if processes change