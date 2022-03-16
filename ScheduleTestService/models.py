import datetime
from constants import *


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
    def __init__(self, availability_id, tester_id, orchestrator_id):
        try:
            self.__init_availability_item(availability_id)
            self.__init_tester_item(tester_id)
            self.__init_orchestrator_item(orchestrator_id)
            self.result : TestResult = TestResult()
            self.assigned_on = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.test_id = self.availability_id
        except Exception as e:
            raise(f"Cannot create AthleteTest with availability_id={availability_id}, \
                tester_id={tester_id}, orchestrator_id={orchestrator_id}.\n \
                {e}")

    def __init_availability_item(self, id):
        # TODO Call Athlete Availability DB
        self.availability_id = id
        self.test_datetime = "2022-03-15 12:00:00"
        self.country = "Ireland"
        user_id = "1"
        self.athlete : UserProfile = self.__init_user_item(user_id)

    def __init_user_item(self, user_id):
        # TODO Call User DB 
        return UserProfile(user_id, "John", "Doe")

    def __init_tester_item(self, tester_id):
        self.tester : UserProfile = self.__init_user_item(tester_id)

    def __init_orchestrator_item(self, orchestrator_id):
        self.orchestrator : UserProfile = self.__init_user_item(orchestrator_id)

    def validate_item(self):
        # TODO Add validation to check item can safely be created?
        return True

    def as_json(self):
        item_dict = self.__dict__
        item_dict['athlete'] = self.athlete.__dict__
        item_dict['tester'] = self.tester.__dict__
        item_dict['orchestrator'] = self.orchestrator.__dict__
        item_dict['result'] = self.result.__dict__
        return item_dict