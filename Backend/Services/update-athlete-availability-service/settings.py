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
