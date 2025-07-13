import os
import time
import logging
from utils.news_fetcher import fetch_trending_news
from utils.script_writer import generate_script_and_prompt
from utils.video_generator import VideoGenerator
from utils.social_poster import schedule_post

logging.basicConfig(level=logging.INFO)

def main():
    # Fetch trending news/topics
    trends = fetch_trending_news()
    if not trends:
        logging.warning("No trends fetched.")
        return

    video_gen = VideoGenerator()

    for trend in trends:
        logging.info(f"Processing trend: {trend['title']}")
        script_data = generate_script_and_prompt(trend['title'], trend['description'])
        script = script_data.get("script", "")
        prompt = script_data.get("prompt", "")

        if not script or not prompt:
            logging.warning(f"Skipping trend due to failed script generation: {trend['title']}")
            continue

        video_path = video_gen.generate_video(prompt, script)
        if not video_path:
            logging.warning(f"Video generation failed for trend: {trend['title']}")
            continue

        # Assume you have an image path if you want to post an image as well, else set img_path to None
        img_path = None  # Set this if you generate an image
        schedule_post(img_path, video_path, trend)
        logging.info(f"Posted video for trend: {trend['title']}")
        time.sleep(2)  # To avoid spamming APIs

if __name__ == "__main__":
    main()