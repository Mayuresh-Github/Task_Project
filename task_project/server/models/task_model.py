from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TaskSchema(BaseModel):
    taskId: str
    taskName: str = Field(...)
    taskCreatedDate: str = Field(datetime.now())
    taskDescription: str = Field(...)
    taskAdditionalInfo: Optional[str]
    taskDueDate: str = Field(...)
    completed: bool = Field(default=False)
    userId: str = Field(...)
    sharedWith: Optional[list]

    class Config:
        schema_extra = {
            "task_example": {
                "taskName": "Test Task",
                "taskDescription": "Just a test task.",
                "taskAdditionalInfo": "Info (Optional)",
                "taskDueDate": "2020-22-12T15:53:00+05:30",
                "completed": "false",
            }
        }


class UpdateTaskModel(BaseModel):
    taskName: Optional[str]
    taskDescription: Optional[str]
    taskAdditionalInfo: Optional[str]
    taskDueDate: Optional[str]
    completed: Optional[bool]

    class Config:
        schema_extra = {
            "task_example": {
                "taskName": "Test Task (Optional)",
                "taskDescription": "Just a test task. (Optional)",
                "taskAdditionalInfo": "Info (Optional)",
                "taskDueDate": "2020-22-12T15:53:00+05:30 (Optional)",
                "completed": "true (Optional)",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
