from fastapi import FastAPI

from task_project.server.routes.task_routes import router as TaskRouter
from task_project.server.routes.user_routes import router as UserRouter

app = FastAPI()

app.include_router(TaskRouter, tags=["Tasks"], prefix="/task")
app.include_router(UserRouter, tags=["User"], prefix="/user")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
