from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from task_project.server.database import (
    createNewUser,
    getUserDetails
)
from task_project.server.models.user_model import (
    UserSchema,
    ResponseModel,
    ErrorResponseModel
)

router = APIRouter()


@router.post("/createUser", response_description="Create new User")
async def add_new_user(password: str, user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await createNewUser(password, user)
    if new_user:
        return ResponseModel(new_user, "User created successfully")
    else:
        return ErrorResponseModel("Precondition failed", 412, "User with that email exists")


@router.get("/getUserDetails", response_description="Get details of a User")
async def get_details(userId: str):
    user = await getUserDetails(userId)
    if user:
        return ResponseModel(user, "Got the details successfully")
    else:
        return ErrorResponseModel("Not Found", 404, "User with that Id does not exist")
