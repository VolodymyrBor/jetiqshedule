import time
import pytz
import datetime
from typing import List

from shared import logger
from databases import mysql
from .enums import VisitStatuses
from configs.schmes import Scheduler
from visit_scheduler.models import ScheduledVisit
from visit_scheduler.visitor import Visitor, VisitorError


class VisitScheduler:

    def __init__(self, config: Scheduler, time_zone: str):
        self.headless = config.BROWSER_HEADLESS
        self.interval = config.INTERVAL
        self.tz = pytz.timezone(time_zone)
        self.logger = logger.get_logger('VisitScheduler')

    async def run(self):
        """
        Run scheduler in inf loop.
        """
        self.logger.info('Scheduler started.')
        while True:
            try:
                self.logger.debug('pinging db for new visit...')
                await self.ping()
                time.sleep(self.interval)
            except (InterruptedError, KeyboardInterrupt):
                break
        self.logger.info('Scheduler stopped.')

    async def ping(self):
        """
        Check in database fro  scheduled visit in current time.
        """
        now = datetime.datetime.now(tz=self.tz)
        visits = await self._get_visits(now)

        if visits:
            self.logger.info(f'Got {len(visits)} visits that needs to do.')

        for visit in visits:
            visit.status = VisitStatuses.RUNNING
            visit.visit_start = datetime.datetime.now(tz=self.tz)
            await visit.save()

            owner = await visit.owner
            subject = await visit.lesson.subject
            try:
                visitor = Visitor(
                    password=owner.jetiq_password,
                    username=owner.jetiq_username,
                    headless=self.headless,
                )
                img = visitor.run([subject])
            except VisitorError as err:
                err_msg = str(err)
                self.logger.warning(err_msg)
                visit.error_message = err_msg
                visit.set_image(err.img)
                visit.status = VisitStatuses.FAILED
            else:
                visit.status = VisitStatuses.SUCCESSFUL
                visit.set_image(img)

            visit.visit_finish = datetime.datetime.now(tz=self.tz)
            await visit.save()

    @staticmethod
    async def _get_visits(before: datetime.datetime) -> List[ScheduledVisit]:
        lessons = ScheduledVisit.filter(date__lte=before.date())
        lessons = await lessons.prefetch_related('lesson')
        return [
            lesson for lesson in lessons
            if lesson.lesson.time.time() <= before.time() and lesson.status == VisitStatuses.CREATED
        ]

    async def connect(self):
        self.logger.info('Connecting to db...')
        await mysql.setup()

    async def close(self):
        self.logger.info('Disconnecting db...')
        await mysql.shutdown()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
