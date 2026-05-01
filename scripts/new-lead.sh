#!/bin/bash
# new-lead.sh — Add a new lead to the AIGENTFORCE CRM
# Usage: ./new-lead.sh "Name" "Business" "Email" "Source" "PainPoint1,PainPoint2"

NAME="$1"
BUSINESS="$2"
EMAIL="$3"
SOURCE="$4"
PAIN_POINTS="$5"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ -z "$NAME" ] || [ -z "$EMAIL" ]; then
  echo "Usage: ./new-lead.sh \"Name\" \"Business\" \"Email\" \"Source\" \"PainPoint1,PainPoint2\""
  exit 1
fi

# Generate a unique ID
ID=$(echo "$NAME $EMAIL $TIMESTAMP" | sha256sum | cut -c1-12)

# Create lead entry
LEAD=$(cat <<EOF
{
  "id": "$ID",
  "name": "$NAME",
  "business": "$BUSINESS",
  "email": "$EMAIL",
  "source": "$SOURCE",
  "status": "new",
  "pain_points": [$(echo "$PAIN_POINTS" | sed 's/,/", "/g' | sed 's/^/"/;s/$/"/')],
  "messages_sent": [],
  "created_at": "$TIMESTAMP",
  "updated_at": "$TIMESTAMP"
}
EOF
)

# Add to leads.json
echo "$LEAD" | jq --argjson lead "$LEAD" \
  '.leads += [$lead] | .metadata.total += 1 | .metadata.last_updated = "'"$TIMESTAMP"'"' \
  /home/workspace/data/leads.json > /tmp/leads_tmp.json && mv /tmp/leads_tmp.json /home/workspace/data/leads.json

echo "✅ Lead added: $NAME <$EMAIL>"
echo "📋 Status: new | Next action: Review and qualify"
echo "📁 File: /home/workspace/data/leads.json"
