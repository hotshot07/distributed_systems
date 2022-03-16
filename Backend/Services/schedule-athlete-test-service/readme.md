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
    "athlete_id": "12345",
    "date": "2022-03-16",
    "orchestrator_id": "2",
    "tester_id": "8"
}'
```
Upload a test result
```
curl --location --request POST 'localhost:5000/upload-test-result' \
--header 'Content-Type: application/json' \
--data-raw '{
    "test_datetime": "2022-03-16 13:00:00",
    "test_result": "negative",
    "tester_id": "8"
}'
```