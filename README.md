# Vietnam YouTube Trending Analytics Pipeline

## Overview
This project collects the top 200 trending YouTube videos in Vietnam using the YouTube Data API, processes the data with Python (Pandas), and visualizes video performance and engagement in Power BI.

The pipeline automates data extraction, transformation, and report generation for trend analysis.

## Dashboard

### 1. General Overview
![Overview Dashboard](dashboard/dashboard_page1.png)

### 2. Creator & Hashtag Intelligence
![Creator & Hashtag Intelligence](dashboard/dashboard_page2.png)

## Technology Stack
- **Language**: Python 3.x
- **Libraries**: `pandas`, `google-api-python-client`, `isodate`, `python-dotenv`
- **API**: YouTube Data API v3
- **BI Tool**: Power BI Desktop
- **Version Control**: Git / GitHub

## Data Pipeline

### 1. Extract
- Fetch the top 200 trending videos in Vietnam from the YouTube Data API.

### 2. Transform
- Clean and validate data.
- Convert ISO 8601 duration into seconds.
- Calculate engagement rate.
- Group videos by duration.
- Extract hashtags into a separate dataset.

### 3. Load
- Export processed CSV files and refresh the Power BI dashboard.

## Getting Started

1. **Clone this repository**:
   ```bash
   git clone https://github.com/Tthoong129/Youtube_Analyst.git
   cd Youtube_Analyst
   ```

2. **Set up virtual environment & install dependencies**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   pip install -r requirements.txt
   ```

3. **Configure API Key**:
   - Create a `.env` file in the root directory.
   - Add your API Key: `YOUTUBE_API_KEY=your_api_key_here`

4. **Run the ETL Pipeline**:
   ```bash
   python run_pipeline.py
   ```
   *(This will fetch the latest trending data and update the CSV files).*

5. **View Dashboard**:
   - Open `dashboard/Youtube_Trending_Dashboard.pbix` in Power BI Desktop.
   - Click **Refresh** to load the newly generated local data.

## License
This project is for educational and portfolio purposes. Data is fetched using the official YouTube API.
