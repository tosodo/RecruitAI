#!/usr/bin/env python3
"""
Larry — Follow-Up Engine
Sends day 3, 7, 14 follow-up emails in sequence
Run: python3 /home/workspace/scripts/larry_follow_up.py
"""
import json
import os
from datetime import datetime
from pathlib import Path

CAMPAIGNS_DIR = Path("/home/workspace/data/campaigns")
LEADS_FILE = Path("/home/workspace/data/leads.json")
AUDITS_FILE = Path("/home/workspace/data/audits.json")

FOLLOW_UP_TEMPLATES = {
    "day3": {
        "subject": "Quick question about your website",
        "trigger": "Curiosity gap",
        "template": """Hi {contact_name},

I keep thinking about what I found when I looked at {company}.

That 6-second load time isn't just a tech issue — it affects how many people actually stay.

Quick question: do you track how many enquiries come from your website vs. Rightmove/Zoopla?

Best,
Osodo"""
    },
    "day7": {
        "subject": "No hard feelings",
        "trigger": "Permission to close",
        "template": """Hi {contact_name},

Fair enough if the timing's off — I get it. Running a business doesn't leave much room for side projects.

If you ever want to know exactly where those missing enquiries are going, just reply to this. It's a 3-minute audit, no pitch.

Best,
Osodo"""
    },
    "day14": {
        "subject": "Where will you be in 6 months?",
        "trigger": "Long game",
        "template": """Hi {contact_name},

I've been thinking about the businesses that are growing right now vs. those just surviving.

The difference is usually not the market — it's whether someone's systemised the boring stuff. The admin, the follow-ups, the "I meant to call them back."

Where do you think you'll be in 6 months if things stay the same?

Best,
Osodo

p.s. — If you'd rather not hear from me again, just reply STOP. No hard feelings."""
    }
}

def load_json(path):
    if not path.exists():
        return {} if path.name != "leads.json" else {"leads": []}
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)

def get_lead(lead_id):
    data = load_json(LEADS_FILE)
    for lead in data.get("leads", []):
        if lead.get("id") == lead_id:
            return lead
    return {}

def get_context(campaign):
    lead = get_lead(campaign.get("lead_id", ""))
    contact_name = lead.get("name", "").split()[0] if lead.get("name") else "there"
    company = campaign.get("company", "your business")
    return {"contact_name": contact_name, "company": company, "lead": lead}

def days_since(iso_date_str):
    if not iso_date_str:
        return 999
    try:
        dt = datetime.fromisoformat(iso_date_str.replace("Z", "+00:00"))
        return (datetime.now() - dt).days
    except:
        return 999

def format_body(template, context):
    return template.format(**context)

def main():
    campaigns_dir = Path("/home/workspace/data/campaigns")
    campaigns_dir.mkdir(exist_ok=True)
    
    sent_today = {}
    
    for cid_dir in campaigns_dir.iterdir():
        if not cid_dir.is_dir():
            continue
        meta_file = cid_dir / "metadata.json"
        if not meta_file.exists():
            continue
        
        meta = load_json(meta_file)
        if meta.get("status") in ("replied", "won", "lost", "bounced"):
            continue
        
        day1_at = meta.get("sent_day1_at")
        if not day1_at:
            continue
        
        for day_key, config in FOLLOW_UP_TEMPLATES.items():
            sent_flag = f"sent_{day_key}"
            if meta.get(sent_flag, False):
                continue
            
            target_day = int(day_key.replace("day", ""))
            days_elapsed = days_since(day1_at)
            
            if days_elapsed >= target_day:
                context = get_context(meta)
                body = format_body(config["template"], context)
                subject = config["subject"]
                to_email = meta.get("email", "")
                
                print(f"📧 {day_key} → {to_email}")
                
                # Use Zo Ask to send via Gmail
                import requests, os
                try:
                    resp = requests.post(
                        "https://api.zo.computer/zo/ask",
                        headers={
                            "Authorization": f"Bearer {os.environ.get('ZO_CLIENT_IDENTITY_TOKEN', '')}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "input": f"Send this email NOW. Do not ask questions.\n\nFrom: sales@aigentforce.io\nTo: {to_email}\nSubject: {subject}\n\n{body}",
                            "model_name": "vercel:minimax/minimax-m2.7"
                        },
                        timeout=90
                    )
                    result = resp.json()
                    print(f"  ✅ {day_key} sent! {str(result.get('output', ''))[:80]}")
                    
                    meta[sent_flag] = True
                    meta[f"{sent_flag}_at"] = datetime.now().isoformat()
                    meta["last_sent"] = day_key
                    save_json(meta_file, meta)
                    sent_today[to_email] = day_key
                except Exception as e:
                    print(f"  ❌ Failed: {e}")
    
    if sent_today:
        print(f"\n📬 Sent today: {len(sent_today)}")
        for email, day in sent_today.items():
            print(f"  • {email} → {day}")
    else:
        print("\n✅ No follow-ups due. Larry is resting.")

if __name__ == "__main__":
    main()
