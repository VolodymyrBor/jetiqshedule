from tortoise import models, fields

from . import enums
import auth
from lesson_schedule.models import Lesson


class ScheduledVisit(models.Model):
    date = fields.DateField(auto_now_add=True)
    lesson: Lesson = fields.ForeignKeyField('lesson_schedule.Lesson', on_delete=fields.CASCADE)

    status = fields.CharEnumField(enums.VisitStatuses, default=enums.VisitStatuses.CREATED)
    error_message = fields.CharField(max_length=200, null=True)
    visit_start = fields.DatetimeField(null=True)
    visit_finish = fields.DatetimeField(null=True)

    # Relations
    owner: 'auth.User' = fields.ForeignKeyField(
        model_name='auth.User',
        related_name='visits',
        on_delete=fields.CASCADE,
    )
