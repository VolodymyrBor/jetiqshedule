import io
import uuid
from pathlib import Path
from typing import Optional, Union

from tortoise import models, fields, BaseDBAsyncClient

import auth
from . import enums
from shared.fileds import ImageField
from shared.strorage import ImageStorage
from lesson_schedule.models import Lesson


class ScheduledVisit(models.Model):
    date = fields.DateField(auto_now_add=True)
    lesson: Lesson = fields.ForeignKeyField('lesson_schedule.Lesson', on_delete=fields.CASCADE)
    image: Optional[Path] = ImageField(upload_to='visit/', null=True)
    status = fields.CharEnumField(enums.VisitStatuses, default=enums.VisitStatuses.CREATED)
    error_message = fields.CharField(max_length=512, null=True)
    visit_start = fields.DatetimeField(null=True)
    visit_finish = fields.DatetimeField(null=True)

    # Relations
    owner: 'auth.User' = fields.ForeignKeyField(
        model_name='auth.User',
        related_name='visits',
        on_delete=fields.CASCADE,
    )

    async def delete(self, using_db: Optional[BaseDBAsyncClient] = None) -> None:
        self._delete_img()
        return await super().delete(using_db)

    def set_image(self, image: Union[io.IOBase, Path, bytes]):

        if isinstance(image, bytes):
            buffer = io.BytesIO()
            buffer.name = f'{uuid.uuid4()}.png'
            buffer.write(image)
            image = buffer

        self._delete_img()
        self.image = image

    def _delete_img(self):
        if self.image:
            storage = ImageStorage.from_path(self.image)
            storage.delete(self.image.name)
