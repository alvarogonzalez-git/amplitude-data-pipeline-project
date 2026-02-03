# Unzip and decompress files to retrieve .json files
# - Initial Unzip of 'amplitude_{start_time}_{end_time}.zip' is to a local 'extract_data' folder
# - JSON files are extracted to this same folder

# Load libraries
import os           # For operating system interactions (paths, directories)
import zipfile      # For working with .zip archives
import gzip         # For working with .gz compressed files
import shutil       # High-level file operations (copying, deleting trees)
import tempfile     # For generating temporary files/directories

def nested_zip_file_extract(extract_dir, filepath):
    """Extracts JSON files from a nested Amplitude data export archive.

    This function handles the specific Amplitude export structure: a main .zip archive 
    containing a numeric directory, which in turn contains multiple .gz compressed 
    JSON files. It handles the full pipeline of unzipping, locating the data, 
    decompressing the files, and cleaning up temporary artifacts.

    Args:
        extract_dir (str): The absolute or relative path to the destination directory 
                        where the final .json files will be saved.
        filepath (str): The absolute or relative path to the source .zip file 
                        downloaded from the Amplitude API.

    Raises:
        zipfile.BadZipFile: If the provided source file is not a valid zip archive.
        StopIteration: If the function cannot find a numeric directory inside the 
                       unzipped archive (unexpected file structure).
        OSError: If there are permission issues or errors creating/deleting directories.

    Process:
        1. Creates a secure temporary directory using `tempfile`.
        2. Extracts the main .zip archive into the temporary directory.
        3. Scans the extracted content to find the internal data folder (typically a numeric ID).
        4. Walks through the internal folder, identifying all .gz files.
        5. Decompresses each .gz file into a .json file in the `data_dir`.
        6. Prints real-time progress to the console.
        7. Recursively deletes the temporary directory to clean up disk space.

    Example:
        >>> output_folder = "/path/to/project/extracted_data"
        >>> source_file = "/path/to/project/data/amplitude_export.zip"
        >>> zip_gzip_file_extract(output_folder, source_file)
    """
    
    # Create variable for data folder creation logic
    download_dir = "downloaded_data"
    os.makedirs(download_dir, exist_ok=True)

    # Create dynamic file name based off of start/end time
    filename = f'amplitude_{start_time}_{end_time}'

    # Created filepath using filename variable and folder variable
    filepath = f'{download_dir}/{filename}.zip'


    print(f"--- Starting extraction process for: {filepath} ---")
    
    # Creates a unique temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary working directory: {temp_dir}")

    try:
        # Opens the main zip file
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            print("Unzipping main archive...")
            zip_ref.extractall(temp_dir)
            print("Main archive unzipped successfully.")
    except Exception as e:
        print(f"ERROR: Failed to unzip main file. {e}")
        shutil.rmtree(temp_dir) # Clean up if it fails immediately
        raise 

    try:
        # Find the numeric folder inside the extracted files
        day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
        day_path = os.path.join(temp_dir, day_folder)
        print(f"Found internal data folder: {day_folder}")
    except StopIteration:
        print("Error: Could not find a numeric folder inside the zip file.")
        shutil.rmtree(temp_dir)
        raise
    except Exception as e:
        print(f"Error locating data folder: {e}")
        raise

    # Initialize a counter for feedback
    file_count = 0
    extract_success = False

    # Walk through the directory tree
    for root, _, files in os.walk(day_path):
        # Filter strictly for .gz files to count them first (optional, for display)
        gz_files = [f for f in files if f.endswith('.gz')]
        
        if gz_files:
            print(f"Processing {len(gz_files)} files in {root}...")

        for file in gz_files:
            try:
                file_count += 1
                # Construct full paths
                gz_path = os.path.join(root, file)
                
                # Determine output filename (removes the last 3 chars '.gz')
                json_filename = file[:-3]  
                output_path = os.path.join(extract_dir, json_filename)

                # PRINT STATUS: This prevents the "frozen" look
                print(f"[{file_count}] Decompressing: {file} -> {json_filename}")

                # Decompress
                with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                    shutil.copyfileobj(gz_file, out_file)
                
            except Exception as e:
                print(f"Error extracting {file}: {e}")
                # We continue to the next file even if one fails
                continue 

    try:
        # Clean up temp directory
        print("Cleaning up temporary files...")
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Warning: Could not delete temp directory {temp_dir}. {e}")
        raise

    print(f"\nSUCCESS! {file_count} files extracted to '{extract_dir}' directory! 😊")
    
    # Logic to pass true for extract_success if more than one file extracted
    if file_count == 0:
        extract_success = False
    else:
        extract_success = True

    # Pass True status when function is run
    return(extract_success)