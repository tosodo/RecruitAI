#!/usr/bin/env python3
"""
Larry — Gmail Sender via Zo Ask API
Sends email FROM sales@aigentforce.io using Gmail integration
Uses Zo Ask API to trigger Gmail send with FROM address override
"""

import json
import os
import requests
import sys
from datetime import datetime, timedelta
from pathlib import Path

CAMPAIGNS_DIR = "/home/workspace/data/campaigns"
LEADS_FILE = "/home/workspace/data/leads.json"

def load_meta(campaign_id):
    with open(Path(CAMPAIGNS_DIR) / campaign_id / "metadata.json") as f:
        return json.load(f)

def save_meta(meta):
    with open(Path(CAMPAIGNS_DIR) / meta["campaign_id"] / "metadata.json", "w") as f:
        json.dump(meta, f, indent=2)

def read_email(campaign_id):
    path = Path(CAMPAIGNS_DIR) / campaign_id / "email_v1.txt"
    if not path.exists():
        return None, None
    with open(path) as f:
        content = f.read()
    if content.startswith("Subject:"):
        lines = content.split("\n", 1)
        subject = lines[0].replace("Subject:", "").strip()
        body = lines[1].strip()
        return subject, body
    return None, content.strip()

def send_via_zo_api(to_email, subject, body, from_email="sales@aigentforce.io"):
    """Send email using Zo Ask API + Gmail integration"""
    zo_token = os.environ.get("ZO_CLIENT_IDENTITY_TOKEN")
    if not zo_token:
        return False, "ZO_CLIENT_IDENTITY_TOKEN not set"
    
    # Build prompt for Zo to send email
    prompt = f"""Send an email with the following details:

From: {from_email}
To: {to_email}
Subject: {subject}
Body:
{body}

Use the Gmail integration to send this email. Make sure the From address is set to {from_email} (sales@aigentforce.io), not the default Gmail address.

Report back whether the email was sent successfully."""

    try:
        response = requests.post(
            "https://api.zo.computer/zo/ask",
            headers={
                "Authorization": zo_token,
                "Content-Type": "application/json"
            },
            json={
                "input": prompt,
                "model_name": "vercel:minimax/minimax-m2.7"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return True, "Email sent via Zo + Gmail"
        else:
            return False, f"Zo API error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_next_to_send():
    """Find campaigns ready to send day1"""
    for cid_dir in sorted(Path(CAMPAIGNS_DIR).iterdir()):
        if not cid_dir.is_dir():
            continue
        meta = load_meta(cid_dir.name)
        if meta.get("sent_day1"):
            continue
        if meta.get("bounced") or meta.get("replied"):
            continue
        if meta.get("status") == "paused":
            continue
        return meta
    return None

def main():
    if "--dry-run" in sys.argv:
        count = 0
        for cid_dir in sorted(Path(CAMPAIGNS_DIR).iterdir()):
            if not cid_dir.is_dir():
                continue
            meta = load_meta(cid_dir.name)
            if meta.get("sent_day1") or meta.get("bounced") or meta.get("replied") or meta.get("status") == "paused":
                continue
            subject, body = read_email(meta["campaign_id"])
            if body:
                print(f"Would send to: {meta['email']}")
                count += 1
        print(f"Total campaigns to send: {count}")
        return

    sent_count = 0
    for cid_dir in sorted(Path(CAMPAIGNS_DIR).iterdir()):
        if not cid_dir.is_dir():
            continue
        campaign_id = cid_dir.name
        meta = load_meta(campaign_id)
        if meta.get("sent_day1") or meta.get("bounced") or meta.get("replied") or meta.get("status") == "paused":
            continue
        subject, body = read_email(campaign_id)
        if not body:
            print(f"⚠ No email content for {meta['company']}")
            continue
        print(f"\n[Larry] Sending to: {meta['email']}")
        print(f"[Larry] Subject: {subject}")
        success, message = send_via_zo_api(meta["email"], subject, body)
        if success:
            meta["sent_day1"] = True
            meta["sent_day1_at"] = datetime.now().isoformat()
            meta["last_sent"] = "day1"
            save_meta(meta)
            print(f"✅ [{sent_count+1}] Sent! {message}")
            sent_count += 1
        else:
            print(f"❌ [{sent_count+1}] Failed: {message}")
            break
    print(f"\n🎯 Larry fired {sent_count} campaigns!")

if __name__ == "__main__":
    main()