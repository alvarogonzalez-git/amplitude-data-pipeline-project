# Import libraries - s3, .env, os
import boto3
from dotenv import load_dotenv
from datetime import datetime
import os
import logging

# Create variable for data folder creation logic
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)

# Create log filename variable that will create a new log file for each run
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"logs/log_s3_load_{timestamp}.log"

# Logging config
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

# Create logger config variable
logger = logging.getLogger()

# Load .env file
load_dotenv()

# Assign keys to variables
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
logger.info('API key, secret and bucket name imported from .env file.')


# Setting s3 client with authentication keys
s3_client = boto3.client(
    's3'
    , aws_access_key_id = AWS_ACCESS_KEY
    , aws_secret_access_key = AWS_SECRET_KEY
)

# Assign data filepath to a variable
data_dir = 'extracted_data'
os.makedirs(data_dir, exist_ok=True)

# Checks if folder is empty
if len(os.listdir(data_dir)) == 0:
    print(f"The '{data_dir}' folder is empty. No files will be loaded to s3.")
    logger.info(f"The '{data_dir}' folder is empty. No files will be loaded to s3.")

else:
    print(f"The '{data_dir}' folder contains files.")
    logger.info(f"The '{data_dir}' folder contains files. Files will begin uploading to s3 shortly...")

    # os.listdir returns everything in the folder (files and folders)
    all_items = os.listdir(data_dir)

    # Filter for files only
    file_list = []

    # Initialize count for number of files
    file_count = 0

    # Loops through all items in the data folder and adds them to a list
    for item in all_items:
        # Creates filepath for each file
        full_path = os.path.join(data_dir, item)
        # If file exists, append to the empty list
        if os.path.isfile(full_path):
            file_list.append(item)
            # Increase file_count by 1
            file_count += 1

    # Log number of files added to file_list
    logger.info(f"{file_count} files appended to upload list.")

    # Initialize count for number of files
    file_count = 0

    for filename in file_list:
        # Recreate the full path relative to the script for upload loop
        full_path = os.path.join(data_dir, filename)

        try:
            # Upload the file
                # 1. Path of data folder
                # 2. s3 bucket name
                # 3. Name of the file you want to upload
            s3_client.upload_file(full_path, AWS_BUCKET_NAME, filename)

            # Delete the local file ONLY if the line above succeeds
            os.remove(full_path)
            print(f"Uploaded and deleted local copy: {filename}")
            logger.info(f"Uploaded and deleted local copy: {filename}")

            # Increase file_count by 1
            file_count += 1

        except Exception as e:
            # If upload fails, the code jumps here, and the file is NOT deleted
            print(f"Failed to upload {filename}: {e}")
            logger.error(f"Failed to upload {filename}: {e}")
    
    # Print and log number of files added to file_list
    print(f"{file_count} files uploaded to s3 bucket and delete locally. Process Complete.")
    logger.info(f"{file_count} files uploaded to s3 bucket and delete locally. Process Complete.")