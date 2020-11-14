import uvicorn
from fastapi import FastAPI

from schedule.route import schedule


app = FastAPI()
app.include_router(schedule, prefix='/schedule')


if __name__ == '__main__':
    uvicorn.run('scheduleapp:app', reload=True, port=8001)
