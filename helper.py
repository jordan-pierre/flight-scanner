from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

month_dict = {	
    1:'January',
    2:'February',
    3:'March',
    4:'April',
    5:'May',
    6:'June',
    7:'July',
    8:'August',
    9:'September',
    10:'October',
    11:'November',
    12:'December'	
}

def get_next_x_months(start_date, months_delta, anytime_option=True, inbound_mode=False):
    today = datetime.today()

    months_dict = dict() # “yyyy-mm”: "Month Year"

    if inbound_mode:
        months_dict[''] = 'One-way'
    if anytime_option:
        months_dict['anytime'] = 'Anytime'


    for i in range(months_delta):
        new_date = start_date + relativedelta(months=i)
        months_dict[f"{new_date.year}-{new_date.month}"] = f"{month_dict[new_date.month]} {new_date.year}"

    return months_dict

def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key
    raise KeyError

def str_date_to_datetime(str_date, months_dict):
    """Converts 'October 2021' type strings to Datetime(2021, 10, 1) type.  Leaves 'Anytime' or 'One-way' alone."""
    # Match 'October 2021' type string
    if bool(re.match('^[A-Z a-z]+ [0-9]+$', str_date)):
        text_date = get_key(str_date, months_dict) 
        # Match '2021-10' type string
        if bool(re.match('^[0-9]+-[0-9]+$', text_date)):
            parsed_date = [int(x) for x in text_date.split('-')]
            return datetime(parsed_date[0], parsed_date[1], 1)
    else:
        return str_date



months_dict = get_next_x_months(datetime.today(), 5, anytime_option=True, inbound_mode=True)
print(months_dict)
print(str_date_to_datetime('October 2021', months_dict))
