import os
import itertools
import logging
import requests

class PikaVideoGenerator:
    def __init__(self):
        self.api_key = os.getenv("PIKA_API_KEY")
        self.endpoint = os.getenv("PIKA_API_ENDPOINT", "https://api.pika.art/v1/generate")

    def generate(self, prompt, script, music="default", aspect_ratio="9:16"):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "script": script,
            "prompt": prompt,
            "music": music,
            "aspect_ratio": aspect_ratio
        }
        try:
            r = requests.post(self.endpoint, headers=headers, json=payload, timeout=180)
            r.raise_for_status()
            video_url = r.json().get("video_url")
            if not video_url:
                logging.error("No video_url returned from Pika.")
                return None
            video_data = requests.get(video_url, timeout=180).content
            video_path = f"outputs/pika_{abs(hash(prompt+script))}.mp4"
            os.makedirs(os.path.dirname(video_path), exist_ok=True)
            with open(video_path, "wb") as f:
                f.write(video_data)
            logging.info(f"Video saved from Pika: {video_path}")
            return video_path
        except Exception as e:
            logging.error(f"Pika video generation failed: {e}")
            return None

class RunwayVideoGenerator:
    def __init__(self):
        self.api_key = os.getenv("RUNWAY_API_KEY")
        self.endpoint = os.getenv("RUNWAY_API_ENDPOINT", "https://api.runwayml.com/v1/generate")

    def generate(self, prompt, script, music="default", aspect_ratio="9:16"):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "script": script,
            "prompt": prompt,
            "music": music,
            "aspect_ratio": aspect_ratio
        }
        try:
            r = requests.post(self.endpoint, headers=headers, json=payload, timeout=180)
            r.raise_for_status()
            video_url = r.json().get("video_url")
            if not video_url:
                logging.error("No video_url returned from RunwayML.")
                return None
            video_data = requests.get(video_url, timeout=180).content
            video_path = f"outputs/runway_{abs(hash(prompt+script))}.mp4"
            os.makedirs(os.path.dirname(video_path), exist_ok=True)
            with open(video_path, "wb") as f:
                f.write(video_data)
            logging.info(f"Video saved from RunwayML: {video_path}")
            return video_path
        except Exception as e:
            logging.error(f"RunwayML video generation failed: {e}")
            return None

class VideoGenerator:
    def __init__(self):
        self.generators = [PikaVideoGenerator(), RunwayVideoGenerator()]
        self._rr = itertools.cycle(self.generators)

    def generate_video(self, prompt, script, music="default", aspect_ratio="9:16"):
        for _ in range(len(self.generators)):
            generator = next(self._rr)
            video = generator.generate(prompt, script, music, aspect_ratio)
            if video:
                return video
        raise RuntimeError("All video generators failed.")