from tkinter import EXCEPTION
from decouple import config

AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")

TEST_POSITIVE = "postive"
TEST_NEGATIVE = "negative"
TEST_INCONCLUSIVE = "inconclusive"
TEST_DID_NOT_SHOW = "did not show"
TEST_NOT_AVAILABLE = "not available"

ITEM_ALREADY_EXISTS = "Item already exists"
ITEM_ADDED_SUCCESSFULLY = "Item added successfully!"