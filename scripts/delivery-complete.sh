#!/bin/bash
# delivery-complete.sh — Mark client delivery complete and request testimonial
# Usage: ./delivery-complete.sh "ClientName"

CLIENT="$1"

if [ -z "$CLIENT" ]; then
  echo "Usage: ./delivery-complete.sh \"ClientName\""
  exit 1
fi

FOLDER="/home/workspace/data/clients/$(echo "$CLIENT" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
DONE_FILE="$FOLDER/delivery-complete.md"

if [ ! -f "$FOLDER/brief.md" ]; then
  echo "❌ No brief found for $CLIENT. Run audit-booked.sh first."
  exit 1
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create delivery complete record
cat > "$DONE_FILE" <<EOF
# Delivery Complete — $CLIENT

- **Completed**: $TIMESTAMP
- **All automations delivered**: [ ]
- **Walkthrough video**: [URL or "pending"]
- **Client sign-off received**: [yes/no]
- **Testimonial requested**: [yes/no]
- **Referral requested**: [yes/no]

## Client Feedback
[Add client feedback here]

## Testimonial (if received)
> "[Quote]"

## Referral Contact
- Name: [Name]
- Email: [Email]
- Business: [Business]
EOF

# Update brief status
sed -i "s/Status.*/Status: DELIVERED/" "$FOLDER/brief.md"
for i in 1 2 3; do
  sed -i "s/Status.*pending.*/Status: delivered/" "$FOLDER/brief.md"
done

echo "✅ Delivery record created: $DONE_FILE"
echo "📋 Next: Request testimonial — 'How did it go?' → 'Would you mind sharing a quick testimonial?'"
