#!/usr/bin/env python3
"""
Larry — Outreach Campaign Generator
Reads leads from /home/workspace/data/leads.json
Generates full outreach campaigns (email + LinkedIn + follow-ups)
Saves to /home/workspace/data/campaigns/[id]/
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

LEADS_FILE = "/home/workspace/data/leads.json"
CAMPAIGNS_DIR = "/home/workspace/data/campaigns"
AUDITS_FILE = "/home/workspace/data/audits.json"

BERNAYS_TRIGGERS = {
    "authority": "Most {industry} we work with don't realise they've already lost before they answer the phone.",
    "social_proof": "Three {industry} in {location} have cut admin by 70% this quarter alone.",
    "scarcity": "We only take on {max_clients} new clients a month — we're currently full until {month}.",
    "reciprocity": "Here's the exact {audit_name} we use with clients — no strings attached.",
    "consistency": "You've clearly built something you're proud of — it deserves {x} more hours a week.",
    "liking": "I noticed {specific_observation} — that's actually quite rare in your space."
}

SUBJECT_LINES = {
    "estate_agent": [
        "The instruction you didn't get — and why it went to your competitor",
        "What happened when someone searched 'estate agent {location}' on your site",
        "I spent 90 seconds on your site. Here's what I saw.",
    ],
    "restaurant": [
        "Your restaurant's admin problem is costing you more than you think",
        "I looked at {company} on Google — here's what most owners miss",
        "The shift scheduling problem isn't solved by hiring more staff",
    ],
    "default": [
        "Quick question about {company}",
        "Saw {company} and had an idea",
        "Three things I noticed about {company}",
    ]
}

def load_leads():
    with open(LEADS_FILE, "r") as f:
        return json.load(f)

def load_audits():
    if not os.path.exists(AUDITS_FILE):
        return {}
    with open(AUDITS_FILE, "r") as f:
        data = json.load(f)
        return {a["id"]: a for a in data.get("audits", [])}

def get_industry(lead):
    """Determine industry from lead data"""
    name = lead.get("company", "").lower()
    industry = lead.get("industry", "").lower()
    
    estate_agent_keywords = ["estate", "property", "agents", "homes"]
    restaurant_keywords = ["restaurant", "cafe", "bistro", "dining", "kitchen", "grill", "pizza", "burger", "fish", "tandoor"]
    
    if any(k in name for k in estate_agent_keywords) or "estate" in industry:
        return "estate agents"
    elif any(k in name for k in restaurant_keywords) or "restaurant" in industry:
        return "restaurants"
    return "businesses"

def get_location(lead):
    """Extract location string"""
    if lead.get("location"):
        return lead["location"].split(",")[0]
    return lead.get("postcode", "your area")

def generate_opening_line(lead, trigger_type, trigger_text):
    """Generate first sentence that interrupts their day"""
    industry = get_industry(lead)
    location = get_location(lead)
    
    if trigger_type == "authority":
        return f"I noticed your site loads in about 6 seconds — most {industry} in {location} are at 3."
    elif trigger_type == "social_proof":
        return f"Three estate agents in {location} have cut admin by 70% this quarter alone."
    elif trigger_type == "liking":
        return f"I noticed {lead.get('notes', 'your website')} — that's actually quite rare in your space."
    return trigger_text

def generate_body(lead, trigger_type):
    """Generate the 3-paragraph body"""
    industry = get_industry(lead)
    location = get_location(lead)
    company = lead.get("company", "your business")
    score = lead.get("score", 0)
    
    p1 = generate_opening_line(lead, trigger_type, BERNAYS_TRIGGERS[trigger_type])
    
    p2 = f"That matters more than you'd think. Every extra second costs you roughly 12% of your enquiries. Because by the time your page loads, your prospect has already checked three competitors."
    
    if score >= 75:
        p3 = "If you're open to it, I'd love to show you the exact 3-minute audit we run for agencies — it usually surfaces one thing costing clients without them knowing."
    else:
        p3 = "Worth a quick conversation? I'll share exactly what we'd see in that time, upfront — no commitment."
    
    return p1, p2, p3

def generate_email(lead):
    """Generate complete cold email for a lead"""
    industry = get_industry(lead)
    company = lead.get("company", "")
    name = lead.get("name", "")
    first_name = name.split()[0] if name else "there"
    
    # Pick trigger based on score
    score = lead.get("score", 0)
    if score >= 80:
        trigger_type = "authority"
    elif score >= 65:
        trigger_type = "social_proof"
    else:
        trigger_type = "liking"
    
    p1, p2, p3 = generate_body(lead, trigger_type)
    
    # Subject line
    if industry == "estate_agent":
        subjects = SUBJECT_LINES["estate_agent"]
        subjects = [s.format(location=get_location(lead)) for s in subjects]
    else:
        subjects = [s.format(company=company) for s in SUBJECT_LINES["default"]]
    
    subject = subjects[0]
    alt_subjects = subjects[1:]
    
    # Email body
    body = f"""{p1}

{p2}

{p3}

Best,
Osodo
p.s. — no commitment. Just 30 minutes, and you'll know exactly where you stand."""

    return {
        "subject": subject,
        "alt_subjects": alt_subjects,
        "body": body,
        "trigger": trigger_type
    }

