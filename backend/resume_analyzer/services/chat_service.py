import os
import requests
from dotenv import load_dotenv

load_dotenv()


def ask_support_bot(message):

    OPENROUTER_KEY = os.getenv(
        "OPENROUTER_API_KEY"
    )

    if not OPENROUTER_KEY:
        return "OpenRouter API key not configured."

    headers = {
        "Authorization":
        f"Bearer {OPENROUTER_KEY}",

        "Content-Type":
        "application/json"
    }

    data = {

        "model":
        "openai/gpt-4o-mini",

        "messages":[

            {
                "role":"system",

                "content":
                """
You are CAMPSPHERE AI Support Assistant.

Help students with:
-placement guidance
-resume analysis
-job recommendations
-platform help
-grievances

Reply short and helpful.
"""
            },

            {
                "role":"user",
                "content":message
            }

        ]
    }

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        print("Chat service error:", e)

        return "Sorry, AI support is unavailable."