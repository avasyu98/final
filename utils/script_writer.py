import os
import requests
import json
import re
import logging

def generate_script_and_prompt(trend_title, trend_description):
    """Uses Gemini API to generate a 3-scene script and a visual prompt for video generation."""
    api_key = os.getenv("GEMINI_API_KEY")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{
            "parts": [{
                "text": (
                    f"Given the trending topic: \"{trend_title}\".\n"
                    f"Description: {trend_description}\n"
                    "Write a 3-scene short video script (with scene headings and dialogue) suitable for a hyperrealistic social media video. "
                    "Also provide a concise visual description prompt for AI video generation, focusing on the overall look and mood."
                    "\nRespond in this JSON format:\n"
                    "{\n"
                    "  \"script\": \"...\",\n"
                    "  \"prompt\": \"...\"\n"
                    "}"
                )
            }]
        }]
    }
    params = {"key": api_key}
    try:
        r = requests.post(endpoint, headers=headers, json=body, params=params, timeout=60)
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("Gemini did not return a valid JSON response")
    except Exception as e:
        logging.error(f"Gemini script generation failed: {e}")
        return {"script": "", "prompt": ""}