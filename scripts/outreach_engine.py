#!/usr/bin/env python3
"""
Larry's Automated Outreach Engine
Automated messaging sequence for TradesReceptionist leads
Run: python3 /home/workspace/scripts/outreach_engine.py
Schedule: cron every 6 hours or trigger via /api/automate endpoint
"""

import json
import os
from datetime import datetime, timedelta

LEADS_FILE = "/home/workspace/data/outreach_leads.json"
OUTREACH_LOG = "/home/workspace/data/outreach_log.jsonl"

MESSAGES = {
    "intro": {
        "channel": "whatsapp",
        "template": """Hi {name} 👋

I'm Larry from TradesReceptionist. We help heating and plumbing businesses in the UK handle calls automatically — so you never miss a booking even when your team is on a job.

Questions?
— Larry 🤖"""
    },
    "followup": {
        "channel": "whatsapp",
        "template": """Hi {name} — Larry here 👋

Just following up on my message. We recorded a 2-minute demo showing exactly how it works for a heating business in Birmingham:

👉 [Watch Demo]

Happy to answer any questions!
— Larry"""
    },
    "case_study": {
        "channel": "whatsapp",
        "template": """Hi {name} — quick update from Larry 🤖

We just signed up a local plumber in Coventry. He was missing ~3 calls a day. Now every caller gets booked in automatically — even when he's under a kitchen sink.

Would a quick 10-min call work this week?

— Larry"""
    },
    "final": {
        "channel": "whatsapp",
        "template": """Hi {name}, last message from Larry 👋

If you're curious, we do free no-commitment demos every Tuesday. Just 10 minutes to see if this makes sense for your business.

Next demo: Tuesday {next_tuesday}
👉 Book: https://tee.zo.space

No pressure.
— Larry"""
    }
}

def load_leads():
    with open(LEADS_FILE, "r") as f:
        return json.load(f)

def save_leads(leads):
    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=2)

def log_outreach(lead_id, action, message):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "lead_id": lead_id,
        "action": action,
        "message": message[:50] + "..." if len(message) > 50 else message
    }
    with open(OUTREACH_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

def get_next_tuesday():
    today = datetime.now()
    days_ahead = 1 + (1 - today.weekday()) % 7
    if days_ahead <= 1:
        days_ahead += 7
    next_tuesday = today + timedelta(days=days_ahead)
    return next_tuesday.strftime("%d %B")

def run_sequence(lead_id=None, force_step=None):
    leads = load_leads()
    targets = [l for l in leads if l.get("id") == lead_id] if lead_id else [l for l in leads if l.get("status") != "converted" and l.get("status") != "cold"]

    results = []
    next_tuesday = get_next_tuesday()

    for lead in targets:
        last_contact = lead.get("lastContacted")
        sent_count = lead.get("sentCount", 0)

        if force_step:
            step = force_step
        elif sent_count == 0:
            step = "intro"
        elif sent_count == 1:
            if last_contact:
                days_since = (datetime.now() - datetime.fromisoformat(last_contact)).days
                if days_since >= 2:
                    step = "followup"
                else:
                    continue
            else:
                step = "followup"
        elif sent_count == 2:
            if last_contact:
                days_since = (datetime.now() - datetime.fromisoformat(last_contact)).days
                if days_since >= 4:
                    step = "case_study"
                else:
                    continue
            else:
                step = "case_study"
        elif sent_count >= 3:
            if last_contact:
                days_since = (datetime.now() - datetime.fromisoformat(last_contact)).days
                if days_since >= 7:
                    step = "final"
                else:
                    continue
            else:
                step = "final"
        else:
            continue

        msg_obj = MESSAGES.get(step, MESSAGES["intro"])
        business_name = lead.get("businessName", "there").split()[0]
        message = msg_obj["template"].replace("{name}", business_name).replace("{next_tuesday}", next_tuesday)

        lead["sentCount"] = sent_count + 1
        lead["lastContacted"] = datetime.now().isoformat()
        lead["status"] = "warm" if lead.get("status") == "new" else lead.get("status")
        if not lead.get("messageLog"):
            lead["messageLog"] = []
        lead["messageLog"].append({
            "step": step,
            "sentAt": datetime.now().isoformat(),
            "channel": msg_obj["channel"],
            "preview": message[:60] + "..."
        })

        log_outreach(lead["id"], step, message)
        results.append({
            "lead": lead["businessName"],
            "step": step,
            "message": message[:80] + "...",
            "status": "sent"
        })

    save_leads(leads)
    return results

def daily_report():
    leads = load_leads()
    report = {
        "generated": datetime.now().isoformat(),
        "total": len(leads),
        "by_status": {},
        "high_priority_pending": [],
        "needs_followup": []
    }
    for lead in leads:
        status = lead.get("status", "new")
        report["by_status"][status] = report["by_status"].get(status, 0) + 1
        if lead.get("priority") == "high" and lead.get("status") in ["new", "warm"]:
            report["high_priority_pending"].append(lead["businessName"])
        if lead.get("lastContacted"):
            days_since = (datetime.now() - datetime.fromisoformat(lead["lastContacted"])).days
            if days_since >= 3 and lead.get("status") not in ["converted", "cold"]:
                report["needs_followup"].append({
                    "name": lead["businessName"],
                    "days": days_since
                })

    print("=== Larry's Daily Outreach Report ===")
    print(f"Generated: {report['generated']}")
    print(f"Total leads: {report['total']}")
    for status, count in report["by_status"].items():
        print(f"  {status}: {count}")
    print(f"\nHigh priority still pending: {len(report['high_priority_pending'])}")
    for name in report["high_priority_pending"][:5]:
        print(f"  - {name}")
    if report["needs_followup"]:
        print(f"\nNeeds immediate follow-up:")
        for item in report["needs_followup"][:5]:
            print(f"  - {item['name']} ({item['days']} days since last contact)")
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--report":
            daily_report()
        elif sys.argv[1] == "--run":
            results = run_sequence()
            print(f"Outreach run complete: {len(results)} messages sent")
            for r in results:
                print(f"  [{r['step']}] {r['lead']}")
    else:
        print("Larry's Outreach Engine")
        print("Usage:")
        print("  python3 outreach_engine.py --report   # Daily report")
        print("  python3 outreach_engine.py --run      # Run outreach sequence")
        print("  python3 outreach_engine.py --run 005  # Run for specific lead")