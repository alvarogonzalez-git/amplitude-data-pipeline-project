# Import libraries
from datetime import datetime, timedelta
from modules.amplitude_date_range import amplitude_data_range


start_time, end_time = amplitude_data_range('days', 1)

print(start_time)
print(end_time)