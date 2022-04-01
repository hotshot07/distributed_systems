from tempfile import tempdir
from settings import *
from dynamodb_handler import check_user_exists

class CreateTestForm:
    def __init__(self, athlete_id, date, tester_id, orchestrator_id) -> None:
        self.athlete_id = athlete_id
        self.tester_id = tester_id
        self.date = date
        self.orchestrator_id = orchestrator_id
        self.validation_failures = {}
        self.orgs = []

    def validate(self):
        self.validate_user(self.athlete_id, ATHLETE_ROLE, "athlete_id")
        self.validate_user(self.orchestrator_id, ORCHESTRATOR_ROLE, "orchestrator_id")
        self.validate_user(self.tester_id, TESTER_ROLE, "tester_id")
        self.validate_org()
        self.validate_date()
        return len(self.validation_failures) == 0

    def validate_user(self, user_id, user_role, failure_tag):
        if not check_type_str(user_id):
            self.validation_failures[failure_tag] = FORM_TYPE_MUST_STRING
        else:
            user_exists = check_user_exists(user_id, user_role)
            if not user_exists[0]:
                self.validation_failures[failure_tag] = f"User ({user_id}) with role ({user_role}) does not exist"
            elif user_role == TESTER_ROLE:
                self.tester_country = user_exists[1]
            if user_exists[0]:
                self.orgs.append(user_exists[1])

    def validate_date(self):
        import datetime
        try:
            datetime.datetime.strptime(self.date,"%Y-%m-%d")
        except ValueError as err:
            self.validation_failures["date"] = f"Invalid date ({self.date}), it should be in the format yyyy-mm-dd"

    def validate_org(self):
        # Check athlete and orchestrator are part of same organization
        if self.orgs[0] != self.orgs[1]:
            self.validation_failures["constraint_violation"] = f"Tester, athlete and orchestrator must all be from the same Organisation"

class UpdateTestResultForm:
    def __init__(self, test_datetime, tester_id, result) -> None:
        self.tester_id = tester_id
        self.test_datetime = test_datetime
        self.result = result

    def validate(self):
        return type(self.tester_id is str) and type(self.test_datetime is str) and type(self.result is str)

def check_type_str(item):
    return type(item is str)