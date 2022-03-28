import datetime
from settings import *
from countries import country_dict
from forms import AvailabilityForm


class AthleteAvailability:
    def __init__(self, availability_form : AvailabilityForm) -> None:
        self.athlete_id = availability_form.athlete_id
        self.location_address = availability_form.location
        try:
            self.__convert_time(availability_form.dateTime_utc)
            self.__verify_country(availability_form.country)
            self.__item_expiry()
        except Exception as e:
            raise e

    def validate(self):
        pass


    def __convert_time(self, datetime_string):
        try:
            datetime_utc = datetime.datetime.fromisoformat(datetime_string)
            if ( (getattr(datetime_utc, 'minute', None) not in  [0, None] ) or (getattr(datetime_utc, 'second', None) not in  [0, None] ) or (getattr(datetime_utc, 'mircosecond', None) not in  [0, None] ) ):
                raise Exception(INVALID_TIME_RESOLUTION_GIVEN)
            datetime_today = datetime.datetime.utcnow()
            
            if (datetime_utc < (datetime_today + datetime.timedelta(days=TIME_DELTA_WINDOW_IN_DAYS))):
                print(datetime_utc)
                raise Exception(TIME_TOO_EARLY)
            else:
                self.date = datetime_utc.date().isoformat()
                self.available_time = datetime_utc.time().isoformat()
        except Exception as e:
            raise e

    
    def __verify_country(self, country):
        country = country.lower().capitalize()
        if country in country_dict.keys():
            self.location_country = country_dict[country]
        else:
            raise Exception(INVALID_COUNTRY_GIVEN)

    def __item_expiry(self):
        availability_datetime = datetime.datetime.fromisoformat(f"{self.date} {self.available_time}")
        expiry_datetime = availability_datetime + datetime.timedelta(days=EXPIRY_IN_DAYS)
        self.expiry_datetime = expiry_datetime.isoformat()
        self.expiry_epoch = int(expiry_datetime.timestamp())
        

