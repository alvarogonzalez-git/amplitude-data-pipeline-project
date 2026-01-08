<img src="https://github.com/user-attachments/assets/ab8eec14-a3b5-4d04-9a84-2928e2c12380" alt="Amplitude Logo" width="30%" />

# Amplitude Data Pipeline

This project was completed as a part of The Information Lab's Data Engineering School. It was incrementally developed on a weekly basis by applying the core skills that correspond to the main stages in the Data Engineering lifecycle: Extract, Transform and Load (ETL). The data for this project comes from [Amplitude's Export API](https://amplitude.com/docs/apis/analytics/export).

---

## Extract

Completed ✅
- [x] Ingestion of data via API Call using python script - `amplitude_api_call.py`
- [x] Error Handling in the python script using API response status code

To-Do ⌛
- [ ] Unpacking ingested ZIP files
- [ ] Logging

Future Enhancements 🔜
- [ ] Error handling of API call using response.exceptions
- [ ] Modularize steps into functions that can be reused in other scripts
