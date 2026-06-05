import logging
from src.extract import extract_pipeline
from src.clean import transform_pipeline
from src.process_hashtags import process_hashtags_pipeline
from src.export_excel import create_excel_report
from src.utils import setup_logger

def main():
    setup_logger()
    logging.info("=== BẮT ĐẦU CHẠY PIPELINE ===")
    
    try:
        extract_pipeline()
        transform_pipeline()
        process_hashtags_pipeline()
        create_excel_report()
        
        logging.info("=== PIPELINE HOÀN TẤT THÀNH CÔNG ===")
    except Exception as e:
        logging.error(f"Pipeline thất bại: {e}")

if __name__ == "__main__":
    main()
