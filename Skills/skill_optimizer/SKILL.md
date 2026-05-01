---
name: skill_optimizer
description: |
  Improve existing skills by reducing cost and increasing clarity. Use when performance is weak or outputs are generic.
compatibility: Zo Computer
metadata:
  author: tee
  category: Meta
  display-name: Skill Optimizer
  tags: skills, optimization, cost reduction, clarity
---

# skill_optimizer

Optimise an existing skill's SKILL.md. Never overwrite the original.

## Steps

1. Read the skill's current SKILL.md
2. Count current lines
3. Identify: redundant text, vague rules, duplicate instructions, generic phrases
4. Rewrite to shorter/clearer format
5. Save improved version as `Skills/<skill>/SKILL_v2.md`
6. Report: changes summary + estimated token reduction %

## Constraints

- Reduce total lines by 30%+ minimum
- Do NOT add new sections unless critical
- Replace paragraphs with bullet rules
- Convert prose to decision conditions
- Remove generic phrases ("handle intelligently", "as appropriate", etc.)
- Max 1 sentence per rule
- Max 150 lines in output

## Output Format

```
## Changes Made
[numbered list]

## Token Reduction
[old lines] → [new lines] ([X]% reduction)
```

## Rules

- No duplicate instructions anywhere in the skill
- Each step must be uniquely identifiable
- Never overwrite original SKILL.md