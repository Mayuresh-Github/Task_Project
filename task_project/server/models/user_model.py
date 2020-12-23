from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    userName: str = Field(...)
    userId: str
    email: EmailStr = Field(...)
    hashed_password: str
    userJoinedDate: str

    class Config:
        schema_extra = {
            "task_example": {
                "userName": "John Doe",
                "email": "john@example.com",
                "userJoinedDate": "2020-22-12T15:53:00+05:30",
            }
        }


'''
For future purposes
'''
'''
class UpdateUserSchemaModel(BaseModel):
    userName: Optional[str]

    class Config:
        schema_extra = {
            "task_example": {
                "userName": "John Doe (Optional)",
            }
        }
'''


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
