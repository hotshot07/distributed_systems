
# Request format for update availability

[{
	
	"athlete_id": "12345",
	"datetimeUTC": "2022-03-16T12:18:51.224726",
	"location": "Dublin 8",
	"location_country" : "Ireland"
}]

### datetimeUTC

-> once you have date and time for availability -> convert to dateTime object, then convert to utc object
-> call datetime.isoformat() # converts time to iso string : https://docs.python.org/3/library/datetime.html#:~:text=datetime.-,isoformat,-(sep%3D%27T%27%2C%20timespec
-> send this as datetimeUTC field, for each item in availability

