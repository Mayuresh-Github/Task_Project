from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from server.routes.user_routes import get_details
from task_project.server.database import (
    add_task,
    retrieveTask,
    retrieveTasks,
    updateTask,
    shareATask,
    detailedTask,
    viewSharedTask
)
from task_project.server.models.task_model import (
    ErrorResponseModel,
    ResponseModel,
    TaskSchema,
    UpdateTaskModel,
)

router = APIRouter()


@router.post("/addTask", response_description="Create new Task")
async def add_task_data(task: TaskSchema = Body(...)):
    task = jsonable_encoder(task)
    user = await get_details(task['userId'])
    if user:
        new_task = await add_task(userId=task['userId'], task_data=task)
        if new_task:
            return ResponseModel(new_task, "Task added successfully.")
    else:
        return ErrorResponseModel("User not found", 404, "User with that Id does not exist")


@router.get("/getAllTasks", response_description="Get all Tasks from DB")
async def getAllTasks():
    tasks = await retrieveTasks()
    return ResponseModel(tasks, "Read successful")


@router.get("/getTask", response_description="Get a Task from Id")
async def getTask(taskId: str):
    task = await retrieveTask(taskId)
    return ResponseModel(task, "Read successful")


@router.post("/updateTask", response_description="Update a Task")
async def update_task(taskId: str, req: UpdateTaskModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_task = await updateTask(taskId, req)
    if updated_task:
        return ResponseModel(
            "Task with ID: {} update is successful".format(taskId),
            "Task updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the task data.",
    )


@router.post("/shareTask", response_description="Share a Task to another User")
async def share_task(taskId: str, emailToShare: EmailStr) -> dict:
    task = await detailedTask(taskId)
    if task is not None:
        result = await shareATask(task, emailToShare, taskId)
        if result[0]:
            return ResponseModel(200, "Task shared successfully")
        elif result[1] == "Exists":
            return ErrorResponseModel("Task is already shared", 400, "The task is already shared with that User")
        elif result[1] == "User Not Found":
            return ErrorResponseModel("User not Found", 400, "User with that mail does not exist")
    else:
        return ErrorResponseModel("Task not Found", 404, "Task with that Id does not exist")


@router.get("/shareTask/view", response_description="View a Shared task")
async def view_task(taskId: str, emailSharedTo: EmailStr) -> dict:
    task = await detailedTask(taskId)
    taskToShare = await viewSharedTask(task, emailSharedTo, taskId)
    if taskToShare is not None:
        return ResponseModel(taskToShare, "Read successful")
    else:
        return ErrorResponseModel("Unauthorised", 404, "You are not authenticated to view this page")
