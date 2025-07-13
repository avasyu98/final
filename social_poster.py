import os
import logging
import requests

# Meta/Instagram/Facebook
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
IG_USER_ID = os.getenv("IG_USER_ID")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# YouTube
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
YOUTUBE_ACCESS_TOKEN = os.getenv("YOUTUBE_ACCESS_TOKEN")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def upload_image_to_imgbb(image_path):
    if not IMGBB_API_KEY:
        logging.error("IMGBB_API_KEY not set in .env for image hosting.")
        return None
    with open(image_path, "rb") as f:
        img_data = f.read()
    imgbb_url = "https://api.imgbb.com/1/upload"
    resp = requests.post(imgbb_url, params={"key": IMGBB_API_KEY}, files={"image": img_data})
    if resp.status_code != 200:
        logging.error(f"Failed to upload image to imgbb: {resp.text}")
        return None
    return resp.json()['data']['url']

def post_to_instagram(image_path, caption):
    if not IG_USER_ID or not META_ACCESS_TOKEN:
        logging.warning("Instagram credentials not set.")
        return
    image_url = upload_image_to_imgbb(image_path)
    if not image_url:
        return
    url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    upload_payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": META_ACCESS_TOKEN
    }
    resp = requests.post(url, data=upload_payload)
    if resp.status_code != 200:
        logging.error(f"Instagram media upload failed: {resp.text}")
        return
    creation_id = resp.json().get("id")
    if not creation_id:
        logging.error("No creation_id returned from Instagram upload.")
        return
    publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    publish_payload = {
        "creation_id": creation_id,
        "access_token": META_ACCESS_TOKEN
    }
    resp = requests.post(publish_url, data=publish_payload)
    if resp.status_code != 200:
        logging.error(f"Instagram publish failed: {resp.text}")
        return
    logging.info(f"Posted image to Instagram: {resp.json()}")

def post_to_facebook(image_path, caption):
    if not FB_PAGE_ID or not META_ACCESS_TOKEN:
        logging.warning("Facebook credentials not set.")
        return
    image_url = upload_image_to_imgbb(image_path)
    if not image_url:
        return
    url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"
    payload = {
        "url": image_url,
        "caption": caption,
        "access_token": META_ACCESS_TOKEN
    }
    resp = requests.post(url, data=payload)
    if resp.status_code != 200:
        logging.error(f"Facebook photo post failed: {resp.text}")
        return
    logging.info(f"Posted image to Facebook: {resp.json()}")

def post_to_youtube(video_path, title, description):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = Credentials(
        token=YOUTUBE_ACCESS_TOKEN,
        refresh_token=YOUTUBE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=YOUTUBE_CLIENT_ID,
        client_secret=YOUTUBE_CLIENT_SECRET
    )
    youtube = build('youtube', 'v3', credentials=creds)
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["shorts", "trending"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    }
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            logging.info(f"Uploading to YouTube: {int(status.progress() * 100)}%")
    logging.info(f"Posted video to YouTube: {response['id']}")

def schedule_post(img_path, vid_path, topic):
    caption = f"Trending: {topic['title']}\n\n{topic.get('description', '')}"
    if img_path:
        post_to_instagram(img_path, caption)
        post_to_facebook(img_path, caption)
    if vid_path and os.path.getsize(vid_path) > 0:
        post_to_youtube(vid_path, topic['title'], caption)