# This script is currently calls the Amplitude API, ingests nested .zip files and extracts .json files for all of yesterday

# Load libraries
import requests
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

# Import libraries for nested .zip file extract function
from modules.functions import nested_zip_file_extract

 # Create variable for data folder creation logic
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)

# Get yesterday's date
yesterday = datetime.now() - timedelta(days=1)

# Format yesterday's start and end time as strings (YYYYMMDDTHH) for API parameters
start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')

# Create dynamic file name based off of start/end time
filename = f'amplitude_{start_time}_{end_time}'

# Create log filename variable that will create a new log file for each run
log_filename = f"logs/log_{filename}.log"

# Logging config
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

# Create logger config variable
logger = logging.getLogger()

# Load .amplitude_env file
load_dotenv()

# Assign keys to variables
api_key = os.getenv('AMP_API_KEY')
secret_key = os.getenv('AMP_SECRET_KEY')
logger.info('API key and secret imported from .env file.')

# API endpoint is the EU residency server
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start_time,
    'end': end_time
}

# Create variables for while loop check status code test
number_of_tries = 3
count = 0
download_success = False

# Logic to ensure API call retries do not exceed defined number limit
while count < number_of_tries:

    # Logging that download attempt has begun
    logger.info(f"Attempting download {count + 1}/{number_of_tries}...")

    # Make the GET request with basic authentication. try/except block to log information in the case of any errors and prevent early exit of loop.
    try:
        response = requests.get(url, params=params, auth=(api_key, secret_key), timeout = 20)

        # Assign response status code to a variable
        response_code = response.status_code

        # Wrapping folder creation, filepath creation, file write logic into conditional statement that checks response status code and returns a response to use based off of this.
        if response_code == 200:
            logger.info("Connection established. Downloading stream...")
            # Assign data to variable
            data = response.content

            # Create variable for data folder creation logic
            data_dir = "data"
            os.makedirs(data_dir, exist_ok=True)

            # Created filepath using filename variable and folder variable
            filepath = f'{data_dir}/{filename}.zip'

            # try/except block to provide information if there are any issues writing the file
            try:
                # Writing data file
                with open(filepath, 'wb') as file:
                    file.write(data)
                # Print success message
                print(f'Data retrieved and stored at /{filepath} 😊')
                # Logger will note a message if file write is successful
                logger.info(f'Data retrieved and stored at /{filepath} 😊') 
                download_success = True
            except Exception as e:
                print(e)
                # Logger will note exception error if file write is unsuccessful
                logger.error(f"An error occurred; {e}")             
            break

        # Print reason status code 400
        elif response_code == 400:
            print('Status code 400: File size max of 4GB exceeded. Adjust date range and try again')
            # Logger notes response reason when response code is 100s or 500s
            logger.warning('Status code 400: File size max of 4GB exceeded.')      
            break

        # Print reason status code 404
        elif response_code == 404:
            print('Status code 404: either the API did not run correctly or there is no data available for this time range. Double check the API configuration or adjust date range and try again')
            # Logger notes response reason when response code is 100s or 500s
            logger.warning('Status code 404: either the API did not run correctly or there is no data available for this time range.')    
            break

        # Print reason status code 504
        elif response_code == 504:
            print('Status code 504: Timeout due to large data size. Adjust date range and try again') 
            # Logger notes response reason when response code is 100s or 500s
            logger.warning('Status code 504: Timeout due to large data size.')    
            break

        # Print response reason and number of attempts and wait 10 seconds before loop runs again
        else:
            count +=1
            print(f'Error: {response.reason}. API will try again shortly. This is attempt {count}/{number_of_tries}. Retrying...')
            # Logger notes response reason when error occurs when connecting to the API
            logger.warning(f'Error: {response.reason}. API will try again shortly. This is attempt {count}/{number_of_tries}. Retrying...')
            time.sleep(10)

    # Exception errors raised if API connection fails
    except requests.exceptions.Timeout as e:
        print(f"Request failed - {e}")
        logger.error("Request timed out - server may be slow")
    except requests.exceptions.ConnectionError as e:
        print(f"Request failed - {e}")
        logger.error("Connection failed - check network")
    except requests.exceptions.RequestException as e:
        print(f"Request failed - {e}")
        logger.error(f"Other request error: {e}")

# Logic to only run nested zip extract function if files successfully downloaded from Amplitude
if download_success == True:
    # Create local output directory
    extracted_data = "extracted_data"
    os.makedirs(extracted_data, exist_ok=True)

    # Call nested zip extract function. Prints exception error if function fails.
    try:
        logger.info("Starting nested zip file extraction...")
        nested_zip_file_extract(extracted_data, filepath)
        logger.info("Extraction complete.") 
    except Exception as e:
        print(f"Extraction failed: {e}")
        logger.error(f"Extraction failed: {e}")
else:
    print("Data download was unsuccessful. Review logs and try again.")
    logger.info(f'Data download was unsuccessful so no data was extracted.') 