def generate_linkedin_message(lead):
    """Generate LinkedIn message (50-80 words)"""
    company = lead.get("company", "")
    name = lead.get("name", "")
    first_name = name.split()[0] if name else "there"
    industry = get_industry(lead)
    score = lead.get("score", 0)
    
    if industry == "estate_agent":
        msg = f"""{first_name} — quick observation.

{company} has a stronger brand than most agencies I see. But the website's not doing you any favours — it's costing you the enquiry before it even arrives.

We help small agencies in London cut admin by 70% and stop losing instructions to whoever shows up first on Rightmove.

Worth 20 minutes? Happy to share what we'd see in that time upfront — no commitment."""
    elif industry == "restaurant":
        msg = f"""{first_name} — quick observation.

{company}'s busy on weekends but the admin backlog on Monday morning is brutal. We help restaurant owners cut that by 70% — without hiring.

Worth 20 minutes?"""
    else:
        msg = f"""{first_name} — I came across {company} and had some thoughts on what could save you 10+ hours a week.

Happy to share what I see — no strings. Worth 15 minutes?"""
    
    return msg.strip()

def generate_follow_ups(lead, first_email_subject):
    """Generate 3-touch follow-up sequence"""
    name = lead.get("name", "")
    first_name = name.split()[0] if name else "there"
    
    day3 = f"""Subject: Re: {first_email_subject} — one thing worth knowing

{first_name},

One thing I've seen work for {get_industry(lead)} like yours:

The admin problem isn't fixed by hiring an VA. It's fixed by having the right system BEFORE the enquiry arrives.

I've shared the audit framework below — takes 3 minutes, tells you exactly where you're losing the most time.

Still worth a conversation?

Osodo"""

    day7 = f"""Subject: Left you alone after this — here's why

{first_name},

Fair enough if the timing's off — most people are swamped right now.

One thing I've learned: the businesses that wait 6 months to fix the admin problem end up spending 3x more when they finally do.

If that changes, I'm around.

Osodo"""
    
    day14 = f"""Subject: 6 months from now

{first_name},

I was thinking about our last conversation. In 6 months, the businesses that sorted their admin this quarter will be running at half the load they are now.

The ones who waited will still be deciding.

Whatever you decide, good luck — I mean that.

Osodo"""

    return {"day3": day3, "day7": day7, "day14": day14}

def create_campaign(lead):
    """Create a full campaign for a lead"""
    campaign_id = str(uuid4())[:8]
    company = lead.get("company", "unknown")
    lead_id = lead.get("id", "unknown")
    
    campaign_dir = Path(CAMPAIGNS_DIR) / campaign_id
    campaign_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate all content
    email = generate_email(lead)
    linkedin = generate_linkedin_message(lead)
    follow_ups = generate_follow_ups(lead, email["subject"])
    
    # Save files
    with open(campaign_dir / "email_v1.txt", "w") as f:
        f.write(f"Subject: {email['subject']}\n\n")
        f.write(email["body"])
    
    with open(campaign_dir / "linkedin_v1.txt", "w") as f:
        f.write(linkedin)
    
    with open(campaign_dir / "follow_up_day3.txt", "w") as f:
        f.write(follow_ups["day3"])
    
    with open(campaign_dir / "follow_up_day7.txt", "w") as f:
        f.write(follow_ups["day7"])
    
    with open(campaign_dir / "follow_up_day14.txt", "w") as f:
        f.write(follow_ups["day14"])
    
    # Metadata
    meta = {
        "campaign_id": campaign_id,
        "lead_id": lead_id,
        "company": company,
        "email": lead.get("email", ""),
        "subject": email["subject"],
        "trigger_used": email["trigger"],
        "status": "ready",
        "created_at": datetime.now().isoformat(),
        "sent_day1": False,
        "sent_day3": False,
        "sent_day7": False,
        "sent_day14": False,
        "replied": False,
        "bounced": False
    }
    
    with open(campaign_dir / "metadata.json", "w") as f:
        json.dump(meta, f, indent=2)
    
    return campaign_id, meta

def main():
    """Main entry point"""
    leads = load_leads()["leads"]
    audits = load_audits()
    
    # Find leads that need campaigns (tier A or B, not yet have campaign)
    needs_campaign = [
        l for l in leads
        if l.get("tier") in ["A", "B"]
        and l.get("status") in ["new", "contacted"]
        and not l.get("campaign_id")
    ]
    
    if not needs_campaign:
        print("No leads need campaigns right now.")
        print(f"Tier A/B leads without campaigns: {len(needs_campaign)}")
        return
    
    print(f"Generating campaigns for {len(needs_campaign)} leads...")
    
    created = []
    for lead in needs_campaign:
        campaign_id, meta = create_campaign(lead)
        created.append(campaign_id)
        
        # Update lead with campaign_id
        lead["campaign_id"] = campaign_id
        
        # Update status to 'emails_ready'
        lead["status"] = "emails_ready"
        
        print(f"  ✓ {meta['company']} → campaign {campaign_id}")
    
    # Save updated leads
    with open(LEADS_FILE, "w") as f:
        json.dump({"leads": leads}, f, indent=2)
    
    print(f"\nDone. Created {len(created)} campaigns:")
    for cid in created:
        print(f"  - /home/workspace/data/campaigns/{cid}/")

if __name__ == "__main__":
    main()