import fire
import uvicorn
from fastapi import FastAPI

from databases import sqlite
from configs import get_config
from visit_api.routs import visit_router
from lesson_schedule.route import schedule


app = FastAPI()
app.include_router(schedule, prefix='/schedule')
app.include_router(visit_router, prefix='/visit')


@app.on_event('startup')
async def startup():
    """
    Setup connection to databases.
    """
    await sqlite.setup()


@app.on_event('shutdown')
async def shutdown():
    """
    Shutdown connection to databases.
    """
    await sqlite.shutdown()


def runserver(config_path=None):
    config = get_config(config_path)
    uvicorn.run(
        app='scheduleapp:app',
        reload=config.FAST_API.RELOAD,
        port=config.FAST_API.PORT,
        host=str(config.FAST_API.HOST),
    )


if __name__ == '__main__':
    fire.Fire(runserver)
