# Import libraries
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Import modules
from modules import amplitude_date_range, amplitude_api_call, amplitude_zip_file_extract, amplitude_s3_load

# Generate start_time, end_time with custom function
start_time, end_time = amplitude_date_range('days', 1)

# Load .amplitude_env file
load_dotenv()

# Assign keys to variables
AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')
# logger.info('API key and secret imported from .env file.')

url = 'https://analytics.eu.amplitude.com/api/2/export'

# Amplitude API Call in try/except block if there are any issues. Prints exception error if function fails.
try:
    download_success = amplitude_api_call(
        url = url
        , start_time = start_time
        , end_time = end_time
        , AMP_API_KEY = AMP_API_KEY
        , AMP_SECRET_KEY = AMP_SECRET_KEY
        , max_attempts=3
        )
    
except Exception as e:
    print(f"Extraction failed: {e}")
    # logger.error(f"Extraction failed: {e}")

# Logic to only run zip extract function if files successfully downloaded from Amplitude
if download_success == True:

    # Call nested zip extract function. Prints exception error if function fails.
    try:
        # logger.info("Starting nested zip file extraction...")
        extract_success = amplitude_zip_file_extract('downloaded_data')
        # logger.info("Extraction complete.")

    except Exception as e:
        print(f"Extraction failed: {e}")
        # logger.error(f"Extraction failed: {e}")

else:
    print("Data download was unsuccessful. Review logs and try again.")
    # logger.info(f'Data download was unsuccessful so no data was extracted.')


# if extract_success == True:

#     # s3 load function

# else: 
#     print("Data download was unsuccessful. Review logs and try again.")
#     # logger.info(f'Data download was unsuccessful so no data was extracted.')