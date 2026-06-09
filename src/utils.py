import re
import logging
import pandas as pd

def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_duration(x):
    # Parse ISO 8601 duration
    if pd.isna(x): 
        return 0
    pattern = re.compile(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(x)
    if not match:
        return 0
    days, hours, minutes, seconds = match.groups()
    
    total = 0
    if days: total += int(days) * 86400
    if hours: total += int(hours) * 3600
    if minutes: total += int(minutes) * 60
    if seconds: total += int(seconds)
    return total

def get_duration_bucket(sec):
    # Bucket durations and return both bucket name and its sort order
    if sec < 60: return "< 1 min", 1
    if sec < 180: return "1-3 mins", 2
    if sec < 300: return "3-5 mins", 3
    if sec < 600: return "5-10 mins", 4
    if sec < 1800: return "10-30 mins", 5
    return "> 30 mins", 6
