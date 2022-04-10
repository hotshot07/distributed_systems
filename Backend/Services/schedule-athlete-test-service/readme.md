# Schedule Athlete Test
Install dependencies
```
pip install -r requirements.txt
```
Run application
```
python app.py
```
---
Create a test
```
curl --location --request POST 'localhost:5000/assign-athlete-test' \
--header 'Content-Type: application/json' \
--data-raw '{
    "athlete_id": "12342",
    "date": "2022-03-16",
    "orchestrator_id": "2",
    "tester_id": "Tester2"
}'
```
Upload a test result
```
curl --location --request POST 'localhost:5000/upload-test-result' \
--header 'Content-Type: application/json' \
--data-raw '{
    "test_datetime": "2022-03-16 12:00:00",
    "test_result": "postive",
    "tester_id": "Tester2"
}'
```
View upcoming tests for a tester
```
curl --location --request GET 'localhost:5000/view-upcoming-tests/56297746115'
```