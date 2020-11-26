from tortoise import fields, models

from .enums import WeekDays


class Subject(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200, unique=True)
    teacher = fields.CharField(max_length=200)
    meet_url_name = fields.CharField(max_length=200)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    id = fields.IntField(pk=True)
    time = fields.DatetimeField()
    weekday = fields.CharEnumField(WeekDays)
    week_slug = fields.CharField(max_length=200)

    # Relations
    subject: Subject = fields.ForeignKeyField(
        'lesson_schedule.Subject',
        related_name='lessons',
        on_delete=fields.CASCADE,
    )

    def __str__(self):
        return f'{self.subject.name}:{self.time.time()}'
