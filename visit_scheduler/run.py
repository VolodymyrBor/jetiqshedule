import asyncio

from configs import BaseConfig
from logger import logger_configure
from visit_scheduler.scheduler import VisitScheduler


async def run_scheduler_async(config: BaseConfig):
    logger_configure(level=config.LOG_LEVEL.value, root_level=config.LOG_ROOT_LEVEL.value)
    async with VisitScheduler(
            interval=config.SCHEDULER.INTERVAL,
            headless=config.SCHEDULER.BROWSER_HEADLESS) as scheduler:
        await scheduler.run()


def run_scheduler(config: BaseConfig):
    asyncio.run(run_scheduler_async(config))
