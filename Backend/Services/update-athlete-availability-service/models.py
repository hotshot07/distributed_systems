import datetime
from settings import *
from countries import country_dict


class AthleteAvailabiltiy:
    def __init__(self, availability_form) -> None:
        self.athlete_id = availability_form.athlete_id
        self.location_address = availability_form.location
        try:
            self.__convert_time(availability_form.dateTime_utc)
            self.__verify_country(availability_form.country)
        except Exception as e:
            raise e

    def validate(self):
        pass


    def __convert_time(self, datetime_string):
        try:
            datetime_utc = datetime.datetime.fromisoformat(datetime_string)
            if ( (getattr(datetime_utc, 'minute', None) not in  [0, None] ) or (getattr(datetime_utc, 'second', None) not in  [0, None] ) or (getattr(datetime_utc, 'mircosecond', None) not in  [0, None] ) ):
                raise Exception(INVALID_TIME_RESOLUTION_GIVEND_TIME_FORMAT_GIVEN)
            else:
                self.date = datetime_utc.date().isoformat()
                self.available_time = datetime_utc.time().isoformat()
        except Exception:
            raise Exception(INVALID_TIME_FORMAT_GIVEN)

    
    def __verify_country(self, country):
        if country == '':
            raise Exception(INVALID_COUNTRY_GIVEN)
        
        country = country.lower().capitalize()
        if country in country_dict.keys():
            self.location_country = country_dict[country]
        else:
            raise Exception(INVALID_COUNTRY_GIVEN)



