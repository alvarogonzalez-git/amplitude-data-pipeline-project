# Import libraries
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from modules.amplitude_date_range import amplitude_data_range
from modules.amplitude_api_call import amplitude_api_call
# from modules.amplitude_s3_load import amplitude_s3_load
from modules.nested_zip_file_extract import nested_zip_file_extract

# Create variable for data folder creation logic
download_dir = "downloaded_data"
os.makedirs(download_dir, exist_ok=True)

# Create local output directory
extracted_data = "extracted_data"
os.makedirs(extracted_data, exist_ok=True)

# Generate start_time, end_time with custom function
start_time, end_time = amplitude_data_range('days', 1)

print(start_time)
print(end_time)

# Load .amplitude_env file
load_dotenv()

# Assign keys to variables
AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')
# logger.info('API key and secret imported from .env file.')

url = 'https://analytics.eu.amplitude.com/api/2/export'

# Create dynamic file name based off of start/end time
filename = f'amplitude_{start_time}_{end_time}'

# Created filepath using filename variable and folder variable
filepath = f'{download_dir}/{filename}.zip'


download_success = amplitude_api_call(
    filepath = filepath
    , url = url
    , start_time = start_time
    , end_time = end_time
    , AMP_API_KEY = AMP_API_KEY
    , AMP_SECRET_KEY = AMP_SECRET_KEY
    , max_attempts=3
    )

print(download_success)

# Logic to only run nested zip extract function if files successfully downloaded from Amplitude
if download_success == True:

    # Call nested zip extract function. Prints exception error if function fails.
    try:
        # logger.info("Starting nested zip file extraction...")
        nested_zip_file_extract(extracted_data, filepath)
        # logger.info("Extraction complete.")

        # .ZIP file is deleted once all files have been extracted without error
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Cleanup: Deleted {filepath}")
            # logger.info(f"Cleanup: Deleted {filepath}")

    # Raise and log appropriate error code if nested zip extraction fails
    except Exception as e:
        print(f"Extraction failed: {e}")
        # logger.error(f"Extraction failed: {e}")

# Raise and log appropriate error code if API download fails
else:
    print("Data download was unsuccessful. Review logs and try again.")
    # logger.info(f'Data download was unsuccessful so no data was extracted.') 
