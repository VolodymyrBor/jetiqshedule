import asyncio

from logger import logger_configure
from visit_scheduler.scheduler import VisitScheduler


async def run_scheduler():
    async with VisitScheduler(interval=60) as scheduler:
        await scheduler.run()


if __name__ == '__main__':
    logger_configure()
    asyncio.run(run_scheduler())
