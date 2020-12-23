import hashlib
from typing import Optional

import motor.motor_asyncio
import uuid

from pydantic.networks import EmailStr

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.task_project

user_collection = database.get_collection("users_collection")

task_collection = database.get_collection("tasks_collection")

salt = "SuP3R_SECR3T_SAL7"


def task_helper(task) -> dict:
    return {
        "taskName": task["taskName"],
        "taskCreatedDate": task["taskCreatedDate"],
        "taskDescription": task["taskDescription"],
        "taskAdditionalInfo": task["taskAdditionalInfo"],
        "completed": task['completed'],
        "taskDueDate": task["taskDueDate"],
    }


def user_helper(user) -> dict:
    return {
        "userName": user["userName"],
        "email": user["email"],
        "userJoinedDate": user["userJoinedDate"],
    }


# Add a new student into the DB
async def add_task(userId: str, task_data: dict) -> Optional[dict]:
    task_data['task_id'] = str(uuid.uuid1())
    task_data['userId'] = userId
    task = await task_collection.insert_one(task_data)
    new_task = await task_collection.find_one({"_id": task.inserted_id})
    return task_helper(new_task)


# Retrieve all tasks from DB
async def retrieve_tasks():
    tasks = []
    async for task in task_collection.find():
        tasks.append(task_helper(task))
    return tasks


# Retrieve a student with a matching ID
async def retrieve_task(uuid: str) -> dict:
    task = await task_collection.find_one({"task_id": uuid})
    if task:
        return task_helper(task)


# Retrieve a student with a matching ID
async def detailed_task(uuid: str) -> dict:
    task = await task_collection.find_one({"task_id": uuid})
    if task:
        return task


# Update a Task
async def updateTask(taskId: str, data: dict) -> bool:
    # Return false if an empty request body is sent
    if len(data) < 1:
        return False
    task = await task_collection.find_one({"task_id": taskId})
    if task:
        updated_task = await task_collection.update_one(
            {"task_id": taskId}, {"$set": data}
        )
        if updated_task:
            return True
        return False


# Create a new User
async def createNewUser(password: str, user_data: dict) -> dict:
    user_data['userId'] = str(uuid.uuid4())
    user_data['hashed_password'] = str(hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest())
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"userId": user_data['userId']})
    if new_user:
        return user_helper(new_user)


async def getUserDetails(userId: str) -> Optional[dict]:
    user = await user_collection.find_one({"userId": userId})
    if user:
        return user_helper(user)
    else:
        return None


async def shareATask(task: dict, emailToShare: EmailStr, taskId: str) -> bool:
    lstShare = task['sharedWith']
    if lstShare[0] is None:
        lstShare.insert(0, emailToShare)
        task['sharedWith'] = lstShare
        result = await updateTask(taskId, task)
        if result:
            return True
    if emailToShare in lstShare:
        return False
    else:
        lstShare.append(emailToShare)
        task['sharedWith'] = lstShare
        result = await updateTask(taskId, task)
        if result:
            return True
