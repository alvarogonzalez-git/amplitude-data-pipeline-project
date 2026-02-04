# Import libraries
import os
import zipfile
import gzip
import shutil
import tempfile

def amplitude_zip_file_extract(zip_folder:str):
    """
    Scans 'downloaded_data' for zips, extracts JSONs to 'extracted_data',
    and deletes source zips upon success.
    
    Args:
        zip_folder (str): Name of the folder containing downloaded .zip files.

    Returns:
        bool: True if ALL found files were processed and cleaned up successfully.
              False if ANY file failed or if no files were found.
    """
    
    # Check that the zip_folder exists, errors and returns False if it doesn't
    if not os.path.exists(zip_folder):
        print(f"Error: Source folder '{zip_folder}' not found.")
        return False

    # Create extracted_data folder if it doesn't already exist
    extract_folder = "extracted_data"
    os.makedirs(extract_folder, exist_ok=True)

    # Create list of all .zip files in zip_folder
    zip_files = [f for f in os.listdir(zip_folder) if f.endswith('.zip')]
    
    # Check if .zip files exist in zip_folder. Returns false if no files
    if not zip_files:
        print(f"No .zip files found in '{zip_folder}'.")
        return False 

    print(f"Starting extraction for {len(zip_files)} file(s)...")

    # Set extract success flag - defaults to False, becomes True if we successfully write even a single file to destination.
    extract_success = False

    # Loop that extracts json files from nested .zip files. If successful, cleans the .zip file by deletion.
    for zip_filename in zip_files:
        full_zip_path = os.path.join(zip_folder, zip_filename)
        temp_dir = tempfile.mkdtemp()
        
        # Local flag: only used to determine if we should cleanup the file currently in the loop
        current_zip_clean = False 

        try:
            # Unzip main .zip into temporary directory
            with zipfile.ZipFile(full_zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Identify folders inside the extracted files from the main .zip
            items = os.listdir(temp_dir)
            internal_folders = [d for d in items if os.path.isdir(os.path.join(temp_dir, d))]
            
            # Error if there were no folders inside main .zip
            if not internal_folders:
                print(f"Skipping {zip_filename}: No internal folder found.")
                continue

            # Select numeric folder first or first folder if no numeric
            day_folder = next((f for f in internal_folders if f.isdigit()), internal_folders[0])
            day_path = os.path.join(temp_dir, day_folder)

            # Extract .gz files
            file_count = 0
            for root, _, files in os.walk(day_path):
                for file in files:
                    if file.endswith('.gz'):
                        # Create gzip filepath
                        gz_path = os.path.join(root, file)
                        # Create json filename
                        json_name = file[:-3]
                        # Extract output filepath
                        out_path = os.path.join(extract_folder, json_name)
                        
                        try:
                            # Extract the gzip files by reading/writing binary to extract in chunks
                            with gzip.open(gz_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                            
                            # Increment only on file extract success
                            file_count += 1
                            
                        except Exception as e:
                            print(f"Error extracting {file}: {e}")
                            # Clean up partial file if it failed mid-stream
                            if os.path.exists(out_path):
                                os.remove(out_path)

            # Update flags on success
            if file_count > 0:
                print(f"Extracted {file_count} files from {zip_filename}")
                extract_success = True  # Extract SUCCESS flag set to True
                current_zip_clean = True # Flags that the specific zip is good to delete
            else:
                print(f"Warning: {zip_filename} contained no .gz files.")

            # Cleanup .zip file if the json was extracted successfully
            if current_zip_clean:
                if os.path.exists(full_zip_path):
                    os.remove(full_zip_path)
                    print(f"Cleanup: Deleted file {zip_filename}")

        except Exception as e:
            # Error message if a file extraction fails
            print(f"Error processing {zip_filename}: {e}")
            
        finally:
            # Delete temporary directory
            shutil.rmtree(temp_dir)

    # Return extract_success status - this will inform logic in main.py
    return extract_success