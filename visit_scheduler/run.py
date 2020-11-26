import asyncio

from logger import logger_configure
from visit_scheduler.scheduler import VisitScheduler


async def run_scheduler_async():
    logger_configure('DEBUG')
    async with VisitScheduler(interval=15) as scheduler:
        await scheduler.run()


def run_scheduler():
    asyncio.run(run_scheduler_async())
