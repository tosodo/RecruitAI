---
name: zopenclaw
description: |
  Install and run OpenClaw on Zo Computer with Tailscale private networking, browser Control UI, and Zo MCP tools via mcporter. Use when user wants OpenClaw running on Zo, or mentions "openclaw", "personal agent framework", or running a persistent AI agent with Telegram/Discord/WhatsApp. NOT for general Zo agent setup.
compatibility: Zo Computer, Node.js, npm, curl, jq
metadata:
  author: skeletorjs
  category: Integration
  display-name: Install OpenClaw on Zo
  tags: openclaw, agent, tailscale, personal-agent, framework
---
# zopenclaw

Install OpenClaw on Zo with Tailscale networking, HTTPS Control UI, and Zo MCP tools.

## Prerequisites

- Zo Computer account
- Tailscale account (free tier)
- LLM API key (Anthropic, OpenAI, OpenRouter)
- Messaging channel token (Telegram bot, Discord bot, or WhatsApp)
- Tailscale Serve enabled on this node

## References

- `references/architecture.md` — Debug why something works; understand two-phase bootstrap
- `references/troubleshooting.md` — Gateway crashes, Tailscale not connecting, port conflicts, workspace limits

## Step 1: Save Tailscale Auth Key (user)

1. Create a reusable auth key at https://login.tailscale.com/admin/settings/keys
2. Save it as secret `TAILSCALE_AUTHKEY` in [Settings > Advanced](/?t=settings&s=advanced)

## Step 2: Install (Zo runs)

```bash
bash /home/workspace/Skills/zopenclaw/scripts/install.sh
supervisorctl -s http://127.0.0.1:29011 restart tailscale
sleep 10 && tailscale status
```

Get the node ID and give the user the Serve enablement link:

```bash
tailscale status --json | jq -r '.Self.ID'
# → tell user to open: https://login.tailscale.com/f/serve?node=<node-id>
```

Do NOT proceed until user confirms Serve is enabled.

## Step 3: OpenClaw Onboard (user)

User runs in Zo terminal:

```bash
openclaw onboard
```

- Pick LLM provider, model, messaging channel
- Do NOT use `--install-daemon` (we use `register_user_service` instead)
- Wait for user to confirm onboarding complete

## Step 4: Bootstrap Gateway (Zo runs)

```bash
bash /home/workspace/Skills/zopenclaw/scripts/bootstrap.sh
```

**Phase 1 — Register gateway without trustedProxies:**

```bash
register_user_service(label="openclaw-gateway", protocol="tcp", local_port=18789, entrypoint="bash -c 'cd /root/.openclaw && exec openclaw gateway run'", workdir="/root/.openclaw")
for i in $(seq 1 20); do openclaw gateway status 2>&1 | grep -qE 'RPC probe: ok|Listening:' && break || sleep 1; done
openclaw devices list
# If pending request: /home/workspace/Skills/zopenclaw/scripts/pairing-helper.sh device <request-id>
```

**Phase 2 — Add trustedProxies and restart:**

```bash
jq '.gateway.trustedProxies = ["127.0.0.1/32"]' ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json
supervisorctl -s http://127.0.0.1:29011 restart openclaw-gateway
```

**Phase 3 — Fix Tailscale Serve if wrong port:**

```bash
tailscale serve status --json | jq .
# If proxy target is NOT 127.0.0.1:18789:
tailscale serve reset && tailscale serve --bg --yes 18789
```

**Phase 4 — Provision HTTPS certificate:**

```bash
TS_HOST=$(tailscale status --json | jq -r '.Self.DNSName' | sed 's/\.$//')
tailscale cert "$TS_HOST"
```

## Step 5: Verify (Zo runs)

```bash
bash /home/workspace/Skills/zopenclaw/scripts/verify.sh
```

Tell user: Control UI is at `https://<tailscale-hostname>` — access ONLY the HTTPS tailnet URL.

If UI says "pairing required": `openclaw devices approve <request-id>`
If Telegram pairing code: `/home/workspace/Skills/zopenclaw/scripts/pairing-helper.sh telegram <PAIRING_CODE>`
If Telegram warns `groupPolicy is "allowlist" but groupAllowFrom is empty`: set `channels.telegram.groupPolicy` to `open` or add sender IDs to `channels.telegram.groupAllowFrom`

## Step 6: Connect Zo Tools via mcporter (Zo runs)

User creates access token at [Settings > Advanced](/?t=settings&s=advanced), saves as secret `ZO_ACCESS_TOKEN`.

```bash
source /root/.zo_secrets
mcporter config add zo https://api.zo.computer/mcp --header "Authorization: Bearer $ZO_ACCESS_TOKEN" --scope home
mcporter list && mcporter call zo.web_search --args '{"query": "test", "time_range": "day"}'
supervisorctl -s http://127.0.0.1:29011 restart openclaw-gateway
```

If `mcporter list` shows zo server and test call returns results, the bridge is working.
