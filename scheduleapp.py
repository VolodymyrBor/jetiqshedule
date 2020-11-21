import uvicorn
from fastapi import FastAPI

from databases import sqlite
from lesson_scheduler.route import schedule


app = FastAPI()
app.include_router(schedule, prefix='/schedule')


@app.on_event('startup')
async def startup():
    await sqlite.setup()


@app.on_event('shutdown')
async def shutdown():
    await sqlite.shutdown()


if __name__ == '__main__':
    uvicorn.run('scheduleapp:app', reload=True, port=8001)
