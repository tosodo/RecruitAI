---
name: lead_research
description: Find and qualify UK small businesses for AIGENTFORCE outreach. Sasha uses Google Maps + web search to identify targets, then Larry scores and qualifies them. Primary targets: estate agents, restaurants, professional services.
compatibility: Zo Computer, Python 3, Google Maps API
metadata:
  author: tee.zo.computer
  category: Lead Generation
  display-name: Lead Research Engine
  tags: lead_research, prospect_list, UK_businesses, maps, AIGENTFORCE
---

# Lead Research Engine — Sasha's Radar

## What Sasha Does

Every morning at 8am, Sasha looks for new UK businesses to add to the pipeline:

1. **Primary targets** (highest conversion fit):
   - Estate agents (1–10 branches, UK)
   - Restaurants with 10+ staff (admin burden)
   - Professional services (solicitors, accountants, financial advisors)

2. **Secondary targets:**
   - Clinics/medical practices
   - Home services (plumbers, electricians with showrooms)
   - Retail with physical premises

3. **Excluded** (wrong segment):
   - Online-only businesses
   - Enterprises (50+ employees)
   - Businesses with no visible admin burden

---

## The Research Priority Matrix

| Segment | Priority | Why | Search Radius |
|---|---|---|---|
| Estate agents | 🔴 PRIMARY | High admin, time-sensitive, sees AI value fast | 30 miles from [postcode] |
| Restaurants (10+ staff) | 🟡 SECONDARY | High volume admin, shift scheduling, reviews | 15 miles |
| Solicitors (1–5 partners) | 🟡 SECONDARY | High admin, regulated, AI-receptive | 20 miles |
| Accountants | 🟢 TERTIARY | Seasonal admin spikes (Jan, Apr), good fit | 25 miles |
| All others | ⚪ NURTURE | Newsletter only | National |

---

## Sasha's Daily Research Protocol

### Morning Research Session (8:00–8:45am)

**Step 1: Pick the postcode sector**

Sasha picks 2–3 postcode sectors to research each day. Rotates through:
- Central London (SW, SE, E, N, W postcodes)
- Major cities: Birmingham, Manchester, Leeds, Bristol, Edinburgh, Glasgow
- Target towns: Reading, Oxford, Cambridge, Brighton, Southampton

**Never research the same postcode twice in 30 days.**

**Step 2: Run Maps Search**

For each postcode, Sasha runs:
```
maps_search(query="estate agents", location="[postcode]", min_rating=4.0, open_now=true)
```

Then filters to businesses with:
- 1–10 listed branches (not chains — too complex)
- 4+ stars
- Recent reviews mentioning "busy," "growing," "admin," "time"
- No obvious AI tooling (if they mention AI tools in reviews, downgrade)

**Step 3: Web Scraping for Each Lead**

For each business found, Sasha reads:
1. Google Business Profile (review summary)
2. Their website (homepage + services page)
3. Any G2/Capterra presence (indicates AI-awareness)

**Step 4: Score and File**

For each business that passes Step 3, Sasha creates a lead entry:

```json
{
  "id": "uuid",
  "name": "[Owner/Contact Name or 'Unknown']",
  "company": "[Business Name]",
  "email": "unknown",
  "phone": "[From Google if available]",
  "source": "maps_research/[date]",
  "tier": "B",
  "status": "new",
  "score": 0,
  "website": "[URL]",
  "location": "[Full address]",
  "postcode": "[Sector]",
  "rating": [X],
  "reviewCount": [X],
  "notes": "[Observations from research]",
  "createdAt": "[ISO date]",
  "updatedAt": "[ISO date]"
}
```

---

## The Qualification Checklist (Before Adding to Leads)

Sasha asks these 5 questions for every business:

| Question | Why It Matters | Pass Criteria |
|---|---|---|
| 1. Is it UK-based, 1–10 employees? | Our ICP | Yes/No |
| 2. Is there visible admin burden? | AI fit | Reviews mention busy/admin/time |
| 3. Do they have a website? | Our outreach needs a destination | Yes |
| 4. Have they mentioned AI tools anywhere? | Receptiveness signal | No = better (easier to position) |
| 5. Are they within our target radius? | Practical sales territory | Yes |

