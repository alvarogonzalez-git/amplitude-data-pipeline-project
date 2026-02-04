import requests
import time
import os

def amplitude_api_call(url: str, start_time: str, end_time: str, AMP_API_KEY: str, AMP_SECRET_KEY: str, max_attempts:int):
    '''
    This function calls the Amplitude API and downloads data between start_time and end_time and saves it to the defined filepath.
    
    Args:
        url (str): Amplitude API URL.
        start_time (str): earliest date in the download date range.
        end_time (str): latest date in the download date range.
        AMP_API_KEY (str): Amplitude API key from .env file.
        AMP_SECRET_KEY (str): Amplitude secret key from .env file.
        max_attempts (int): Maximum number of times the API call will retry in case of timeout.

    Returns:
        bool: True if API call and download completed successfully.
              False if API call fails.
    '''

    # API data parameters
    params = {
        'start': start_time,
        'end': end_time
    }

    # Create variables for while loop check status code test and confirmation download_complete
    loop_count = 0
    download_success = False

    # Logic to ensure API call retries do not exceed defined number limit
    while loop_count < max_attempts:

        # Logging that download attempt has begun
        # logger.info(f"Attempting download {loop_count + 1}/{max_attempts}...")

        # Make the GET request with basic authentication. try/except block to log information in the case of any errors and prevent early exit of loop.
        try:
            response = requests.get(url, params=params, auth=(AMP_API_KEY, AMP_SECRET_KEY), timeout = 45)

            # Assign response status code to a variable
            response_code = response.status_code

            # Create variable for data folder creation logic
            download_dir = "downloaded_data"
            os.makedirs(download_dir, exist_ok=True)

            # Create dynamic file name based off of start/end time
            filename = f'amplitude_{start_time}_{end_time}'

            # Created filepath using filename variable and folder variable
            filepath = f'{download_dir}/{filename}.zip'

            # Wrapping folder creation, filepath creation, file write logic into conditional statement that checks response status code and returns a response to use based off of this.
            if response_code == 200:
                # logger.info("Connection established. Downloading stream...")
                # Assign data to variable
                data = response.content

                # try/except block to provide information if there are any issues writing the file
                try:
                    # Writing data file
                    with open(filepath, 'wb') as file:
                        file.write(data)
                    # Print success message
                    print(f'Data retrieved and stored at /{filepath} 😊')
                    # Logger will note a message if file write is successful
                    # logger.info(f'Data retrieved and stored at /{filepath} 😊') 
                    download_success = True
                except Exception as e:
                    print(e)
                    # Logger will note exception error if file write is unsuccessful
                    # logger.error(f"An error occurred; {e}")             
                break

            # Print reason status code 400
            elif response_code == 400:
                print('Status code 400: File size max of 4GB exceeded. Adjust date range and try again')
                # Logger notes response reason when response code is 100s or 500s
                # logger.warning('Status code 400: File size max of 4GB exceeded.')      
                break

            # Print reason status code 404
            elif response_code == 404:
                print('Status code 404: either the API did not run correctly or there is no data available for this time range. Double check the API configuration or adjust date range and try again')
                # Logger notes response reason when response code is 100s or 500s
                # logger.warning('Status code 404: either the API did not run correctly or there is no data available for this time range.')    
                break

            # Print reason status code 504
            elif response_code == 504:
                print('Status code 504: Timeout due to large data size. Adjust date range and try again') 
                # Logger notes response reason when response code is 100s or 500s
                # logger.warning('Status code 504: Timeout due to large data size.')    
                break

            # Print response reason and number of attempts and wait 10 seconds before loop runs again
            else:
                loop_count +=1
                print(f'Error: {response.reason}. Status code: {response_code}. API will try again shortly. This is attempt {loop_count}/{max_attempts}. Retrying...')
                # Logger notes response reason when error occurs when connecting to the API
                # logger.warning(f'Error: {response.reason}. API will try again shortly. This is attempt {loop_count}/{max_attempts}. Retrying...')
                time.sleep(10)

        # Exception errors raised if API connection fails
        except requests.exceptions.Timeout as e:
            print(f"Request failed - {e}")
            # logger.error("Request timed out - server may be slow")
        except requests.exceptions.ConnectionError as e:
            print(f"Request failed - {e}")
            # logger.error("Connection failed - check network")
        except requests.exceptions.RequestException as e:
            print(f"Request failed - {e}")
            # logger.error(f"Other request error: {e}")

    return(download_success)