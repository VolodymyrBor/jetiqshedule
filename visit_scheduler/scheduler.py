import time
import logging
import datetime
from typing import List

from databases import sqlite
from .enums import VisitStatuses
from logger import LOG_BASE_NAME
from visitor.visitor import Visitor
from visit_scheduler.models import ScheduledVisit


class VisitScheduler:

    def __init__(self, interval: float = 1):
        self.interval = interval
        self.logger = logging.getLogger(f'{LOG_BASE_NAME}.VisitScheduler')

    async def run(self):
        self.logger.info('Scheduler started.')
        while True:
            try:
                self.logger.info('pinging...')
                await self.ping()
                time.sleep(self.interval)
            except (InterruptedError, KeyboardInterrupt):
                break
        self.logger.info('Scheduler stopped.')

    async def ping(self):
        now = datetime.datetime.now()
        visits = await self._get_lessons(now)
        self.logger.info(f'Got {len(visits)} visits that needs to do.')
        for visit in visits:
            visit.status = VisitStatuses.running
            await visit.save()

            subject = await visit.lesson.subject
            visitor = Visitor(password=visit.password, username=visit.login)
            try:
                visitor.run([subject])
            except Exception as err:
                self.logger.warning(err)
                visit.error_message = str(err)
                visit.status = VisitStatuses.failed
            else:
                visit.status = VisitStatuses.successful

            visit.visit_finish = datetime.datetime.now()
            await visit.save()

    @staticmethod
    async def _get_lessons(before: datetime.datetime) -> List[ScheduledVisit]:
        lessons = ScheduledVisit.filter(date__lte=before.date())
        lessons = await lessons.prefetch_related('lesson')
        return [
            lesson for lesson in lessons
            if lesson.lesson.time.time() <= before.time() and lesson.status == VisitStatuses.created
        ]

    async def connect(self):
        self.logger.info('Connecting to db...')
        await sqlite.setup()

    async def close(self):
        self.logger.info('Disconnecting db...')
        await sqlite.shutdown()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
