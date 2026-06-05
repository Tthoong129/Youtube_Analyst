import os
import logging
import pandas as pd
import xlsxwriter
from .utils import setup_logger

setup_logger()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_excel_report():
    input_file = os.path.join(BASE_DIR, "data", "processed", "youtube_clean.csv")
    if not os.path.exists(input_file):
        logging.error(f"File not found: {input_file}")
        return

    logging.info(f"Loading {input_file}...")
    df = pd.read_csv(input_file)
    
    os.makedirs(os.path.join(BASE_DIR, "reports"), exist_ok=True)
    output_file = os.path.join(BASE_DIR, "reports", "Youtube_Operations_Report.xlsx")
    
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    workbook = writer.book
    
    fmt_header = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#2C3E50',
        'font_color': 'white',
        'border': 1
    })
    
    fmt_num = workbook.add_format({'num_format': '#,##0'})
    fmt_pct = workbook.add_format({'num_format': '0.00%'})
    
    df.to_excel(writer, sheet_name='Master Data', index=False)
    ws_master = writer.sheets['Master Data']
    
    ws_master.autofilter(0, 0, len(df), len(df.columns) - 1)
    ws_master.freeze_panes(1, 0)
    
    for col_num, value in enumerate(df.columns.values):
        ws_master.write(0, col_num, value, fmt_header)
        
    ws_master.set_column('A:A', 15)
    ws_master.set_column('B:B', 50)
    ws_master.set_column('G:G', 20)
    ws_master.set_column('I:I', 15)
    
    view_idx = df.columns.get_loc('viewCount')
    comment_idx = df.columns.get_loc('commentCount')
    engagement_idx = df.columns.get_loc('engagement_rate')
    
    ws_master.set_column(view_idx, comment_idx, 15, fmt_num)
    ws_master.set_column(engagement_idx, engagement_idx+2, 12, fmt_pct)
    
    summary_df = df.groupby('categoryName').agg(
        Total_Videos=('video_id', 'count'),
        Avg_Views=('viewCount', 'mean'),
        Avg_Likes=('likeCount', 'mean'),
        Avg_Engagement_Rate=('engagement_rate', 'mean')
    ).reset_index().sort_values(by='Total_Videos', ascending=False)
    
    summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
    ws_summary = writer.sheets['Executive Summary']
    
    for col_num, value in enumerate(summary_df.columns.values):
        ws_summary.write(0, col_num, value, fmt_header)
        
    ws_summary.set_column('A:A', 20)
    ws_summary.set_column('B:B', 15, fmt_num)
    ws_summary.set_column('C:D', 15, fmt_num)
    ws_summary.set_column('E:E', 25, fmt_pct)
    
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
        'name':       ['Executive Summary', 0, 2],
        'categories': ['Executive Summary', 1, 0, len(summary_df), 0],
        'values':     ['Executive Summary', 1, 2, len(summary_df), 2],
        'fill':       {'color': '#3498DB'},
    })
    chart.set_title({'name': 'Average Views by Category'})
    chart.set_x_axis({'name': 'Category'})
    chart.set_y_axis({'name': 'Average Views'})
    ws_summary.insert_chart('G2', chart)
    
    writer.close()
    logging.info(f"Saved -> {output_file}")

if __name__ == "__main__":
    create_excel_report()
