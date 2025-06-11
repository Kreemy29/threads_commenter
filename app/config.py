"""
Configuration for the comment service application.
Loads environment variables from .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")  # TODO: Add your API key to .env file
print(f"API Key loaded: {'Key found (not showing for security)' if DEEPSEEK_API_KEY else 'No key found!'}")

# API URLs
DEEPSEEK_CHAT_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_VISION_URL = "https://api.deepseek.com/v1/chat/completions"  # same base URL

# Model names
CHAT_MODEL = "deepseek-chat"
VISION_MODEL = "deepseek-vision"

# Regular fallback responses when API is unavailable
FALLBACK_COMMENTS = [
    "Main‑character energy ✨", "Love this vibe 😍", "Absolute fire 🔥",
    "Gym goals! 💪", "Chef's kiss 😘", "Instant mood‑boost 💯"
]

# Event-specific fallback responses (more baity/engaging)
EVENT_FALLBACK_COMMENTS = [
    "This is gonna be THE event of the year! 🔥",
    "Need tickets ASAP! Who's coming with? 🎟️",
    "I'd literally sell a kidney to be there! 🤩",
    "Just dropped everything to get tickets! 🎵",
    "My FOMO is through the roof right now! 😭",
    "No way I'm missing this! Who has the link? 🎤",
    "Had goosebumps just reading about this! 💯",
    "The energy at these shows is UNMATCHED! ⚡",
    "Stop everything and get tickets NOW! 🚨",
    "Their last show sold out in 2 min... setting alarms! ⏰"
]

# In-memory storage for session-level duplicate prevention
POSTED_COMMENTS = {} 