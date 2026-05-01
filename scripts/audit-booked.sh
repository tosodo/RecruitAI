#!/bin/bash
# audit-booked.sh — Create client brief when audit is booked
# Usage: ./audit-booked.sh "ClientName" "BusinessName" "Email"

CLIENT="$1"
BUSINESS="$2"
EMAIL="$3"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ -z "$CLIENT" ] || [ -z "$EMAIL" ]; then
  echo "Usage: ./audit-booked.sh \"ClientName\" \"BusinessName\" \"Email\""
  exit 1
fi

# Create client folder
FOLDER="/home/workspace/data/clients/$(echo "$CLIENT" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
mkdir -p "$FOLDER"

# Copy brief template
cp /home/workspace/data/clients/CLIENT-NAME/brief.md "$FOLDER/brief.md"

# Replace placeholders
sed -i "s/\[CLIENT NAME\]/$CLIENT/g" "$FOLDER/brief.md"
sed -i "s/\[Business Name\]/$BUSINESS/g" "$FOLDER/brief.md"
sed -i "s/\[email@domain.com\]/$EMAIL/g" "$FOLDER/brief.md"
sed -i "s/\[Full Name\]/$CLIENT/g" "$FOLDER/brief.md"

# Update leads.json status
if [ -f /home/workspace/data/leads.json ]; then
  EMAIL_ESCAPED=$(echo "$EMAIL" | sed 's/[\/&]/\\&/g')
  jq --arg email "$EMAIL_ESCAPED" \
     '(.leads[] | select(.email == $email)).status = "booked" | (.leads[] | select(.email == $email)).updated_at = "'"$TIMESTAMP"'"' \
     /home/workspace/data/leads.json > /tmp/leads_tmp.json && mv /tmp/leads_tmp.json /home/workspace/data/leads.json
fi

echo "✅ Client brief created: $FOLDER/brief.md"
echo "📋 Status updated: booked"
echo "📁 Next: Run audit call and fill in $FOLDER/brief.md"
