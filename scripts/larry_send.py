#!/usr/bin/env python3
"""
Larry — Email Sender
Reads campaigns from /home/workspace/data/campaigns/
Sends via Gmail (ragwetee@gmail.com → FROM sales@aigentforce.io)
Updates campaign metadata with sent status
"""

import json
import os
from datetime import datetime
from pathlib import Path
from random import choice

CAMPAIGNS_DIR = "/home/workspace/data/campaigns"
LEADS_FILE = "/home/workspace/data/leads.json"

# Signatures to rotate
SIGNATURES = [
    "Best,\nOsodo. T\nAIGENTFORCE\nStop Working Harder. Make AI Work Harder.",
    "Osodo. T\nFounder, AIGENTFORCE\nwww.aigentforce.io",
    "Osodo\nAIGENTFORCE | AI Automation for UK Small Businesses",
]

def get_lead(lead_id):
    with open(LEADS_FILE) as f:
        return next((l for l in json.load(f)["leads"] if l["id"] == lead_id), None)

def load_campaign(campaign_id):
    meta_path = Path(CAMPAIGNS_DIR) / campaign_id / "metadata.json"
    if not meta_path.exists():
        return None
    with open(meta_path) as f:
        return json.load(f)

def save_meta(meta):
    meta_path = Path(CAMPAIGNS_DIR) / meta["campaign_id"] / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

def read_email_body(campaign_id, filename="email_v1.txt"):
    path = Path(CAMPAIGNS_DIR) / campaign_id / filename
    if not path.exists():
        return None
    with open(path) as f:
        content = f.read()
    # Remove subject line if present
    if content.startswith("Subject:"):
        lines = content.split("\n")
        body = "\n".join(lines[2:]).strip()
        subject = lines[0].replace("Subject:", "").strip()
        return subject, body
    return None, content.strip()

def mark_sent(meta, day):
    """Update metadata to reflect sent email"""
    meta[f"sent_{day}"] = True
    meta[f"sent_{day}_at"] = datetime.now().isoformat()
    meta["last_sent"] = day
    save_meta(meta)

def print_campaign_preview(meta, subject, body):
    print(f"\n{'='*60}")
    print(f"📤 SEND EMAIL — {meta['company']}")
    print(f"{'='*60}")
    print(f"To: {meta['email']}")
    print(f"Subject: {subject}")
    print(f"\nBody:\n{'-'*40}")
    print(body)
    print(f"{'='*60}")

def get_next_campaign():
    """Find oldest campaign with day1 not sent"""
    for cid_dir in sorted(Path(CAMPAIGNS_DIR).iterdir()):
        if not cid_dir.is_dir():
            continue
        meta = load_campaign(cid_dir.name)
        if not meta:
            continue
        if meta.get("sent_day1"):
            continue
        if meta.get("bounced") or meta.get("replied"):
            continue
        return meta
    return None

def main():
    campaign = get_next_campaign()
    
    if not campaign:
        print("No campaigns to send today.")
        print("All campaigns have been sent or need generation.")
        return
    
    campaign_id = campaign["campaign_id"]
    subject, body = read_email_body(campaign_id)
    
    if not body:
        print(f"Campaign {campaign_id} has no email content.")
        return
    
    # Print preview
    print_campaign_preview(campaign, subject, body)
    
    # Add signature
    sig = choice(SIGNATURES)
    full_body = f"{body}\n\n{sig}"
    
    # Ask for confirmation
    print(f"\n🤖 To send this email, Zo will use Gmail.")
    print(f"   From: sales@aigentforce.io via ragwetee@gmail.com")
    print(f"\n⏳ To actually send, you need to confirm.")
    print(f"   Run: python3 /home/workspace/scripts/larry_send.py --send")
    
    # Also show what follows if confirmed
    meta = load_campaign(campaign_id)
    print(f"\n📋 Campaign Timeline:")
    print(f"   Day 1  → Cold email       {'✅ SENT' if meta.get('sent_day1') else '⏳ PENDING'}")
    print(f"   Day 3  → Follow-up         {'✅ SENT' if meta.get('sent_day3') else '⏳ PENDING'}")
    print(f"   Day 7  → Break-up email    {'✅ SENT' if meta.get('sent_day7') else '⏳ PENDING'}")
    print(f"   Day 14 → Final check-in    {'✅ SENT' if meta.get('sent_day14') else '⏳ PENDING'}")

if __name__ == "__main__":
    import sys
    main()