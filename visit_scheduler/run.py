import asyncio

from configs import get_db_config
from configs.schmes import Config
from shared.logger import logger_configure
from visit_scheduler.scheduler import VisitScheduler


async def run_scheduler_async(config: Config):
    db_config = get_db_config()
    logger_configure(level=config.LOG_LEVEL.value, root_level=config.LOG_ROOT_LEVEL.value)
    async with VisitScheduler(config.SCHEDULER, time_zone=db_config.TIME_ZONE) as scheduler:
        await scheduler.run()


def run_scheduler(config: Config):
    asyncio.run(run_scheduler_async(config))
