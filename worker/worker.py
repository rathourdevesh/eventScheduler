"""Worker class."""
from dao.db_helper import Scheduler

async def start_worker() -> None:
    scheduler = Scheduler()
    await scheduler.run()
