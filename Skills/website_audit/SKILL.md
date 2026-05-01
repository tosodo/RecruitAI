---
name: website_audit
description: |
  Analyse business websites for conversion and UX issues. Use when website URLs are available and task requires quality evaluation.
compatibility: Zo Computer, browser tools, web_research
metadata:
  author: tee
  category: Lead Generation
  display-name: Website Audit
  tags: website audit, UX, conversion, lead quality
---

# website_audit

Audit business websites for conversion and UX issues. Max 6 issues per site.

## Execution

**For each URL, run `use_webpage` or `read_webpage`:**
- Mobile responsiveness
- Page structure clarity
- Call-to-action visibility
- Design quality (modern vs outdated)
- Trust signals (reviews, testimonials)
- Load performance

## Constraints

- Use bullet points only
- Max 6 issues per site
- Be specific — name exact elements, not vague categories
- Severity: Low / Medium / High

## Output

```
## [Business Name](URL)

**Issues:**
- [High] Specific issue with exact element referenced
- [Medium] Specific issue
- [Low] Specific issue

**Overall:** Good / Needs Work / Poor
```

Skip sites with no website URL or broken links.