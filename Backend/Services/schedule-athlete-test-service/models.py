import datetime
import boto3
import botocore
from boto3.dynamodb.conditions import Key
from settings import *
import traceback

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

AthleteTestTable = resource.Table(ATHELTE_TEST_TABLE)
AthleteAvailabilityTable = resource.Table(ATHLETE_AVAILABILITY_TABLE)
UserProfileTable = resource.Table(USER_PROFILE_TABLE)
CountryAdoTable = resource.Table(COUNTRY_ADO_TABLE)


class UserProfile:
    def __init__(self, user_id) -> None:
        self.user_id = user_id


class AthleteTest:
    def __init__(self, athlete_id, date, tester_id, orchestrator_id):
        try:
            self.__init_availability_item(athlete_id, date)
            self.__init_tester_item(tester_id)
            self.__init_orchestrator_item(orchestrator_id)
            self.__init_athlete_item(athlete_id)
            self.__init_datetime_key(self.start_date, self.start_time)
            self.result = TEST_NOT_AVAILABLE
            self.assigned_on = datetime.datetime.now().isoformat()
        except Exception as e:
            traceback.print_exc()
            raise Exception(
                f"Cannot create AthleteTest with athlete_id={athlete_id}, date={date}, tester_id={tester_id}, orchestrator_id={orchestrator_id}.\n Exception: {e}")

    def __init_datetime_key(self, start_date, start_time):
        test_datetime_as_dt = datetime.datetime.fromisoformat(
            f"{start_date} {start_time}")
        if test_datetime_as_dt.minute >= 5:
            test_datetime_as_dt = test_datetime_as_dt + \
                datetime.timedelta(hours=1)
        test_datetime_as_dt = test_datetime_as_dt.replace(second=0, minute=0)
        self.test_datetime = test_datetime_as_dt.strftime("%Y-%m-%d %H:%M:%S")

    def __init_availability_item(self, athlete_id, date):
        availability_item = self.fetch_athlete_availability(athlete_id, date)
        self.start_date = availability_item.get("date")
        self.start_time = availability_item.get("available_time")
        self.location = availability_item.get("location_address")
        self.country = availability_item.get("location_country")

    def fetch_athlete_availability(self, athlete_id, date):
        try:
            response = AthleteAvailabilityTable.get_item(
                Key={
                    'athlete_id': athlete_id,
                    'date': date,
                }
            )
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Message'])
        else:
            if response.get('Item'):
                return response['Item']
            raise Exception(f"Athlete availability item does not exist in table")

    def fetch_user_data(self, user_id):
        response = UserProfileTable.query(IndexName="Id-index", KeyConditionExpression=Key('Id').eq(user_id))
        return response.get("Items")[0]

    def fetch_country_ado(self, country):
        response = CountryAdoTable.get_item(Key={'Country': country})
        return response.get("Item")

    def __init_user_item(self, user_id):
        return UserProfile(user_id)

    def __init_tester_item(self, tester_id):
        self.tester: UserProfile = self.__init_user_item(tester_id)
        self.tester_id = self.tester.user_id

    def __init_orchestrator_item(self, orchestrator_id):
        self.orchestrator: UserProfile = self.__init_user_item(orchestrator_id)

    def __init_athlete_item(self, athlete_id):
        self.athlete: UserProfile = self.__init_user_item(athlete_id)

    def validate_item(self):
        validation_failures = {}
        self.check_location(validation_failures)
        if len(validation_failures) > 0:
            return False, validation_failures
        return True, None

    def check_location(self, validation_failures):
        tester = self.fetch_user_data(self.tester.user_id)
        if not tester.get("Country"):
            raise Exception("Tester does not have country assigned")
        tester_country_id = self.fetch_country_ado(tester.get("Country")).get("Id")
        if str(tester_country_id) != str(self.country):
            validation_failures["constraint_violation"] = COUNTRIES_DONT_MATCH

    def as_json(self):
        item_dict = self.__dict__.copy()
        item_dict['athlete'] = self.athlete.__dict__
        item_dict['tester'] = self.tester.__dict__
        item_dict['orchestrator'] = self.orchestrator.__dict__
        return item_dict

    def to_dynamo_json(self):
        athlete_test_safe = {
            'start_date': {'S': self.start_date},
            'start_time': {'S': self.start_time},
            'location': {'S': self.location},
            'country': {'S': str(self.country)},
            'tester': {'M': {
                'user_id': {
                    'S': self.tester.user_id
                }
            }
            },
            'tester_id': {'S': self.tester_id},
            'orchestrator': {'M': {
                'user_id': {
                    'S': self.orchestrator.user_id
                }
            }
            },
            'athlete': {'M': {
                'user_id': {
                    'S': self.athlete.user_id
                }
            }
            },
            'test_datetime': {'S': self.test_datetime},
            'result': {'S': self.result},
            'assigned_on': {'S': self.assigned_on},
        }
        return athlete_test_safe
