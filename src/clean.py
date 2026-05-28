import os
import re
import logging
import pandas as pd
import emoji
from .utils import setup_logger, parse_duration, get_duration_bucket

setup_logger()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def transform_pipeline():
    input_path  = os.path.join(BASE_DIR, "data", "raw", "youtube_raw.csv")
    output_path = os.path.join(BASE_DIR, "data", "processed", "youtube_clean.csv")
    
    if not os.path.exists(input_path):
        logging.error(f"File not found: {input_path}")
        return

    logging.info("Cleaning youtube_raw.csv...")
    df = pd.read_csv(input_path)
    
    df = df.drop_duplicates(subset=["video_id"]).copy()
    
    for col in ["viewCount", "likeCount", "commentCount"]:
        df[col] = df[col].fillna(0).astype(int)
        
    df = df[df["viewCount"] > 0].copy()
    
    df["publishedAt"] = pd.to_datetime(df["publishedAt"])
    df["publishedAt_vn"] = df["publishedAt"].dt.tz_convert('Asia/Ho_Chi_Minh')
    df["publish_date"] = df["publishedAt_vn"].dt.date
    df["publish_hour"] = df["publishedAt_vn"].dt.hour
    df["day_of_week"] = df["publishedAt_vn"].dt.day_name()
    
    now = pd.Timestamp.now(tz='Asia/Ho_Chi_Minh')
    df["days_since_published"] = (now - df["publishedAt_vn"]).dt.days
    
    df["duration_sec"] = df["duration"].apply(parse_duration)
    df = df[df["duration_sec"] > 0].copy()
    df["duration_bucket"] = df["duration_sec"].apply(get_duration_bucket)
    
    df["engagement_rate"] = (df["likeCount"] + df["commentCount"]) / df["viewCount"]
    df["like_rate"] = df["likeCount"] / df["viewCount"]
    df["comment_rate"] = df["commentCount"] / df["viewCount"]
    
    df["tags"] = df["tags"].fillna("")
    df["tag_count"] = df["tags"].apply(lambda x: len(str(x).split("|")) if str(x).strip() else 0)
    
    df["title"] = df["title"].fillna("")
    df["title_length"] = df["title"].apply(len)
    df["has_number_in_title"] = df["title"].apply(lambda x: bool(re.search(r'\d', x)))
    df["has_emoji"] = df["title"].apply(lambda x: emoji.emoji_count(x) > 0)
    
    cols = [
        "video_id", "title", "title_length", "has_number_in_title", "has_emoji",
        "channelId", "channelTitle", "categoryId", "categoryName",
        "publishedAt_vn", "publish_date", "publish_hour", "day_of_week", "days_since_published",
        "duration", "duration_sec", "duration_bucket",
        "viewCount", "likeCount", "commentCount", 
        "engagement_rate", "like_rate", "comment_rate",
        "tags", "tag_count", "thumbnail_link"
    ]
    df_clean = df[[c for c in cols if c in df.columns]]
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_clean.to_csv(output_path, index=False, encoding="utf-8-sig")
    logging.info(f"Saved cleaned data -> {output_path}")

if __name__ == "__main__":
    transform_pipeline()
