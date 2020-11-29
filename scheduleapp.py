import uvicorn
from fastapi import FastAPI

from databases import sqlite
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


if __name__ == '__main__':
    uvicorn.run('scheduleapp:app', reload=True, port=8001)
