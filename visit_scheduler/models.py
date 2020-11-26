from tortoise import models, fields

from . import enums
from lesson_schedule.models import Lesson


class ScheduledVisit(models.Model):
    date = fields.DateField(auto_now_add=True)
    lesson: Lesson = fields.ForeignKeyField('lesson_schedule.Lesson', on_delete=fields.CASCADE)
    login = fields.CharField(max_length=200)
    password = fields.CharField(max_length=200)

    status = fields.CharEnumField(enums.VisitStatuses, default=enums.VisitStatuses.created)
    error_message = fields.CharField(max_length=200, null=True)
    visit_start = fields.DatetimeField(null=True)
    visit_finish = fields.DatetimeField(null=True)
