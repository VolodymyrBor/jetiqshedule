from enum import Enum


class VisitStatuses(str, Enum):
    CREATED = 'created'
    RUNNING = 'running'
    SUCCESSFUL = 'successful'
    FAILED = 'failed'
