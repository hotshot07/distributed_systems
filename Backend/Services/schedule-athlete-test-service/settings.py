from tkinter import EXCEPTION
from decouple import config

AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")

ATHLETE_AVAILABILITY_TABLE = 'AthleteAvailability'
ATHELTE_TEST_TABLE = 'AthleteTest'

TEST_POSITIVE = "postive"
TEST_NEGATIVE = "negative"
TEST_INCONCLUSIVE = "inconclusive"
TEST_DID_NOT_SHOW = "did not show"
TEST_NOT_AVAILABLE = "not available"

ITEM_COULD_NOT_BE_ADDED = "Item could not be added to database"
ITEM_PARAMETERS_INVALID = "Item paramaters are invalid"
ITEM_ADDED_SUCCESSFULLY = "Item added successfully!"
ITEM_UPDATED_SUCCESSFULLY = "Item updated successfully!"