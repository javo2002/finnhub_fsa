import pandas as pd
import logging
import schedule
import time

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sentiment_data_df.log'),
        logging.StreamHandler()
    ]
)

# Create a logger
logger = logging.getLogger(__name__)


# Function to read CSV and log information
def log_csv_info():
    try:
        # Replace the path with your actual file path
        file_path = 'news_data_with_sentiments.csv'
        df = pd.read_csv(file_path)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        # Log DataFrame info
        logger.info(f'{df}')

    except Exception as e:
        logger.error(f'Failed to read and log CSV file: {e}')


# Run the scheduler
if __name__ == "__main__":
   log_csv_info()