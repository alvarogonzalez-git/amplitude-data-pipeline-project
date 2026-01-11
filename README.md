<img src="https://github.com/user-attachments/assets/ab8eec14-a3b5-4d04-9a84-2928e2c12380" alt="Amplitude Logo" width="30%" />

# Amplitude Data Pipeline

This project was completed as a part of The Information Lab's Data Engineering School. It was incrementally developed on a weekly basis by applying the core skills that correspond to the main stages in the Data Engineering lifecycle: Extract, Transform and Load (ETL). The data for this project comes from [Amplitude's Export API](https://amplitude.com/docs/apis/analytics/export).

### Tasks
✅ Extract Completed
- [x] Ingestion of data via API Call using python script - `amplitude_api_call.py`
- [x] Error Handling in the python script using API response status code
- [x] Robust logging in python script
- [x] Error handling of API call using response.exceptions
- [x] Extract events data from nested .zip files

---

## Extract

The `amplitude_api_call.py` scriptnautomates the process of exporting raw event data from the **Amplitude Analytics API (EU Residency Server)**. It fetches data for the previous day, handles the download of large nested ZIP files, and automatically extracts the JSON event files.

### 🚀 Features
* **Automated Date Handling:** Automatically calculates "yesterday's" date to define the export window (00:00 to 23:00).
* **Resilient API Connection:** Includes a retry mechanism (up to 3 attempts) for handling intermittent connection failures or server timeouts.
* **Status Code Handling:** specific handling for common Amplitude API responses (200, 400, 404, 504).
* **Secure Configuration:** Uses `.env` files to keep API keys and secrets secure.
* **Comprehensive Logging:** detailed logs are generated for every run in the `logs/` directory, tracking success, errors, and retry attempts.
* **Automatic Extraction:** successfully downloaded ZIP files are automatically processed to extract the inner JSON data ready for analysis.

### 📋 Prerequisites
* Python 3.12
* An Amplitude Project (EU Data Center)
* API Key and Secret Key

### 🛠️ Setup
1.  **Clone the repository** (or download the script):
    ```bash
    git clone [https://github.com/alvarogonzalez-git/amplitude-data-pipeline-project.git](https://github.com/alvarogonzalez-git/amplitude-data-pipeline-project.git)
    cd amplitude-data-pipeline-project
    ```

2.  **Install required dependencies:**
    This script requires `requests` and `python-dotenv`.
    ```bash
    pip install requests python-dotenv
    ```

3.  **Configure Environment Variables:**
    Create a file named `.env` in the same directory as the script. Add your Amplitude credentials:

    ```text
    AMP_API_KEY=your_actual_api_key_here
    AMP_SECRET_KEY=your_actual_secret_key_here
    ```

### 🏃 How to run
Run the script from your terminal:

```bash
python your_script_name.py
```

### 👷 How it works
1. Date Calculation: The script determines the start and end time for the previous day.
2. API Request: It requests the export from the Amplitude Export API.
3. Download:
    - Success (200): Downloads the data to the data/ folder.
    - Failure: Logs the error (e.g., 404 if no data, 504 if timed out) and retries if applicable.
4. Extraction: If the download is successful, the nested_zip_file_extract function unzips the content into the extracted_data/ folder.

### 🪵 Logging
Logs are stored in the logs/ directory. Each run creates a specific log file based on the date range, e.g., logs/log_amplitude_20231025T00_20231025T23.log.
Common Log Messages:
- `INFO`: Successful connections and file writes.
- `WARNING`: API errors (400, 404, 504) or connection retries.
- `ERROR`: Critical failures (network timeouts, file write permission errors).

### ❔ Troubleshooting
- Status Code 400: File size exceeded 4GB. You may need to modify the script to download smaller hourly chunks rather than a full day.
- Status Code 404: No data found for the requested time range, or the API keys do not have access to the project.
- Status Code 504: The request timed out. The script handles this by retrying, but persistent 504s may indicate the data volume is too large for a single request.
