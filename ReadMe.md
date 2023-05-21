Event Scheduler
- Make the object and start the consumer in eventloop.
- Consume event in json/xml in below format.
{
    "payload": {}
    "interval": utc timestamp, when the payload will emitted
    "retry": retryCount how many times to retry . default 1
    "topic": topic to which payload to emitted. default is the original emited topic
    "seriliazationFormat": json/xml default received format.
}
- store data in db.
