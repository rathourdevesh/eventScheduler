"""Event processor helper functions."""
import logging
import json

from dao.db_helper import Scheduler

async def process_event(raw_msg, **kwargs) -> None:
    """Load and save event into the db."""
    logger: logging = kwargs.get("logger")
    event = None
    try:
        event: dict = json.loads(raw_msg)
    except json.decoder.JSONDecodeError as e:
        logger.info(f"Invalid message format :: {raw_msg}")
        logger.info(e)
    if event:
        logger.info(f"processing event {event}")
        scheduler = Scheduler()
        scheduler.add_task(event)
