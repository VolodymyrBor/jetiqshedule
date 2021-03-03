import io
from pathlib import Path
from typing import Any, Union, Optional

from tortoise import fields

from shared.strorage import ImageStorage


class ImageField(fields.TextField):

    def __init__(self, *, upload_to: str, **kwargs: Any):
        super().__init__(**kwargs)
        self._storage = ImageStorage(upload_to)

    def to_db_value(self, value: Optional[Union[io.IOBase, Path]], instance) -> Optional[str]:

        if value is None:
            return None

        image_path = self._storage.save(value)
        image_path = self._storage.cut_file_path(image_path)
        return str(image_path)

    def to_python_value(self, value: str) -> Optional[Path]:

        if value is None:
            return None

        return Path(value)
