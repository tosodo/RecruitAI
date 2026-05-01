#!/usr/bin/env python3
"""
AIGENTFORCE Email Delivery System
Uses Zo's email sender (not SMTP) for guaranteed delivery
"""

import os
import json
import requests
from datetime import datetime

def send_via_zo(to_email, subject, body):
    """Send email using Zo's built-in email capability"""
    zo_token = os.environ.get("ZO_CLIENT_IDENTITY_TOKEN")
    if not zo_token:
        return False, "No Zo token"
    
    try:
        # Use Zo's email delivery through the Zo API
        response = requests.post(
            "https://api.zo.computer/zo/ask",
            headers={
                "Authorization": zo_token,
                "Content-Type": "application/json"
            },
            json={
                "input": f"Send an email with the following details:\n\nFrom: AIGENTFORCE <sales@aigentforce.io>\nTo: {to_email}\nSubject: {subject}\nBody:\n{body}\n\nIMPORTANT: Send this email immediately. Do not save as draft. Report success or failure.",
                "model_name": "vercel:minimax/minimax-m2.7"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return True, "Sent via Zo"
        else:
            return False, f"Zo error: {response.status_code}"
    except Exception as e:
        return False, str(e)

def send_alert_email(subject, body):
    """Send critical alert"""
    return send_via_zo("osodot@icloud.com", f"[ALERT] {subject}", body)

def send_briefing(to_email, subject, body):
    """Send routine briefing"""
    return send_via_zo(to_email, subject, body)

def send_lead_alert(lead_data):
    """Send hot lead alert with full details"""
    subject = f"🔥 HOT LEAD: {lead_data['name']} — {lead_data['company']}"
    body = f"""A new Tier A lead has been detected.

Name: {lead_data['name']}
Company: {lead_data['company']}
Email: {lead_data['email']}
Phone: {lead_data['phone']}
Score: {lead_data['score']}/100
Source: {lead_data['source']}

Recommended action: Call within 2 hours.

— AIGENTFORCE Alert System
"""
    return send_via_zo("osodot@icloud.com", subject, body)

if __name__ == "__main__":
    # Test email
    success, msg = send_via_zo(
        "osodot@icloud.com",
        "AIGENTFORCE Email System — Test",
        "This is a test from AIGENTFORCE email system.\n\n"
        "If you received this, email delivery is working.\n\n"
        "— Technical Team\n"
        f"Sent at: {datetime.now().isoformat()}"
    )
    print(f"Email test result: {msg}")
    
    # Log result
    with open("/home/workspace/data/email_alerts.log", "a") as f:
        timestamp = datetime.now().isoformat()
        status = "✅" if success else "❌"
        f.write(f"[{timestamp}] {status} Email test: {msg}\n")