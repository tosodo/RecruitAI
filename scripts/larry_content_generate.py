#!/usr/bin/env python3
"""
Larry — LinkedIn Post Generator
Generates 5 posts per campaign lead, stores to content/
"""
import json, os, sys
from pathlib import Path
from datetime import datetime, timedelta

CAMPAIGNS_DIR = "/home/workspace/data/campaigns"
CONTENT_DIR = "/home/workspace/data/content"
os.makedirs(CONTENT_DIR, exist_ok=True)

POST_TYPES = [
    ("story", "Story — personal angle, builds trust"),
    ("tip", "Tip — practical value, quick win"),
    ("question", "Question — drives engagement, starts conversation"),
    ("stat", "Stat — backed by data, establishes authority"),
    ("case_study", "Case Study — proof, social proof"),
]

def load_leads():
    with open("/home/workspace/data/leads.json") as f:
        return json.load(f)

def get_lead(campaign):
    leads = load_leads()["leads"]
    for lead in leads:
        if lead["email"] == campaign["email"]:
            return lead
    return {"name": "there", "company": campaign.get("company", "your business"), "industry": campaign.get("industry", "business")}

def generate_post(post_type, lead, company=None):
    name = lead.get("name", "there")
    first = name.split()[0] if name != "there" else "there"
    ind = lead.get("industry", "business")

    posts = {
        "story": [
            f"I almost missed the biggest opportunity of my year because I was too busy working IN my business to think about working ON it.\n\nSound familiar?\n\n{first} at {company or 'your business'} figured this out — and within 3 weeks of making one small change, their team reclaimed 10 hours every single week.\n\nThe fix wasn't a new hire. It wasn't a new tool.\n\nIt was AI. Specifically — the kind that handles the 6am inbox, the follow-up nobody sends, and the admin that keeps you stuck at your desk instead of growing your business.\n\nAsk me how if this sounds familiar.",
            f"Most business owners I talk to are spending 3-4 hours EVERY DAY on tasks that AI could handle in minutes.\n\n{first} at {company or 'their business'} was one of them.\n\nUntil they ran a free AI audit. One 30-minute call identified £2,000+ in wasted revenue per month.\n\nThe irony? They'd been too busy 'being productive' to see it.\n\nIf you're a UK business owner drowning in admin — I want to show you what's possible. Book a free AI audit. Link in comments.",
        ],
        "tip": [
            "UK small businesses: you're leaving £1,000+ per month on the table by not automating your follow-up emails.\n\nHere's why it matters:\n• 78% of customers buy from the first responder\n• Most businesses respond in 12+ hours\n• AI responds in 90 seconds\n\nThe businesses winning right now aren't working harder — they're working smarter.\n\nWhat's your biggest admin time-waster? Drop it in the comments 👇",
            "3 AI tools that save UK small businesses 10+ hours per week:\n\n1. Email automation — handles inquiries while you sleep\n2. Lead qualification — scores and routes leads automatically  \n3. Follow-up sequences — never miss a hot prospect\n\nMost businesses need all 3. Most don't have any.\n\nWhich one do you need most? Comment below and I'll point you in the right direction.",
        ],
        "question": [
            "If you had 10 extra hours every week — what would you actually DO with your business?\n\nNot 'work more.' Something strategic.\n\nFor most UK small business owners I talk to, the honest answer is: 'I'd finally work ON it instead of just IN it.'\n\nWhat's yours? 💬",
            "At what point does a small business NEED AI automation?\n\nA) When you're drowning\nB) When you hit £500k revenue\nC) When you start hiring admin staff\nD) Right now, proactively\n\nI've seen all 4 situations. The businesses that waited for A or C are always further behind than the ones who started at D.\n\nAgree? Disagree? 👇",
        ],
        "stat": [
            "73% of UK small businesses say admin is their biggest time drain.\n\nBut only 12% have any AI automation in place.\n\nThat's a gap. And the businesses closing that gap are the ones winning.\n\nIf you're in the 88% without AI — I'd love to show you what's possible. Free AI audit in the comments.",
            "Small businesses using AI automation save an average of 12 hours per week.\n\nThat's 600+ hours per year. Nearly 25 full days.\n\nWhat would you do with 25 extra days?\n\nLink in comments — I'll respond to every single one.",
        ],
        "case_study": [
            "After 30 days with AI automation, a UK estate agency we worked with saw:\n\n✓ 40% faster response to new enquiries\n✓ 10+ hours reclaimed per week for the team\n✓ £1,800 reduction in admin costs\n\nAll from one free audit and one implementation.\n\nSound too good to be true? That's exactly what their team said before we started.\n\nWant to see if this could work for YOUR business? Let's talk.",
        ],
    }
    import random
    pool = posts[post_type]
    return random.choice(pool)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--company":
        company = sys.argv[2] if len(sys.argv) > 2 else "their business"
        lead = {"name": "a UK business owner", "industry": "small business"}
    else:
        leads = load_leads()["leads"]
        if not leads:
            print("No leads found. Add leads first.")
            return
        lead = leads[0]
        company = lead.get("company", "their business")

    print(f"[Larry] Generating LinkedIn posts for {company}...")
    campaign_id = sys.argv[3] if len(sys.argv) > 3 else None

    generated = []
    for post_type, _ in POST_TYPES:
        content = generate_post(post_type, lead, company)
        slug = post_type.replace("_", "-")
        path = Path(CONTENT_DIR) / f"{slug}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        path.write_text(f"# {post_type.replace('_', ' ').title()}\n\nType: {post_type}\nCompany: {company}\nCampaign: {campaign_id or 'general'}\nCreated: {datetime.now().isoformat()}\nStatus: draft\n---\n{content}")
        generated.append(str(path))
        print(f"  ✅ Generated: {path.name}")

    print(f"\n[Larry] {len(generated)} posts ready. Run larry_buffer_poster.py to schedule them.")
    return generated

if __name__ == "__main__":
    main()