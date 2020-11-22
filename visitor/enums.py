from enum import Enum


class VisitStatuses(str, Enum):
    created = 'created'
    running = 'running'
    successful = 'successful'
    failed = 'failed'
