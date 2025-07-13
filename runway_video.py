import os
import logging
import requests

class RunwayVideoGenerator:
    def __init__(self):
        self.api_key = os.getenv("RUNWAY_API_KEY")
        self.endpoint = os.getenv("RUNWAY_API_ENDPOINT", "https://api.runwayml.com/v1/generate")

    def generate(self, prompt, script, music="default", aspect_ratio="9:16"):
        """Generate video using RunwayML API."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "script": script,
            "prompt": prompt,
            "music": music,
            "aspect_ratio": aspect_ratio
        }
        try:
            r = requests.post(self.endpoint, headers=headers, json=payload)
            r.raise_for_status()
            video_url = r.json().get("video_url")
            if not video_url:
                logging.error("No video_url returned from RunwayML.")
                return None
            # Download video
            video_data = requests.get(video_url).content
            video_path = f"outputs/runway_{hash(prompt)}.mp4"
            with open(video_path, "wb") as f:
                f.write(video_data)
            logging.info(f"Video saved from RunwayML: {video_path}")
            return video_path
        except Exception as e:
            logging.error(f"RunwayML video generation failed: {e}")
            return None