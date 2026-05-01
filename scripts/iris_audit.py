#!/usr/bin/env python3
"""
IRIS — Audit & Delivery Agent
AIGENTFORCE's lead closing agent
- Scores audit submissions (0-100)
- Sends personalised email with score + opportunities + Calendly link
- Creates client brief for Tier A leads
- Alerts SASHA of new high-value leads
- 3-hour heartbeat (scales to 15 min as we grow)
"""

import json
import os
import uuid
import requests
from datetime import datetime, timedelta
from pathlib import Path

# === CONFIG ===
AUDITS_FILE = "/home/workspace/data/audits.json"
LEADS_FILE = "/home/workspace/data/leads.json"
BRIEFFILE = "/home/workspace/data/client-briefs"
ZO_TOKEN = os.environ.get("ZO_CLIENT_IDENTITY_TOKEN")
SALES_EMAIL = "sales@aigentforce.io"
CALENDLY_URL = "https://calendly.com/osodot/ai-audit-free"

# === SCORING MATRIX ===
def score_lead(answers: dict) -> tuple[int, str, list]:
    """Score a lead 0-100, return tier + top 3 opportunities"""
    score = 0
    opportunities = []
    
    # Budget confirmed (max 25 pts)
    budget = answers.get("budget", "").lower()
    if "budget" in budget or any(w in budget for w in ["£500", "£1000", "200", "500", "1000"]):
        score += 25
    elif budget in ["under £100", "under £1000"]:
        score += 15
    else:
        score += 5
    
    # Timeline (max 25 pts)
    timeline = answers.get("timeline", "").lower()
    if "immediately" in timeline or "asap" in timeline or "week" in timeline:
        score += 25
    elif "month" in timeline:
        score += 15
    else:
        score += 5
    
    # Team size (max 20 pts)
    team = answers.get("teamSize", "").lower()
    if any(w in team for w in ["5-10", "10+", "five", "ten", "large"]):
        score += 20
    elif any(w in team for w in ["2-5", "2 ", "three", "four"]):
        score += 12
    else:
        score += 5
    
    # AI tools already tried (max 15 pts — they know the value)
    ai_tools = answers.get("aiTools", "").lower()
    if ai_tools and ai_tools != "none" and ai_tools != "not using any":
        score += 15
    else:
        score += 8
    
    # Biggest challenge matches our offering (max 15 pts)
    challenge = answers.get("biggestChallenge", "").lower()
    if any(w in challenge for w in ["time", "admin", "manual", "follow", "lead", "customer"]):
        score += 15
    else:
        score += 5
    
    # Tier assignment
    if score >= 75:
        tier = "A"
    elif score >= 50:
        tier = "B"
    else:
        tier = "C"
    
    # Generate top 3 opportunities based on answers
    if any(w in challenge for w in ["time", "admin", "manual", "follow", "email"]):
        opportunities.append("Email automation — save 10+ hours/week on routine replies")
    if any(w in challenge for w in ["lead", "customer", "conversion", "win"]):
        opportunities.append("AI-powered lead qualification — convert more browsers to buyers")
    if any(w in challenge for w in ["content", "social", "marketing"]):
        opportunities.append("Content generation AI — post consistently without the burnout")
    if any(w in challenge for w in ["data", " organise", "track", "crm"]):
        opportunities.append("Smart CRM setup — auto-track every lead and never miss a follow-up")
    if any(w in challenge for w in ["cost", "budget", "affordable", "cheap"]):
        opportunities.append("DIY AI toolkit — our £50/month Starter plan covers everything you need")
    
    # Fill to 3 if needed
    if len(opportunities) < 3:
        opportunities.append("AI chatbot for your website — 24/7 lead capture while you sleep")
    
    return score, tier, opportunities[:3]

def load_audits():
    if not Path(AUDITS_FILE).exists():
        return []
    with open(AUDITS_FILE) as f:
        data = json.load(f)
        return data.get("audits", [])

def save_audits(audits):
    with open(AUDITS_FILE, "w") as f:
        json.dump({"audits": audits}, f, indent=2)

def load_leads():
    if not Path(LEADS_FILE).exists():
        return {"leads": []}
    with open(LEADS_FILE) as f:
        return json.load(f)

