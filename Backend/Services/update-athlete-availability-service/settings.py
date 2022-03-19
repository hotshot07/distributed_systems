from decouple import config

ATHLETE_AVAILABILITY_TABLE= "AthleteAvailability"

AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")

METHOD_NOT_FOUND = 'Method not recognised'
ITEM_ALREADY_EXISTS = 'Initialisation could not be completed, item may already exist'
ITEM_DOES_NOT_EXIST = 'Initialisation could not be completed, item may not exist'
INIT_SUCCESS = 'Initialised Successfully'
UPDATE_SUCCESS = 'Updated Successfully'
INVALID_REQUEST_BODY = 'Invalid Request Body'
INVALID_TIME_RESOLUTION_GIVEN = 'The user has supplied an incorrect time format, the supplied utc time-slot must start on the hour. For example, 16:00 not 16:01'
INVALID_TIME_FORMAT_GIVEN = 'The user has not given time in the correct format, please give utc time in iso (8601) format'