import uuid

class eventObject:
    def __init__(
        self,
        payload: dict = {},
        interval: int = 0,
        retry: int = 1,
        topic: str = "",
        seriliazation_format: str = "json"
    ) -> None:
        self.task_id = str(uuid.uuid())
        self.payload = payload
        self.interval = interval
        self.retry = retry
        self.topic = topic
        self.seriliazation_format = seriliazation_format
