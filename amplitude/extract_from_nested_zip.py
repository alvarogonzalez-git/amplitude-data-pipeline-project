# Unzip and decompress files to retrieve .json files
# - Initial Unzip of 'amplitude_{start_time}_{end_time}.zip' is to a local 'extract_data' folder
# - JSON files are extracted to this same folder

# Load libraries
import os           # For operating system interactions (paths, directories)
import zipfile      # For working with .zip archives
import gzip         # For working with .gz compressed files
import shutil       # High-level file operations (copying, deleting trees)
import tempfile     # For generating temporary files/directories

def zip_gzip_file_extract(data_dir, filename):
    print(f"--- Starting extraction process for: {filename} ---")
    
    # Creates a unique temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary working directory: {temp_dir}")

    try:
        # Opens the main zip file
        with zipfile.ZipFile(filename, "r") as zip_ref:
            print("Unzipping main archive...")
            zip_ref.extractall(temp_dir)
            print("Main archive unzipped successfully.")
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to unzip main file. {e}")
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
                output_path = os.path.join(data_dir, json_filename)

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

    print(f"\nSUCCESS! {file_count} files extracted to '{data_dir}' directory! 😊")