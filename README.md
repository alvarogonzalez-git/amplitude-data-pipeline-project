<img src="https://github.com/user-attachments/assets/ab8eec14-a3b5-4d04-9a84-2928e2c12380" alt="Amplitude Logo" width="30%" />

# Amplitude Data Pipeline

This project was completed as a part of The Information Lab's Data Engineering School. It was incrementally developed on a weekly basis by applying the core skills that correspond to the main stages in the Data Engineering lifecycle: Extract, Transform and Load (ETL). The data for this project comes from [Amplitude's Export API](https://amplitude.com/docs/apis/analytics/export).

Completed ✅
- [x] Ingestion of data via API Call using python script - `amplitude_api_call.py`
- [x] Error Handling in the python script using API response status code

To-Do ⌛
- [ ] Unpacking ingested ZIP files
- [ ] Logging

Future Enhancements 🔜
- [ ] Error handling of API call using response.exceptions
- [ ] Modularize steps into functions that can be reused in other scripts

---

## Extract

The `amplitude_api_call.py` script automates the process of exporting raw event data from Amplitude's **EU Residency** server. It calculates the date range for "yesterday" (full 24-hour cycle), fetches the data via the Amplitude Export API, and saves the resulting ZIP file locally.

## 🚀 Features

* **Automated Date Handling:** Automatically calculates start and end times for the previous day.
* **EU Endpoint:** Configured specifically for `analytics.eu.amplitude.com`.
* **Retry Logic:** Includes a `while` loop to retry the request up to 3 times in case of server instability.
* **Secure Configuration:** Uses environment variables to protect API credentials.
* **Error Handling:** Provides specific feedback for common HTTP status codes (400, 404, 504).
* **File Management:** Automatically checks for/creates a `data/` directory and saves files with timestamped naming conventions.

## 📋 Prerequisites

* Python 3.x
* An Amplitude Project (EU Data Center)
* API Key and Secret Key

## 🛠️ Installation & Setup

1.  **Clone the repository** (or download the script):
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
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

## 🏃 Usage

Run the script from your terminal:

```bash
python your_script_name.py
