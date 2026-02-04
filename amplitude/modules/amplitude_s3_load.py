# Import libraries
import boto3
import os
import logging

# Define the logger
logger = logging.getLogger(__name__)

def amplitude_s3_load(extract_folder, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET_NAME):
    """
    This function uploads each extracted JSON file to an S3 bucket. Once files are uploaded successfully, the folder is cleaned up.

    Args:
        extract_folder (str): Name of the folder containing extracted JSON files.
        AWS_ACCESS_KEY (str): AWS access key from .env file
        AWS_SECRET_KEY (str): AWS access key from .env file
        AWS_BUCKET_NAME (str): AWS access key from .env file
    """

    # S3 client set-up with authentication keys
    s3_client = boto3.client(
        's3'
        , aws_access_key_id = AWS_ACCESS_KEY
        , aws_secret_access_key = AWS_SECRET_KEY
    )

    # Check if folder with extracted data exists. If it doesn't, folder is created.
    os.makedirs(extract_folder, exist_ok=True)

    # Checks if folder is empty. Function stops if folder is empty.
    if len(os.listdir(extract_folder)) == 0:
        print(f"The '{extract_folder}' folder is empty. No files will be loaded to s3.")
        logger.info(f"The '{extract_folder}' folder is empty. No files will be loaded to s3.")

    else:
        print(f"The '{extract_folder}' folder contains files.")
        logger.info(f"The '{extract_folder}' folder contains files. Files will begin uploading to s3 shortly...")

        # os.listdir returns everything in the folder (files and folders)
        all_items = os.listdir(extract_folder)

        # Create empty list to input files in extract_folder
        file_list = []

        # Initialize count for number of files added to the list
        file_count = 0

        # Loops through all items in the extract_folder and adds them to the file_list
        for item in all_items:
            # Creates filepath for file in the loop
            full_path = os.path.join(extract_folder, item)
            # If file exists, append to the empty list
            if os.path.isfile(full_path):
                file_list.append(item)
                # Increase file_count by 1
                file_count += 1

        # Log number of files added to file_list
        print(f"{file_count} files added to upload list.")
        logger.info(f"{file_count} files appended to upload list.")

        # Initialize count for number of files
        file_count = 0

        # Loops through all files in the file_list, creates relative path and enters try/except block that will upload to S3 bucket and clean up folder
        for filename in file_list:
            # Recreate the full path relative to the script for upload loop
            full_path = os.path.join(extract_folder, filename)

            try:
                # Uploads the file to S3 bucket. Args - path of data folder, s3 bucket name, name of the file you want to upload
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
        
        # Print and log number of files uploaded to S3 and cleaned up
        print(f"{file_count} files uploaded to bucket:{AWS_BUCKET_NAME} and deleted locally.")
        logger.info(f"{file_count} files uploaded to s3 bucket and delete locally. Process Complete.")