**Pass all 5 → Add as Tier B lead**
**Pass 4 → Add as Tier C lead**
**Pass 3 or fewer → Skip (not a fit)**

---

## Research by Segment — Specific Search Templates

### Estate Agents
```
Primary query: "estate agents [postcode]" + "estate agents near [landmark]"
Filters: 4+ stars, 5–50 reviews, NOT chain (no Foxtons, Hamptons, Savills)
Signal of admin pain: mentions of "viewings," "enquiries," "paperwork," "time"
Signal of AI awareness: mentions of "automated," "online," "portal" — these are actually good signals
Warning: If they have a sophisticated tech stack already (5+ tools), downgrade — competitive sale
```

### Restaurants
```
Primary query: "restaurants [postcode]" + "restaurants near me"
Filters: 4+ stars, 20+ reviews, 10+ staff (check website)
Signal of admin pain: reviews mention "busy," "long waits," "booking issues"
Warning: Restaurant owners are time-poor but often cash-poor — budget may be an issue
```

### Solicitors
```
Primary query: "solicitors [postcode]" + "law firm near [landmark]"
Filters: 4+ stars, 3–20 staff, not LegalAid-heavy (volume, low margin)
Signal of admin pain: reviews mention "slow," "paperwork," "calls," "chasing"
Warning: Legal has strict compliance — AI use cases are more limited at first
```

---

## The Research Output Format

After each research session, Sasha writes a summary:

```
## Lead Research Summary — [Date]

### Postcodes Researched
- [Postcode 1] — [X] businesses found, [Y] qualified
- [Postcode 2] — [X] businesses found, [Y] qualified
- [Postcode 3] — [X] businesses found, [Y] qualified

### Qualified Leads Added
| Company | Location | Tier | Key Signal |
|---|---|---|---|
| [Name] | [Postcode] | B | [Observation e.g. "5-star, busy, no AI"] |

### Skipped (Not a Fit)
| Company | Reason |
|---|---|
| [Name] | [Specific reason: chain, wrong size, tech-heavy] |

### Notes for Larry
- [Any specific context about the area or segment]
- [Any businesses that need immediate outreach if high-urgency signals found]

### Next Session
Will target: [Postcodes] — prioritised because [reason]
```

---

## Sasha's Never-Do List

1. Never add a chain (Foxtons, Domino's, Cafe Nero) — wrong segment
2. Never add a business with 50+ employees — enterprise sales, not our model
3. Never skip the website check — if no website, no outreach possible
4. Never research the same postcode twice in 30 days — diminishing returns
5. Never add a lead without a location — impossible to prioritise geographically
6. Never add a lead without at least ONE positive signal (4+ stars OR mention of growth)

---

## Files Sasha Reads

- `/home/workspace/data/leads.json` — checks for duplicates before adding
- `/home/workspace/AIGENTFORCE-memory.md` — reminds herself of target segments

## Files Sasha Writes

- `/home/workspace/data/leads.json` — appends new leads
- `/home/workspace/data/research-sessions/[date].md` — research summary

## Rotating Postcode System

To ensure coverage without waste, Sasha maintains a list of postcodes:

```python
# Rotates through this list, 3 per day
POSTCODE_ROTATION = [
    "SW1A", "SW5", "SW6", "SW10", "SW11",  # Central/West London
    "SE1", "SE5", "SE15", "SE22",           # South London
    "E1", "E2", "E8", "E14",                 # East London
    "N1", "N4", "N7", "N16",                 # North London
    "W1", "W2", "W8", "W11",                 # West London
    "B1", "B2", "B3",                         # Birmingham
    "M1", "M2", "M4", "M8",                  # Manchester
    "BS1", "BS2", "BS8",                      # Bristol
    "EH1", "EH2", "EH3",                      # Edinburgh
    "G1", "G2", "G3",                          # Glasgow
]
```

Sasha works through 3 per day, rotating back after 30 days.