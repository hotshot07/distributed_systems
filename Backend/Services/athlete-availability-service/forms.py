from settings import *

def convert_data_to_form(form):
    return AvailabilityForm(
        form['athlete_id'],
        form['datetimeUTC'],
        form['location'],
        form['location_country']
        )


class AvailabilityForm:
    def __init__(self, athlete_id, dateTime_utc, location, location_country) -> None:
        self.athlete_id = athlete_id
        self.dateTime_utc = dateTime_utc
        self.location = location
        self.country = location_country
    
    def validate(self):
        return type(self.athlete_id is str) and type(self.dateTime_utc is str) and type(self.location is str) and type(self.country is str)