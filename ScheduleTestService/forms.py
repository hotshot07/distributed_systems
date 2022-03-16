class CreateTestForm:
    def __init__(self, athlete_id, date, tester_id, orchestrator_id) -> None:
        self.athlete_id = athlete_id
        self.tester_id = tester_id
        self.date = date
        self.orchestrator_id = orchestrator_id

    def validate(self):
        return type(self.athlete_id is str) and type(self.tester_id is str) and type(self.orchestrator_id is str) and type(self.date is str)


class UpdateTestResultForm:
    def __init__(self, test_datetime, tester_id, result) -> None:
        self.tester_id = tester_id
        self.test_datetime = test_datetime
        self.result = result

    def validate(self):
        return type(self.tester_id is str) and type(self.test_datetime is str) and type(self.result is str)