# This script is currently calls the Amplitude API and ingests data for all of yesterday

# Load libraries
import requests
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load .amplitude_env file
load_dotenv()

# Assign keys to variables
api_key = os.getenv('AMP_API_KEY')
secret_key = os.getenv('AMP_SECRET_KEY')

# Get yesterday's date
yesterday = datetime.now() - timedelta(days=1)

# Format the start and end time strings (YYYYMMDDTHH)
start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')


# API endpoint is the EU residency server
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start_time,
    'end': end_time
}

# Create dynamic file name based off of start/end time
filename = f'amplitude_{start_time}_{end_time}'

# Create variables for while loop check status code test
number_of_tries = 3
count = 0

# Logic to ensure API call retries do not exceed defined number limit
while count < number_of_tries:

    # Make the GET request with basic authentication
    response = requests.get(url, params=params, auth=(api_key, secret_key))

    # Assign response status code to a variable
    response_code = response.status_code

    # Wrapping folder creation, filepath creation, file write logic into conditional statement that checks response status code and returns a response to use based off of this.
    if response_code == 200:
        # Assign data to variable
        data = response.content

        # Create variable for data folder creation logic
        dir = 'data'

        # Checking if data folder exists. If it doesn't exist, a folder is created
        if os.path.exists(dir):
            pass
        else:
            os.mkdir(dir)

        # Created filepath using filename variable and folder variable
        filepath = f'{dir}/{filename}.zip'

        # try/except block to provide information if there are any issues writing the file
        try:
            # Writing data file
            with open(filepath, 'wb') as file:
                file.write(data)
            # Print success message
            print(f'Data retrieved and stored at /{filepath} 😊')
        except Exception as e:
            print(e)
        break

    # Print reason status code 400
    elif response_code == 400:
        print('Status code 400: File size max of 4GB exceeded. Adjust date range and try again')      
        break

    # Print reason status code 404
    elif response_code == 404:
        print('Status code 404: either the API did not run correctly or there is no data available for this time range. Double check the API configuration or adjust date range and try again')    
        break

    # Print reason status code 504
    elif response_code == 504:
        print('Status code 504: Timeout due to large data size. Adjust date range and try again')     
        break

    # Print response reason and number of attempts and wait 10 seconds before loop runs again
    else:
        count +=1
        print(f'Error: {response.reason}. API will try again shortly. This is attempt {count}/{number_of_tries}')
        time.sleep(10)