import datetime
from settings import *

def create_and_validate(data):
    availability = {}
    
    try:
        
        availability['athlete_id'] = data[0]['athlete_id']
        if availability['athlete_id'] == '':
            return 0
        
        availability['date_time_utc'] = validate_time(data[0]['datetimeUTC'])
        if availability['date_time_utc'] == 0:
            return INVALID_TIME_RESOLUTION_GIVEN
        if availability['date_time_utc'] == 1:
            return INVALID_TIME_FORMAT_GIVEN

        availability['location'] = data[0]['location']
        if availability['location'] == '':
            return 0
        
        availability['country'] = data[0]['location_country']
        if availability['country'] == '':
            return 0
    
    except Exception as e:
        print(e)
        return 0

    return availability


def validate_time(datetime_string):

    try:
        datetime_utc = datetime.datetime.fromisoformat(datetime_string)
        if ( (getattr(datetime_utc, 'minute', None) not in  [0, None] ) or (getattr(datetime_utc, 'second', None) not in  [0, None] ) or (getattr(datetime_utc, 'mircosecond', None) not in  [0, None] ) ):
            return 0
        else:
            return datetime_utc
    except:
        return 1
