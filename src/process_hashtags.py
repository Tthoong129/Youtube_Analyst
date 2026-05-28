import os
import logging
import pandas as pd
from .utils import setup_logger

setup_logger()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def process_hashtags_pipeline():
    input_path = os.path.join(BASE_DIR, "data", "processed", "youtube_clean.csv")
    output_path = os.path.join(BASE_DIR, "data", "processed", "hashtag_performance.csv")
    
    if not os.path.exists(input_path):
        logging.error(f"File not found: {input_path}")
        return

    logging.info("Processing hashtags for BI...")
    df_clean = pd.read_csv(input_path)
    
    df_tags = df_clean[['video_id', 'tags', 'viewCount', 'likeCount', 'commentCount', 'engagement_rate']].copy()
    df_tags['tag'] = df_tags['tags'].str.split('|')
    df_exploded = df_tags.explode('tag')
    df_exploded = df_exploded[df_exploded['tag'].astype(str).str.strip() != '']
    df_exploded['tag'] = df_exploded['tag'].astype(str).str.lower().str.strip()
    
    hashtag_perf = df_exploded.groupby('tag').agg(
        Total_Videos=('video_id', 'count'),
        Total_Views=('viewCount', 'sum'),
        Total_Likes=('likeCount', 'sum'),
        Total_Comments=('commentCount', 'sum'),
        Avg_Engagement_Rate=('engagement_rate', 'mean')
    ).reset_index()
    
    hashtag_perf = hashtag_perf[hashtag_perf['Total_Videos'] >= 2]
    hashtag_perf = hashtag_perf.sort_values('Total_Views', ascending=False)
    
    hashtag_perf.to_csv(output_path, index=False, encoding="utf-8-sig")
    logging.info(f"Saved hashtag data -> {output_path}")

if __name__ == "__main__":
    process_hashtags_pipeline()
