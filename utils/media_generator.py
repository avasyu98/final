import os
import requests
import logging
from datetime import datetime

def generate_image(prompt, topic):
    api_key = os.getenv("STABILITY_API_KEY")
    endpoint = os.getenv("STABILITY_API_ENDPOINT")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "output_format": "png"
    }
    try:
        r = requests.post(endpoint, headers=headers, json=payload)
        if r.status_code == 200:
            img_data = r.content
            img_path = f"outputs/{topic['title'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            with open(img_path, "wb") as f:
                f.write(img_data)
            logging.info(f"Image saved to {img_path}")
            return img_path
        else:
            logging.error(f"Image generation failed: {r.text}")
            return None
    except Exception as e:
        logging.error(f"Image generation error: {e}")
        return None

def generate_video(prompt, topic):
    # Placeholder: Replace with actual video API integration when available
    vid_path = f"outputs/{topic['title'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
    # For now, just create an empty file as placeholder
    os.makedirs(os.path.dirname(vid_path), exist_ok=True)
    with open(vid_path, "wb") as f:
        f.write(b"")
    logging.info(f"Video (placeholder) saved to {vid_path}")
    return vid_path