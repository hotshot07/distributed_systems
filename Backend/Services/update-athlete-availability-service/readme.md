
# Request format for update availability

[{
	
	"athlete_id": "12345",
	"datetimeUTC": "2022-03-19 16:00:00",
	"location": "Dublin 8",
	"location_country" : "Ireland"
}]

### datetimeUTC

-> you must send time values to a resolution of 1 hour : 16:00, not 16:01 or 16:27
-> once you have date and time for availability -> convert to dateTime object, then convert to utc object
-> call datetime.isoformat() # converts time to iso (8601) string : https://docs.python.org/3/library/datetime.html#:~:text=datetime.-,isoformat,-(sep%3D%27T%27%2C%20timespec
-> send this as datetimeUTC field, for each item in availability

