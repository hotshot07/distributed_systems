import datetime
import boto3
import botocore
from settings import *

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

AthleteTestTable = resource.Table(ATHELTE_TEST_TABLE)
AthleteAvailabilityTable = resource.Table(ATHLETE_AVAILABILITY_TABLE)


class UserProfile:
    def __init__(self, user_id, first_name, second_name) -> None:
        self.user_id = user_id
        self.first_name = first_name
        self.second_name = second_name

    def fullname(self):
        return f"{self.first_name} {self.second_name}"

    def __str__(self) -> str:
        return f"{self.user_id}"


class TestResult:
    def __init__(self, result=TEST_NOT_AVAILABLE, note=None) -> None:
        self.result = result
        self.note = note


class AthleteTest:
    def __init__(self, athlete_id, date, tester_id, orchestrator_id):
        try:
            self.__init_availability_item(athlete_id, date)
            self.__init_tester_item(tester_id)
            self.__init_orchestrator_item(orchestrator_id)
            self.__init_athlete_item(athlete_id)
            self.__init_datetime_key(self.start_date, self.start_time)
            self.result: TestResult = TestResult()
            self.assigned_on = datetime.datetime.now().isoformat()
        except Exception as e:
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
        availability_item = self.get_athlete_availability(athlete_id, date)
        self.start_date = availability_item.get("date")
        self.start_time = availability_item.get("available_time")
        self.location = availability_item.get("location_address")
        self.country = availability_item.get("location_country")

    def get_athlete_availability(self, athlete_id, date):
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
            return response['Item']

    def __init_user_item(self, user_id):
        # TODO Call User DB
        return UserProfile(user_id, "John", "Doe")

    def __init_tester_item(self, tester_id):
        self.tester: UserProfile = self.__init_user_item(tester_id)
        self.tester_id = self.tester.user_id

    def __init_orchestrator_item(self, orchestrator_id):
        self.orchestrator: UserProfile = self.__init_user_item(orchestrator_id)

    def __init_athlete_item(self, athlete_id):
        self.athlete: UserProfile = self.__init_user_item(athlete_id)

    def validate_item(self):
        # TODO Add validation to check item can safely be created?
        return True

    def as_json(self):
        item_dict = self.__dict__.copy()
        item_dict['athlete'] = self.athlete.__dict__
        item_dict['tester'] = self.tester.__dict__
        item_dict['orchestrator'] = self.orchestrator.__dict__
        item_dict['result'] = self.result.__dict__
        return item_dict

    def to_dynamo_json(self):
        athlete_test_safe = {
            'start_date': {'S': self.start_date},
            'start_time': {'S': self.start_time},
            'location': {'S': self.location},
            'country': {'S': self.country},
            'tester': {'M': {
                'user_id': {
                    'S': self.tester.user_id
                },
                'first_name': {
                    'S': self.tester.first_name
                },
                'second_name': {
                    'S': self.tester.second_name
                }
            }
            },
            'tester_id': {'S': self.tester_id},
            'orchestrator': {'M': {
                'user_id': {
                    'S': self.orchestrator.user_id
                },
                'first_name': {
                    'S': self.orchestrator.first_name
                },
                'second_name': {
                    'S': self.orchestrator.second_name
                }
            }
            },
            'athlete': {'M': {
                'user_id': {
                    'S': self.athlete.user_id
                },
                'first_name': {
                    'S': self.athlete.first_name
                },
                'second_name': {
                    'S': self.athlete.second_name
                }
            }
            },
            'test_datetime': {'S': self.test_datetime},
            'result': {'S': self.result.result},
            'assigned_on': {'S': self.assigned_on},
        }
        return athlete_test_safe
