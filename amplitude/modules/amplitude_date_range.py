# Import libraries
from datetime import datetime, timedelta
import logging

# Define the logger
logger = logging.getLogger(__name__)

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

    # Log detected inputs
    print(f'Detected inputs are time_unit = "{time_unit}" and amount = "{amount}."')
    logger.info(f'Detected inputs are time_unit = "{time_unit}" and amount = "{amount}."')

    # 2. **args takes dictionary keys and tells python to accept the parameters 
    start_time = datetime.now() - timedelta(**kwargs)
    end_time = datetime.now() - timedelta(days=1)
    
    # Log calculated start_time and end_time and completion message
    print(f'Calculated start_time is {start_time.strftime('%Y%m%dT00')}.')
    logger.info(f'Calculated start_time is {start_time.strftime('%Y%m%dT00')}.')

    print(f'Calculated end_time is {end_time.strftime('%Y%m%dT00')}.')
    logger.info(f'Calculated end_time is {end_time.strftime('%Y%m%dT00')}.')

    print(f'Dynamic date range calculation complete.')
    logger.info(f'Dynamic date range calculation complete.')

    # Returns dynamic dates in desired format
    return start_time.strftime('%Y%m%dT00'), end_time.strftime('%Y%m%dT23')