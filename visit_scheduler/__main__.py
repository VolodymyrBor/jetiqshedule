import asyncio

from logger import logger_configure
from visit_scheduler.scheduler import VisitScheduler


async def run_scheduler():
    async with VisitScheduler(interval=15) as scheduler:
        await scheduler.run()


if __name__ == '__main__':
    logger_configure('DEBUG')
    asyncio.run(run_scheduler())
