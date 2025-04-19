"""
Comment generation service using DeepSeek Chat API.
"""

import random
from typing import Dict
import aiohttp
from app.config import (
    DEEPSEEK_API_KEY, DEEPSEEK_CHAT_URL, 
    CHAT_MODEL, FALLBACK_COMMENTS, POSTED_COMMENTS
)


async def make_comment(p: Dict) -> str:
    """
    Build prompts, call DeepSeek‑Chat, enforce length & uniqueness.
    """
    # -- greeting fallback if minimal info ----------------------------
    if not (p.get("text") or p.get("mediaDesc")):
        return f"Hey @{p['username']}! 👋"

    # -- build user prompt -------------------------------------------
    u = f"POST by @{p['username']} (ID {p['postId']}):\n"
    if p.get("text"):
        u += f'Text: "{p["text"]}"\n'
    if p.get("mediaDesc"):
        u += f'Media: "{p["mediaDesc"]}"\n'
    if p.get("hashtags"):
        u += "Hashtags: " + ", ".join(p["hashtags"]) + "\n"
    if p["isReply"] and p["parentContent"]:
        pc = p["parentContent"]
        u += f'Replying to @{pc["username"]}: "{pc["text"]}"\n'
    u += """
Write ONE casual reply (<=10 words) that references the post.
Add exactly ONE emoji. Output only the comment string.
DO NOT use quotes around your response.
"""

    sys = "You are Ava, a witty 20‑something woman replying on Threads."

    # -- call DeepSeek‑Chat ------------------------------------------
    if not DEEPSEEK_API_KEY:
        print("DEBUG: No API key found, using fallback comment")
        return random.choice(FALLBACK_COMMENTS)

    print(f"DEBUG: Attempting API call to DeepSeek with key: {DEEPSEEK_API_KEY[:5]}...")
    
    try:
        async with aiohttp.ClientSession() as s:
            r = await s.post(
                DEEPSEEK_CHAT_URL,
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": CHAT_MODEL,
                    "messages": [
                        {"role": "system", "content": sys},
                        {"role": "user",   "content": u},
                    ],
                    "max_tokens": 60,
                    "temperature": 0.9,
                    "top_p": 0.95,
                    "frequency_penalty": 1.5,
                    "presence_penalty": 1.5,
                },
                timeout=60
            )
            js = await r.json()
            print(f"DEBUG: API response status: {r.status}")
            print(f"DEBUG: API response body: {js}")

        comment = (js.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                    .strip())

        # Strip any quotes from the comment
        comment = comment.strip('"\'')

        if not comment:
            print("DEBUG: Empty comment from API, using fallback")
            comment = random.choice(FALLBACK_COMMENTS)

        # duplicate guard (per session)
        if comment in POSTED_COMMENTS.values():
            comment += random.choice([" ✨", " 🔥", " 🙌"])
        POSTED_COMMENTS[p["postId"]] = comment

        return " ".join(comment.split())[:80]
    
    except Exception as e:
        print(f"DEBUG: API call error: {str(e)}")
        return random.choice(FALLBACK_COMMENTS) 