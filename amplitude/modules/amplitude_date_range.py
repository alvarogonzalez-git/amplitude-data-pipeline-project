# Import libraries
from datetime import datetime, timedelta

def amplitude_date_range(time_unit: str, amount: int):
    '''
    Returns start_time, end_time in '%Y%m%dT00' format. start_time is determined from input parameters. The parameters determine how far back you wish to ingest from. end_time will return yesterday's end of day.
    
    Args:
    time_unit (str): weeks, days, hours, minutes, seconds.
    amount (int): amount of time unit.

    Returns:
    str: start_time in "%Y%m%dT00" format
        end_time in "%Y%m%dT00" format
    '''

    # 1. Mapping 'time_unit' to 'amount'. Can't pass through directly as timedelta will take 'time_unit' literally
    kwargs = {time_unit: amount}

    # 2. **args takes dictionary keys and tells python to accept the parameters 
    start_time = datetime.now() - timedelta(**kwargs)
    
    end_time = datetime.now() - timedelta(days=1)
    
    # Returns dynamic dates in desired format
    return start_time.strftime('%Y%m%dT00'), end_time.strftime('%Y%m%dT23')