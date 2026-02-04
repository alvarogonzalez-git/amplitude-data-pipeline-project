# Import libraries
from dotenv import load_dotenv
import os

# Import modules
from modules.amplitude_date_range import amplitude_date_range
from modules.amplitude_api_call import amplitude_api_call
from modules.amplitude_zip_file_extract import  amplitude_zip_file_extract
from modules.amplitude_s3_load import amplitude_s3_load

# Generate start_time, end_time with custom function
start_time, end_time = amplitude_date_range('days', 1)

# Load .amplitude_env file
load_dotenv()

# Assign AMP keys to variables
AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')
# logger.info('API key and secret imported from .env file.')

# Assign keys to variables
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
# logger.info('API key, secret and bucket name imported from .env file.')

# Declare url for API call function
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
    print(f"Amplitude file download failed: {e}")
    # logger.error(f"Extraction failed: {e}")

# Logic to only run zip extract function if files successfully downloaded from Amplitude
if download_success == True:

    # Call nested zip extract function. Prints exception error if function fails.
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