"""
Comment generation service using DeepSeek Chat API.
"""

import random
import re
import base64
from typing import Dict
import aiohttp
from app.config import (
    DEEPSEEK_API_KEY, DEEPSEEK_CHAT_URL, DEEPSEEK_VISION_URL,
    CHAT_MODEL, VISION_MODEL, FALLBACK_COMMENTS, EVENT_FALLBACK_COMMENTS, POSTED_COMMENTS
)


def is_event_related(text: str, media_desc: str = None) -> bool:
    """
    Determine if content is event-related based on keywords.
    """
    event_keywords = [
        'concert', 'show', 'performing', 'performance', 'stage', 'tour', 'festival',
        'live', 'lineup', 'tickets', 'venue', 'gig', 'band', 'artist', 'music', 
        'event', 'arena', 'stadium', 'theater', 'theatre', 'hall', 'sold out',
        'tour dates', 'on sale', 'presale', 'vip', 'backstage', 'exclusive'
    ]
    
    # Check text content
    content = (text or '').lower() + ' ' + (media_desc or '').lower()
    
    # Return True if any keyword is in the content
    return any(keyword in content for keyword in event_keywords)


async def process_image(image_base64: str) -> str:
    """
    Process image using DeepSeek Vision API and return description.
    """
    try:
        # Call Vision API
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                DEEPSEEK_VISION_URL,
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": VISION_MODEL,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Describe this image in detail, focusing on the main subject, actions, and emotions. Be specific but concise."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 300
                }
            )
            
            if response.status != 200:
                print(f"DEBUG: Vision API error: {response.status}")
                return None
                
            result = await response.json()
            description = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            return description.strip()
            
    except Exception as e:
        print(f"DEBUG: Image processing error: {str(e)}")
        return None


async def make_comment(p: Dict) -> str:
    """
    Build prompts, call DeepSeek‑Chat, enforce length & uniqueness.
    """
    # -- greeting fallback if minimal info ----------------------------
    if not (p.get("text") or p.get("mediaDesc") or p.get("imageBase64")):
        return f"Hey @{p['username']}! 👋"

    # -- process image if present ------------------------------------
    image_description = None
    if p.get("imageBase64"):
        print("DEBUG: Processing image...")
        image_description = await process_image(p["imageBase64"])
        if image_description:
            print(f"DEBUG: Image description: {image_description}")

    # -- build user prompt -------------------------------------------
    u = f"POST by @{p['username']} (ID {p['postId']}):\n"
    if p.get("text"):
        u += f'Text: "{p["text"]}"\n'
    if image_description:
        u += f'Image Description: "{image_description}"\n'
    elif p.get("mediaDesc"):
        u += f'Media: "{p["mediaDesc"]}"\n'
    if p.get("hashtags"):
        u += "Hashtags: " + ", ".join(p["hashtags"]) + "\n"
    if p["isReply"] and p["parentContent"]:
        pc = p["parentContent"]
        u += f'Replying to @{pc["username"]}: "{pc["text"]}"\n'
    u += """
Write ONE casual reply (<=10 words) that references the post and image if present.
Add exactly ONE emoji. Output only the comment string.
DO NOT use quotes around your response.
"""

    sys = "You are Ava, a witty 20‑something woman replying on Threads."

    # -- detect if content is event-related --------------------------
    is_event = is_event_related(p.get("text", ""), p.get("mediaDesc", ""))
    
    # -- call DeepSeek‑Chat ------------------------------------------
    if not DEEPSEEK_API_KEY:
        print("DEBUG: No API key found, using fallback comment")
        if is_event:
            return random.choice(EVENT_FALLBACK_COMMENTS)
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
            if is_event:
                comment = random.choice(EVENT_FALLBACK_COMMENTS)
            else:
                comment = random.choice(FALLBACK_COMMENTS)

        # duplicate guard (per session)
        if comment in POSTED_COMMENTS.values():
            comment += random.choice([" ✨", " 🔥", " 🙌"])
        POSTED_COMMENTS[p["postId"]] = comment

        return " ".join(comment.split())[:80]
    
    except Exception as e:
        print(f"DEBUG: API call error: {str(e)}")
        if is_event:
            return random.choice(EVENT_FALLBACK_COMMENTS)
        return random.choice(FALLBACK_COMMENTS) 