# Import libraries
from dotenv import load_dotenv
from datetime import datetime
import os
import logging

# Import modules
from modules.amplitude_date_range import amplitude_date_range
from modules.amplitude_api_call import amplitude_api_call
from modules.amplitude_zip_file_extract import  amplitude_zip_file_extract
from modules.amplitude_s3_load import amplitude_s3_load

# CONFIGURE LOGGING
# Define runtime timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

# Create log directories if they do not exist
os.makedirs('logs/date_range', exist_ok=True)
os.makedirs('logs/api_call', exist_ok=True)
os.makedirs('logs/zip_file_extract', exist_ok=True)
os.makedirs('logs/s3_load', exist_ok=True)

# Configure Logging for amplitude_date_range.py
date_range_logger = logging.getLogger('modules.amplitude_date_range')
date_range_logger.setLevel(logging.INFO)
date_range_handler = logging.FileHandler(f'logs/date_range/{timestamp}_date_range.log', encoding='utf-8')
date_range_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
date_range_logger.addHandler(date_range_handler)
date_range_logger.propagate = False 

# Configure Logging for amplitude_api_call.py
api_call_logger = logging.getLogger('modules.amplitude_api_call')
api_call_logger.setLevel(logging.INFO)
api_call__handler = logging.FileHandler(f'logs/api_call/{timestamp}_api_call.log', encoding='utf-8')
api_call__handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
api_call_logger.addHandler(api_call__handler)
api_call_logger.propagate = False 

# Configure Logging for amplitude_zip_file_extract.py
zip_file_extract_logger = logging.getLogger('modules.amplitude_zip_file_extract')
zip_file_extract_logger.setLevel(logging.INFO)
zip_file_extract__handler = logging.FileHandler(f'logs/zip_file_extract/{timestamp}_zip_file_extract.log', encoding='utf-8')
zip_file_extract__handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
zip_file_extract_logger.addHandler(zip_file_extract__handler)
zip_file_extract_logger.propagate = False 

# Configure Logging for amplitude_s3_load.py
s3_load_logger = logging.getLogger('modules.amplitude_s3_load')
s3_load_logger.setLevel(logging.INFO)
s3_load__handler = logging.FileHandler(f'logs/s3_load/{timestamp}_s3_load.log', encoding='utf-8')
s3_load__handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
s3_load_logger.addHandler(s3_load__handler)
s3_load_logger.propagate = False 

# Generate start_time, end_time with custom function
start_time, end_time = amplitude_date_range('days', 1)

# Load .env file
load_dotenv()

# Assign AMP keys to variables
AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')
# logger.info('API key and secret imported from .env file.')

# Assign AWS keys to variables
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
# logger.info('API key, secret and bucket name imported from .env file.')

# Declare url for API call function
url = 'https://analytics.eu.amplitude.com/api/2/export'

# Amplitude API call in try/except block using custom function. Prints exception error if function fails.
try:
    download_success = amplitude_api_call(
        url = url
        , start_time = start_time
        , end_time = end_time
        , AMP_API_KEY = AMP_API_KEY
        , AMP_SECRET_KEY = AMP_SECRET_KEY
        , max_attempts=3
        )
    print(f'Data files for range {start_time}-{end_time} downloaded into "downloaded_data" folder.')
    
except Exception as e:
    print(f"Amplitude file download failed: {e}")
    # logger.error(f"Extraction failed: {e}")

# Logic to only run zip extract function if files successfully downloaded from Amplitude
if download_success == True:

    # Call custom zip extract function. Prints exception error if function fails.
    try:
        # logger.info("Starting nested zip file extraction...")
        extract_success = amplitude_zip_file_extract('downloaded_data')
        print('Files successfully extracted from extracted .zip files')
        # logger.info("Extraction complete.")

    except Exception as e:
        print(f".zip file extraction failed: {e}")
        # logger.error(f"Extraction failed: {e}")

else:
    print("Data download was unsuccessful. Review logs and try again.")
    # logger.info(f'Data download was unsuccessful so no data was extracted.')

# Logic to only run s3 load function if files successfully extracted nested .zip files
if extract_success == True:

    # Call s3 file upload function. Prints exception error if function fails.
    try:
        # logger.info("Starting nested zip file extraction...")
        amplitude_s3_load('extracted_data', AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET_NAME)
        print('S3 load process is complete.')
        # logger.info('S3 load process is complete.')

    except Exception as e:
        print(f"S3 load process has failed: {e}")
        # logger.error(f"Extraction failed: {e}")

else: 
    print("Data download was unsuccessful. Review logs and try again.")
    # logger.info(f'Data download was unsuccessful so no data was extracted.')