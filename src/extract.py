import os
import csv
import logging
import requests
from dotenv import load_dotenv
from .utils import setup_logger

setup_logger()
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY or API_KEY == "your_api_key_here":
    raise ValueError("Missing YOUTUBE_API_KEY in .env")

def get_video_categories(api_key: str, region_code: str = "VN") -> dict:
    url = "https://www.googleapis.com/youtube/v3/videoCategories"
    params = {"part": "snippet", "regionCode": region_code, "key": api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])
    return {item["id"]: item["snippet"]["title"] for item in items}

def get_trending_videos(api_key: str, max_results: int = 200, region_code: str = "VN") -> list:
    url = "https://www.googleapis.com/youtube/v3/videos"
    videos = []
    next_page_token = None
    
    while len(videos) < max_results:
        limit = min(50, max_results - len(videos))
        params = {
            "part": "snippet,contentDetails,statistics",
            "chart": "mostPopular",
            "regionCode": region_code,
            "maxResults": limit,
            "key": api_key,
        }
        if next_page_token:
            params["pageToken"] = next_page_token
            
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        items = data.get("items", [])
        videos.extend(items)
        next_page_token = data.get("nextPageToken")
        
        if not next_page_token or not items:
            break
            
    return videos[:max_results]

def extract_pipeline():
    logging.info("Extracting trending YouTube VN...")
    try:
        categories = get_video_categories(API_KEY)
        trending_videos = get_trending_videos(API_KEY, max_results=200)
        
        processed_data = []
        for video in trending_videos:
            snippet = video.get("snippet", {})
            content_details = video.get("contentDetails", {})
            statistics = video.get("statistics", {})
            
            category_id = snippet.get("categoryId", "")
            tags = snippet.get("tags", [])
            
            processed_data.append({
                "video_id": video.get("id", ""),
                "title": snippet.get("title", ""),
                "publishedAt": snippet.get("publishedAt", ""),
                "channelId": snippet.get("channelId", ""),
                "channelTitle": snippet.get("channelTitle", ""),
                "categoryId": category_id,
                "categoryName": categories.get(category_id, "Unknown"),
                "duration": content_details.get("duration", ""),
                "viewCount": statistics.get("viewCount", "0"),
                "likeCount": statistics.get("likeCount", "0"),
                "commentCount": statistics.get("commentCount", "0"),
                "tags": "|".join(tags) if tags else "",
                "thumbnail_link": snippet.get("thumbnails", {}).get("high", {}).get("url", "")
            })
            
        output_path = os.path.join("data", "raw", "youtube_raw.csv")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        fieldnames = list(processed_data[0].keys()) if processed_data else []
        with open(output_path, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_data)
                
        logging.info(f"Saved raw data -> {output_path}")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    extract_pipeline()
