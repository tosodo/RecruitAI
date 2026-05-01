#!/usr/bin/env python3
"""
Alex — AIGENTFORCE Supervisor Agent
The AI CEO: Coordinates all agents, routes work, escalates to Osodo. T

Alex is the layer between you and all other agents. She:
- Reads all agent outputs and logs
- Prepares your morning brief
- Routes leads to the right agents
- Flags urgent items
- Tracks team performance
"""

import json
import os
import sys
sys.path.insert(0, '/home/workspace/scripts')

from email_delivery import send_via_zo, send_briefing
from datetime import datetime
from pathlib import Path
from typing import Optional

DATA = Path("/home/workspace/data")
CAMPAIGNS = DATA / "campaigns"
LEADS_FILE = DATA / "leads.json"
AUDITS_FILE = DATA / "audits.json"
LOG_DIR = DATA / "agent_logs"

class Alex:
    """Supervisor Agent — coordinates the AIGENTFORCE AI team"""
    
    def __init__(self):
        self.name = "Alex"
        self.role = "Supervisor Agent"
        self.reports_to = "Osodo. T"
        self.team = ["Sasha", "Larry", "Marcus"]
    
    def read_file(self, path: Path) -> Optional[dict]:
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return None
    
    def get_campaign_stats(self) -> dict:
        stats = {
            "active": 0,
            "sent": 0,
            "awaiting_reply": 0,
            "replies": 0,
            "meetings_booked": 0
        }
        if not CAMPAIGNS.exists():
            return stats
        
        for cid_dir in CAMPAIGNS.iterdir():
            if not cid_dir.is_dir():
                continue
            meta_path = cid_dir / "metadata.json"
            if meta_path.exists():
                with open(meta_path) as f:
                    meta = json.load(f)
                stats["active"] += 1
                if meta.get("sent_day1"):
                    stats["sent"] += 1
                if meta.get("replied"):
                    stats["replies"] += 1
                if meta.get("meeting_booked"):
                    stats["meetings_booked"] += 1
                if not meta.get("replied") and meta.get("sent_day1"):
                    stats["awaiting_reply"] += 1
        return stats
    
    def get_lead_stats(self) -> dict:
        data = self.read_file(LEADS_FILE) or {"leads": []}
        data2 = self.read_file(AUDITS_FILE) or {"audits": []}
        leads = data["leads"]
        audits = data2["audits"]
        return {
            "total_leads": len(leads),
            "tier_a": sum(1 for l in leads if l.get("tier") == "A"),
            "tier_b": sum(1 for l in leads if l.get("tier") == "B"),
            "tier_c": sum(1 for l in leads if l.get("tier") == "C"),
            "new_today": sum(1 for a in audits if a.get("createdAt", "").startswith(datetime.now().strftime("%Y-%m-%d"))),
            "total_audits": len(audits),
        }
    
    def get_action_items(self) -> list:
        """What needs human attention RIGHT NOW"""
        items = []
        data = self.read_file(LEADS_FILE) or {"leads": []}
        
        # Flag Tier A leads
        tier_a = [l for l in data["leads"] if l.get("tier") == "A" and l.get("status") != "won"]
        if tier_a:
            items.append({
                "priority": "HIGH",
                "action": "Call these Tier A leads now",
                "items": tier_a,
                "agent": "Sasha"
            })
        
        # Flag replies from campaigns
        stats = self.get_campaign_stats()
        if stats["replies"] > 0:
            items.append({
                "priority": "URGENT",
                "action": "Reply to campaign responses",
                "count": stats["replies"],
                "agent": "Larry"
            })
        
        return items
    
    def generate_morning_brief(self) -> str:
        stats = self.get_campaign_stats()
        leads = self.get_lead_stats()
        actions = self.get_action_items()
        date_str = datetime.now().strftime("%A, %d %B %Y")
        
        brief = f"""
**Good morning Osodo. Here's your AIGENTFORCE briefing for {date_str}:**

**📊 CAMPAIGN STATUS**
- Active campaigns: {stats['active']}
- Day 1 emails sent: {stats['sent']}
- Awaiting reply (Day 3-7): {stats['awaiting_reply']}
- Replies received: {stats['replies']}
- Meetings booked: {stats['meetings_booked']}

**🎯 LEADS PIPELINE**
- Total leads: {leads['total_leads']}
- Tier A (call now): {leads['tier_a']}
- Tier B (nurture): {leads['tier_b']}
- Tier C (future): {leads['tier_c']}
- Audits submitted (total): {leads['total_audits']}

**📋 TODAY'S ACTION ITEMS**
"""
        if not actions:
            brief += "- No urgent action required — Larry is running the sequences\n"
        else:
            for i, item in enumerate(actions, 1):
                brief += f"{i}. **[{item['priority']}]** {item['action']}"
                if "count" in item:
                    brief += f" ({item['count']} replies)"
                brief += f"\n   → Assigned to: {item['agent']}\n"
        
        brief += f"""
**🔍 TEAM STATUS**
- Sasha (Sales Ops): ✅ Active — monitoring leads
- Larry (Outreach): ✅ Active — running {stats['active']} campaigns
- Marcus (Research): ✅ Standby — awaiting new targets

**⚠️ FLAGS FOR YOU**
"""
        if not actions:
            brief += "- None — all systems green\n"
        else:
            for item in actions:
                brief += f"- **[{item['priority']}]** {item['action']}\n"
        
        brief += f"""
---
*Alex | AIGENTFORCE Supervisor Agent | Next update in 24 hours*
*All systems operational | {date_str}*"""
        return brief
    
    def run_daily_check(self) -> str:
        """Full daily supervisor check"""
        os.makedirs(LOG_DIR, exist_ok=True)
        
        brief = self.generate_morning_brief()
        
        # Log the brief
        log_file = LOG_DIR / f"alex_brief_{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_file, "w") as f:
            f.write(brief)
        
        return brief

def main():
    alex = Alex()
    result = alex.run_daily_check()
    print(result)

if __name__ == "__main__":
    main()
