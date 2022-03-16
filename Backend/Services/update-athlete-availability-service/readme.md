
# Request format for update availability

[{
	"country": "Ireland",
	"athlete_id": "99",
	"availability": [
        {
			"datetimeUTC": "datetime",
			"location": "location1"
		},
		{
			"datetimeUTC": "datetime",
			"location": "location2"
		},
        ...
	]
}]

Note: you can send several availability uploads at once, these availability items are shown above^


# Request format for initialise athelte availability

[{
	"country": "Ireland",
	"athlete_id": "99"
}]

### datetimeUTC

-> once you have date and time for availability -> convert to dateTime object, then convert to utc object
-> call datetime.isoformat() # converts time to iso string : https://docs.python.org/3/library/datetime.html#:~:text=datetime.-,isoformat,-(sep%3D%27T%27%2C%20timespec
-> send this as datetimeUTC field, for each item in availability

