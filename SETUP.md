# Additional Setups for Real Social Posting

## 1. Meta (Instagram/Facebook) Setup

- Create a Facebook App at https://developers.facebook.com/apps/
- Get your Facebook Page ID (`FB_PAGE_ID`).
- Convert your Instagram account to a Business or Creator account, link it to your Facebook Page, and get the Instagram User ID (`IG_USER_ID`).
- Get a long-lived Page access token (`META_ACCESS_TOKEN`) with the permissions:
  - `pages_show_list`
  - `pages_read_engagement`
  - `pages_manage_posts`
  - `instagram_basic`
  - `instagram_content_publish`
  - `pages_read_user_content`

**Meta Docs:**  
- [Instagram Graph API Getting Started](https://developers.facebook.com/docs/instagram-api/getting-started)
- [Instagram Content Publishing](https://developers.facebook.com/docs/instagram-api/guides/content-publishing/)

## 2. YouTube Data API Setup

- Go to [Google Cloud Console](https://console.developers.google.com/).
- Enable "YouTube Data API v3" for your project.
- Create OAuth2 credentials:
  - Get `YOUTUBE_CLIENT_ID` and `YOUTUBE_CLIENT_SECRET`.
- Authorize your app and save the `YOUTUBE_ACCESS_TOKEN` and `YOUTUBE_REFRESH_TOKEN`.
- You can use the [YouTube API Quickstart](https://developers.google.com/youtube/v3/quickstart/python) to obtain and save your tokens.

## 3. ImgBB Setup (for public image URLs)

- Register at [imgbb.com](https://imgbb.com/) and get your API key (`IMGBB_API_KEY`).
- This is required so Instagram and Facebook can get a public URL to your images.

## 4. Running the App

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Fill out your `.env` file with all the required secrets and keys.
3. Launch your bot:
   ```
   python main.py
   ```

---