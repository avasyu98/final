# Automated Trend-based Social Video Generator

## Overview

This project fetches trending news, generates a 3-scene script and visual prompt with Gemini AI, creates a hyperrealistic video using Pika Labs and RunwayML (with automatic load balancing), and posts the result to Instagram, Facebook, and YouTube.

## Requirements

- Python 3.8+
- API keys/tokens for: NewsAPI, Google Gemini, Pika Labs, RunwayML, YouTube, Meta (Facebook/Instagram), ImgBB

## Quickstart

1. **Fill out `.env`** with all required API keys and credentials.
2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
3. **Run the pipeline:**
    ```sh
    python main.py
    ```

## Directory Structure

- `main.py` - Main pipeline script
- `utils/news_fetcher.py` - Fetch trending news/articles
- `utils/script_writer.py` - Gemini-powered script & prompt generator
- `utils/video_generator.py` - Video generation and load balancing
- `utils/social_poster.py` - Social media upload logic

## Environment Variables

See `.env` for all required keys.

## Notes

- Logging is enabled by default.
- Extendable to more trend sources, more video backends, more platforms.
- All video and API failures are logged.