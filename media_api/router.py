import pathlib

from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException, status

from shared.strorage import ImageStorage

tag = ['media']


router = APIRouter()


@router.get('/', tags=tag)
async def get_media(path: str):
    path = pathlib.Path(path)
    storage = ImageStorage.from_path(path)
    try:
        return FileResponse(str(storage.get_file(path.name)))
    except FileNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'File {path!r} does not exits')
