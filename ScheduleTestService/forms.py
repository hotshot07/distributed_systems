class CreateTestForm():
    def __init__(self, availability_id, tester_id, orchestrator_id) -> None:
        self.availability_id = availability_id
        self.tester_id = tester_id
        self.orchestrator_id = orchestrator_id

    def validate(self):
        return type(self.availability_id is str) and type(self.tester_id is str) and type(self.orchestrator_id is str)
