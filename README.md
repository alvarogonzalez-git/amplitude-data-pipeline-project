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

- **Automated Date Handling:** Automatically calculates "yesterday's" date to define the export window (00:00 to 23:00).
- **Resilient API Connection:** Includes a retry mechanism (up to 3 attempts) for handling intermittent connection failures or server timeouts.
- **Status Code Handling:** specific handling for common Amplitude API responses (200, 400, 404, 504).
- **Secure Configuration:** Uses `.env` files to keep API keys and secrets secure.
- **Comprehensive Logging:** detailed logs are generated for every run in the `logs/` directory, tracking success, errors, and retry attempts.
- **Automatic Extraction:** successfully downloaded ZIP files are automatically processed to extract the inner JSON data ready for analysis.

### 📋 Prerequisites

- Python 3.12
- An Amplitude Project (EU Data Center)
- API Key and Secret Key

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

<div align="center">
  <img src="https://github.com/user-attachments/assets/ab8eec14-a3b5-4d04-9a84-2928e2c12380" alt="Amplitude Logo" width="30%" />

  <h1>Amplitude Data Pipeline</h1>

  <p>
    <strong>A production-ready ELT pipeline extracting behavioral data from Amplitude and loading it to AWS S3.</strong>
  </p>
</div>

<hr />

<p>
  This project was developed as part of <strong>The Information Lab's Data Engineering School</strong>. It implements a robust ELT (Extract, Load, Transform) pipeline to ingest raw event data from <a href="https://amplitude.com/docs/apis/analytics/export">Amplitude's Export API</a> and secure it in a Data Lake (AWS S3).
</p>

<h3>Tasks Completed</h3>
<ul>
  <li>✅ <strong>Extract:</strong> Ingestion via API, robust error handling, and nested ZIP extraction.</li>
  <li>✅ <strong>Load:</strong> Automated upload to AWS S3 with local cleanup.</li>
  <li>✅ <strong>Logging:</strong> Comprehensive runtime logging for auditing and debugging.</li>
</ul>

<hr />

<h2>🚀 Project Architecture</h2>

<p>The pipeline operates in two distinct phases:</p>

<ol>
  <li><strong>Extract (<code>amplitude_api_call.py</code>):</strong>
    <ul>
      <li>Calculates the date window for "yesterday" (00:00 - 23:00).</li>
      <li>Queries the Amplitude EU Export API.</li>
      <li>Downloads nested ZIP files and extracts the raw JSON event data.</li>
    </ul>
  </li>
  <li><strong>Load (<code>s3_load_amplitude.py</code>):</strong>
    <ul>
      <li>Scans the extracted data folder.</li>
      <li>Authenticates with AWS and uploads JSON files to an S3 bucket.</li>
      <li><strong>Auto-cleanup:</strong> Deletes local files immediately after a successful upload to save disk space.</li>
    </ul>
  </li>
</ol>

<hr />

<h2>📂 Project Structure</h2>

<pre>
├── logs/                   # Auto-generated: Stores runtime logs per execution
├── downloaded_data/        # Auto-generated: Temp storage for raw ZIPs
├── extracted_data/         # Auto-generated: Temp storage for JSON files
├── modules/
│   └── functions.py        # Contains helper function: nested_zip_file_extract
├── .env                    # Secrets (API Keys & AWS Credentials)
├── amplitude_api_call.py   # Script 1: Extract from Amplitude
├── s3_load_amplitude.py    # Script 2: Load to AWS S3
└── README.md
</pre>

<hr />

<h2>🛠️ Setup & Installation</h2>

<h3>1. Clone the repository</h3>
<pre><code>git clone https://github.com/alvarogonzalez-git/amplitude-data-pipeline-project.git
cd amplitude-data-pipeline-project</code></pre>

<h3>2. Install Dependencies</h3>
<p>Ensure you have Python 3.12+ installed:</p>
<pre><code>pip install requests boto3 python-dotenv</code></pre>

<h3>3. Configure Environment Variables</h3>
<p>Create a <code>.env</code> file in the root directory. You now need both Amplitude <strong>and</strong> AWS credentials:</p>

<p><strong>File: <code>.env</code></strong></p>
<pre><code># Amplitude Credentials
AMP_API_KEY=your_amplitude_api_key
AMP_SECRET_KEY=your_amplitude_secret_key
<code>
# AWS Credentials
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your_s3_bucket_name</code></pre>

<hr />

<h2>🏃 Usage</h2>

<h3>Phase 1: Extraction</h3>
<p>Run the API call script to fetch yesterday's data.</p>
<pre><code>python amplitude_api_call.py</code></pre>
<ul>
  <li><strong>Resilient Connection:</strong> Retries up to 3 times for 500/504 server errors.</li>
  <li><strong>Smart Handling:</strong> Detects 400 (File too large) and 404 (No data) status codes.</li>
  <li><strong>Output:</strong> Unzipped JSON files ready in <code>extracted_data/</code>.</li>
</ul>

<h3>Phase 2: Loading</h3>
<p>Run the load script to push data to the cloud.</p>
<pre><code>python s3_load_amplitude.py</code></pre>
<ul>
  <li><strong>Safety First:</strong> Only deletes local data if the S3 upload returns a success response.</li>
  <li><strong>Feedback:</strong> Logs every file upload status to <code>logs/log_s3_load_...</code>.</li>
</ul>

<hr />

<h2>🪵 Logging & Troubleshooting</h2>
<p>Logs are stored in the <code>logs/</code> directory. Check these files if the script exits unexpectedly.</p>

<table width="100%">
  <thead>
    <tr>
      <th>Status Code</th>
      <th>Meaning</th>
      <th>Action</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>200</code></td>
      <td>Success</td>
      <td>Data is downloading.</td>
    </tr>
    <tr>
      <td><code>400</code></td>
      <td>Bad Request</td>
      <td>File size > 4GB. Adjust script to download smaller time chunks.</td>
    </tr>
    <tr>
      <td><code>404</code></td>
      <td>Not Found</td>
      <td>No data for this date, or API keys are incorrect.</td>
    </tr>
    <tr>
      <td><code>504</code></td>
      <td>Timeout</td>
      <td>Data volume too large. Script will auto-retry.</td>
    </tr>
  </tbody>
</table>

<hr />

<h2>📄 License</h2>
<p>This project is open source and available under the <a href="LICENSE">MIT License</a>.</p>
