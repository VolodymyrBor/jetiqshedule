from tortoise import fields, models

import auth
from lesson_schedule.enums import WeekDays

class Subject(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200, unique=True)
    teacher = fields.CharField(max_length=200)
    meet_url_name = fields.CharField(max_length=200, null=True)

    # Relations
    owner: 'auth.User' = fields.ForeignKeyField(
        model_name='auth.User',
        related_name='subjects',
        on_delete=fields.CASCADE,
    )

    class Meta:
        unique_together = (('name', 'owner'), )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    id = fields.IntField(pk=True)
    time = fields.DatetimeField()
    weekday = fields.CharEnumField(WeekDays)
    week_slug = fields.CharField(max_length=200)

    # Relations
    subject = fields.ForeignKeyField(
        model_name='lesson_schedule.Subject',
        related_name='lessons',
        on_delete=fields.CASCADE,
    )

    owner: 'auth.User' = fields.ForeignKeyField(model_name='auth.User', related_name='lessons')

    def __str__(self):
        return f'{self.subject.name}:{self.time.time()}'
