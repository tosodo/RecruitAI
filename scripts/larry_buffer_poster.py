#!/usr/bin/env python3
"""
Larry — Buffer Poster
Posts content to LinkedIn via Buffer API.
"""
import json, os, requests, sys, pathlib
from datetime import datetime

BUFFER_API = "https://api.bufferapp.com/1"

def get_token():
    token = os.environ.get("BUFFER_ACCESS_TOKEN", "").strip()
    if not token:
        token_file = pathlib.Path("/home/workspace/.buffer_token")
        if token_file.exists():
            token = token_file.read_text().strip()
    return token

def get_profile_ids(token):
    resp = requests.get(f"{BUFFER_API}/profiles.json?access_token={token}")
    if resp.status_code != 200:
        return None, f"Buffer API error: {resp.status_code}"
    data = resp.json()
    if not data:
        return None, "No Buffer profiles found. Connect LinkedIn to Buffer first."
    return data, None

def get_queue(profile_id, token):
    resp = requests.get(f"{BUFFER_API}/profiles/{profile_id}/updates.json?access_token={token}&count=5")
    return resp.json() if resp.status_code == 200 else []

def post_to_buffer(profile_id, token, text, media_url=None):
    payload = {
        "access_token": token,
        "profile_ids[]": profile_id,
        "text": text,
        "top": "true",
    }
    if media_url:
        payload["media[link]"] = media_url
    resp = requests.post(f"{BUFFER_API}/updates/create.json", data=payload)
    return (True, resp.json()) if resp.status_code == 200 else (False, f"Error {resp.status_code}")

def main():
    if "--setup" in sys.argv:
        print("\n=== Larry Buffer Setup ===")
        print("1. Go to https://buffer.com/developers → Create App")
        print("2. Get Access Token")
        print("3. Save token to Settings > Advanced as secret BUFFER_ACCESS_TOKEN")
        print("   OR: echo 'TOKEN' > /home/workspace/.buffer_token")
        print("4. Ensure LinkedIn is connected in Buffer")
        print("============================\n")
        return

    token = get_token()
    if not token:
        print("No Buffer token. Run with --setup for instructions.")
        return

    profiles, err = get_profile_ids(token)
    if err:
        print(f"Error: {err}")
        return

    linkedin_id = None
    for p in profiles:
        svc = p.get("service", "").lower()
        if "linkedin" in svc:
            linkedin_id = p["id"]
            break
    if not linkedin_id:
        linkedin_id = profiles[0]["id"]

    print(f"[Larry] Buffer connected → {profiles[0].get('formatted_username', 'unknown')}")

    if "--status" in sys.argv:
        queue = get_queue(linkedin_id, token)
        print(f"[Larry] Queue: {len(queue)} pending posts")
        for u in queue[:5]:
            print(f"  - {u.get('text','')[:80]}...")
        return

    if "--dry-run" in sys.argv:
        posts_dir = pathlib.Path("/home/workspace/data/content")
        files = sorted(posts_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        if files:
            print(f"[Larry] Would post:\n{files[0].read_text()[:300]}...")
        return

    posts_dir = pathlib.Path("/home/workspace/data/content")
    files = sorted(posts_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        print("No content. Run larry_content_generate.py first.")
        return

    content = files[0].read_text()
    parts = content.split("\n---\n")
    body = parts[-1].strip() if len(parts) > 1 else content.strip()

    print(f"[Larry] Posting to LinkedIn via Buffer...")
    success, result = post_to_buffer(linkedin_id, token, body)
    if success:
        print(f"✅ Posted! Update ID: {result.get('update_id', 'N/A')}")
        new_name = files[0].stem + "-sent.md"
        files[0].rename(files[0].parent / new_name)
    else:
        print(f"❌ Failed: {result}")

if __name__ == "__main__":
    main()
