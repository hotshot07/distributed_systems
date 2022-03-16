
def create_and_validate(data):
    availability = {}
    try:
        availability.athlete_id = data[0]['athlete_id']
        if availability.athlete_id == '':
            return 0
        availability.date_time_utc = data[0]['datetimeUTC']
        if availability.date_time_utc == '':
            return 0
        availability.location = data[0]['location']
        if availability.location == '':
            return 0
        availability.country = data[0]['location_country']
        if availability.country == '':
            return 0
    except:
        return 0

    return availability