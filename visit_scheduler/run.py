import asyncio

from configs.schmes import Config
from shared.logger import logger_configure
from visit_scheduler.scheduler import VisitScheduler


async def run_scheduler_async(config: Config):
    logger_configure(level=config.LOG_LEVEL.value, root_level=config.LOG_ROOT_LEVEL.value)
    async with VisitScheduler(config.SCHEDULER) as scheduler:
        await scheduler.run()


def run_scheduler(config: Config):
    asyncio.run(run_scheduler_async(config))
