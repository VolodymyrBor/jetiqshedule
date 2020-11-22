from tortoise import models, fields

from . import enums


class VisitStatus(models.Model):
    id = fields.IntField(pk=True)
    status = fields.CharEnumField(enums.VisitStatuses, default=enums.VisitStatuses.created)
    error_message = fields.CharField(max_length=200, null=True)
    start = fields.DatetimeField(auto_now_add=True)
    finish = fields.DatetimeField(null=True)
