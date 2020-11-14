from tortoise import fields, models


class Subject(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200, unique=True)
    teacher = fields.CharField(max_length=200)

    def __str__(self):
        return self.name
