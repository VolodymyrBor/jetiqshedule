import io
import uuid
import shutil
from pathlib import Path
from typing import Union

from configs import get_db_config

config = get_db_config()


class ImageStorage:

    root_path = config.MEDIA_DIR

    def __init__(self, folder: str):
        self.folder = self.root_path / folder

    def save(self, file: Union[io.IOBase, Path]) -> Path:
        file_name = self._get_file_name(file.name)
        file_path = self.folder / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(file, Path):
            shutil.copy(file, file_path)
        else:
            file.seek(0)
            mode = 'w' if isinstance(file, io.StringIO) else 'wb'
            with file_path.open(mode) as opened_file:
                opened_file.write(file.read())

        return file_path

    def get_file(self, file_name: str, missing_ok=False) -> Path:
        file_path = self.folder / file_name

        if not missing_ok and not file_path.exists():
            raise FileNotFoundError('File does not exist')

        return file_path

    def cut_file_path(self, path: Path) -> Path:
        return Path(self.folder.name) / path.name

    def delete(self, file_name: str):
        file_path = self.get_file(file_name, missing_ok=True)
        file_path.unlink(missing_ok=True)

    @classmethod
    def from_path(cls, path: Path) -> 'ImageStorage':
        return ImageStorage(path.parts[0])

    def _get_file_name(self, file_name: str):

        if file_name not in self:
            return file_name

        file_uuid = uuid.uuid4()
        if '.' in file_name:
            file_name, extension = file_name.rsplit('.', 1)
            return f'{file_name}-{file_uuid}.{extension}'

        return f'{file_name}-{file_uuid}'

    def __contains__(self, file_name: str):
        files = set(self.folder.iterdir())
        return file_name in files