def save_leads(data):
    with open(LEADS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def send_email_via_zo(to_email: str, subject: str, body: str, from_email: str = SALES_EMAIL) -> bool:
    """Send email using Zo Ask API + Gmail"""
    if not ZO_TOKEN:
        print("❌ ZO_CLIENT_IDENTITY_TOKEN not set")
        return False
    
    prompt = f"""Send an email with these exact details:

From: {from_email}
To: {to_email}
Subject: {subject}
Body:
{body}

IMPORTANT:
- Use the Gmail integration to send this email
- The From address MUST be "{from_email}" (sales@aigentforce.io), NOT your default email
- Make sure the email is sent successfully
- Report back: "Email sent successfully" or the exact error message"""

    try:
        response = requests.post(
            "https://api.zo.computer/zo/ask",
            headers={
                "Authorization": ZO_TOKEN,
                "Content-Type": "application/json"
            },
            json={
                "input": prompt,
                "model_name": "vercel:minimax/minimax-m2.7"
            },
            timeout=90
        )
        
        if response.status_code == 200:
            result = response.json()
            output = result.get("output", "")
            if "error" in output.lower() or "fail" in output.lower():
                print(f"❌ Zo reported issue: {output}")
                return False
            return True
        else:
            print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def create_client_brief(audit: dict, score: int, tier: str, opportunities: list):
    """Create client brief for Tier A leads"""
    Path(BRIEFFILE).mkdir(parents=True, exist_ok=True)
    company_slug = audit.get("company", "unknown").lower().replace(" ", "-").replace("&", "-")
    brief_path = Path(BRIEFFILE) / f"{company_slug}-{audit['id'][:8]}.md"
    
    brief = f"""# Client Brief — {audit.get('company', 'Unknown')}

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Source:** Audit form submission
**Audit Score:** {score}/100 ({tier} tier)

---

## Contact
- **Name:** {audit.get('name', 'N/A')}
- **Email:** {audit.get('email', 'N/A')}
- **Phone:** {audit.get('phone', 'N/A')}
- **Company:** {audit.get('company', 'N/A')}

---

## Business Profile
- **Industry:** {audit.get('industry', 'N/A')}
- **Team Size:** {audit.get('teamSize', 'N/A')}
- **Current AI Tools:** {audit.get('aiTools', 'N/A')}

---

## Their Challenge
{audit.get('biggestChallenge', 'N/A')}

---

## Top 3 AI Opportunities
{chr(10).join(f"{i+1}. {opp}" for i, opp in enumerate(opportunities))}

---

## Timeline: {audit.get('timeline', 'N/A')}
## Budget: {audit.get('budget', 'N/A')}

---

## Recommended Actions
1. Book discovery call via Calendly
2. Prepare tailored proposal based on their score
3. Send follow-up with relevant case study

---
*Brief generated by IRIS — AIGENTFORCE Audit & Delivery Agent*
"""
    
    with open(brief_path, "w") as f:
        f.write(brief)
    print(f"✅ Client brief created: {brief_path}")
    return str(brief_path)

def alert_sasha(audit: dict, score: int, tier: str):
    """Send alert to Osodo. T about new lead (SASHA-style alert)"""
    if tier != "A":
        return
    
    alert_subject = f"🚨 Tier A Lead — {audit.get('name', 'Unknown')} ({score}/100)"
    alert_body = f"""NEW TIER A LEAD DETECTED

Name: {audit.get('name', 'N/A')}
Company: {audit.get('company', 'N/A')}
Email: {audit.get('email', 'N/A')}
Phone: {audit.get('phone', 'N/A')}
Score: {score}/100

Their Challenge: {audit.get('biggestChallenge', 'N/A')}

Timeline: {audit.get('timeline', 'N/A')}
Budget: {audit.get('budget', 'N/A')}

📅 Book their call: {CALENDLY_URL}

IRIS has sent them their audit report with their score + top 3 AI opportunities.

— IRIS (Audit & Delivery Agent)"""
    
    send_email_via_zo(
        to_email="osodot@icloud.com",
        subject=alert_subject,
        body=alert_body
    )
    print(f"✅ SASHA-style alert sent for Tier A lead")

def generate_audit_email(audit: dict, score: int, tier: str, opportunities: list) -> tuple[str, str]:
    """Generate personalised audit reply email"""
    first_name = audit.get("name", "there").split()[0] if audit.get("name") else "there"
    company = audit.get("company", "your business")
    
    # Score interpretation
    if score >= 80:
        score_msg = "You're clearly ready for AI"
        score_colour = "🎯"
    elif score >= 60:
        score_msg = "You're close — just need the right system"
        score_colour = "⚡"
    elif score >= 40:
        score_msg = "Big opportunity sitting untapped"
        score_colour = "💡"
    else:
        score_msg = "Quick wins are there — let us show you"
        score_colour = "🚀"
    
    subject = f"Your AI Audit Results — {score}/100 for {company}"
    
    body = f"""Hi {first_name},

{score_colour} YOUR AI AUDIT RESULTS

Business: {company}
Audit Score: {score}/100 — {score_msg}

---

TOP 3 AI OPPORTUNITIES FOR YOUR BUSINESS

{chr(10).join(f"{i+1}. {opp}" for i, opp in enumerate(opportunities))}

---

WHAT HAPPENS NEXT

📅 BOOK YOUR FREE 30-MINUTE CALL
→ {CALENDLY_URL}

During our call, I'll show you:
• Exactly which of your daily tasks AI can handle
• How other {audit.get('industry', 'businesses')} have saved 10+ hours/week
• A custom roadmap to get your first AI automation running in 48 hours

No cost. No commitment. Just clarity.

— Osodo. T
AIGENTFORCE | Stop Working Harder. Make AI Work Harder.
"""
    
    return subject, body

def process_unprocessed_audits():
    """Main logic — find unprocessed audits and handle them"""
    audits = load_audits()
    
    for audit in audits:
        if audit.get("iris_processed"):
            continue
        
        email = audit.get("email", "")
        if not email:
            print("⚠️ No email for audit, skipping")
            audit["iris_processed"] = True
            audit["iris_error"] = "No email provided"
            continue
        
        # Score the lead
        score, tier, opportunities = score_lead(audit)
        
        # Update audit record
        audit["score"] = score
        audit["tier"] = tier
        audit["opportunities"] = opportunities
        audit["iris_processed"] = True
        audit["iris_processed_at"] = datetime.now().isoformat()
        
        # Send email to lead with their score
        subject, body = generate_audit_email(audit, score, tier, opportunities)
        email_sent = send_email_via_zo(email, subject, body)
        audit["email_sent"] = email_sent
        
        if email_sent:
            print(f"✅ Audit email sent to {email} (score: {score}, tier: {tier})")
        else:
            print(f"❌ Failed to send audit email to {email}")
        
        # Create client brief for Tier A
        if tier == "A":
            brief_path = create_client_brief(audit, score, tier, opportunities)
            audit["client_brief"] = brief_path
        
        # Alert Osodo. T (SASHA-style) for Tier A
        if tier == "A":
            alert_sasha(audit, score, tier)
        
        # Also add to leads.json
        leads_data = load_leads()
        new_lead = {
            "id": str(uuid.uuid4()),
            "name": audit.get("name", ""),
            "company": audit.get("company", ""),
            "email": email,
            "phone": audit.get("phone", ""),
            "source": "audit_form",
            "tier": tier,
            "status": "new",
            "score": score,
            "answers": {
                "industry": audit.get("industry", ""),
                "teamSize": audit.get("teamSize", ""),
                "aiTools": audit.get("aiTools", ""),
                "biggestChallenge": audit.get("biggestChallenge", ""),
                "timeline": audit.get("timeline", ""),
                "budget": audit.get("budget", "")
            },
            "createdAt": audit.get("createdAt", datetime.now().isoformat()),
            "updatedAt": datetime.now().isoformat(),
            "lastContactedAt": datetime.now().isoformat() if email_sent else None
        }
        leads_data["leads"].append(new_lead)
        save_leads(leads_data)
        print(f"✅ Lead added to pipeline: {audit.get('name')} ({tier})")
    
    save_audits(audits)

def main():
    print(f"**IRIS — Audit & Delivery Agent**")
    print(f"**AIGENTFORCE | {datetime.now().strftime('%d %B %Y, %H:%M')}**")
    print(f"=" * 50)
    
    audits = load_audits()
    unprocessed = [a for a in audits if not a.get("iris_processed")]
    
    print(f"Total audits: {len(audits)}")
    print(f"Unprocessed: {len(unprocessed)}")
    
    if not unprocessed:
        print("No new audits to process. IRIS is resting.")
        return
    
    print(f"\n{'='*50}")
    print(f"PROCESSING {len(unprocessed)} NEW AUDIT(S)...")
    print(f"{'='*50}")
    
    process_unprocessed_audits()
    
    print(f"\n**IRIS heartbeat complete**")
    print(f"Next check in 3 hours.")

if __name__ == "__main__":
    main()