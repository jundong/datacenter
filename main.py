import os
import logging
from typing import List
from datacenter.model.base import EmailModel, UpdateEmailModel
from fastapi import FastAPI, Body, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from threading import Thread
from worker.celery_app import celery_app
from db import mongo_db

# TO SUPPORT RUN python main.py in windows,but I use python "app/main.py" to start in liunx
os.sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core.config import settings
from api.api_v1 import api_router
from middleware import register_middleware
from extensions.logger import LOGGING_CONFIG

# app
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
# set middleware
register_middleware(app)

# set router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup():
    await mongo_db.connect_to_database(path=settings.MONGO_DATABASE_URI)

@app.on_event("shutdown")
async def shutdown():
    await mongo_db.close_database_connection()


if __name__ == '__main__':
    import uvicorn

    # Don't set debug/reload equals True,becauese TimedRotatingFileHandler can't support multi-prcoess
    # or dont't use my LOGGING_CONFIG in debug/reload
    uvicorn.run(app='main:app', host="0.0.0.0", port=8080, log_config=LOGGING_CONFIG)



# log = logging.getLogger(__name__)
# # MONGODB_URL=r'mongodb+srv://root:admin@localhost/datacenter?retryWrites=true&w=majority'
# MONGODB_URL=r'mongodb://root:admin@localhost:27017/datacenter?retryWrites=true&w=majority'

# app = FastAPI()
# #client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
# client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
# db = client.college

# def celery_on_message(body):
#     log.warn(body)

# def background_on_message(task):
#     log.warn(task.get(on_message=celery_on_message, propagate=False))

# @app.get("/{word}")
# async def root(word: str, background_task: BackgroundTasks):
#     task_name = None
#     # set correct task name based on the way you run the example
#     if not bool(os.getenv('DOCKER')):
#         task_name = "datacenter.worker.celery_worker.test_celery"
#     else:
#         task_name = "datacenter.worker.celery_worker.test_celery"
#     task = celery_app.send_task(task_name, args=[word])
#     print(task)
#     background_task.add_task(background_on_message, task)
#     return {"message": "Word received"}


# @app.post("/", response_description="Add new email", response_model=EmailModel)
# async def create_email(email: EmailModel = Body(...)):
#     email = jsonable_encoder(email)
#     new_email = await db["emails"].insert_one(email)
#     created_email = await db["emails"].find_one({"_id": new_email.inserted_id})
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_email)


# @app.get(
#     "/", response_description="List all emails", response_model=List[EmailModel]
# )
# async def get_emails():
#     emails = await db["emails"].find().to_list(1000)
#     return emails


# @app.get(
#     "/{id}", response_description="Get a single email", response_model=EmailModel
# )
# async def get_email(id: str):
#     if (email := await db["emails"].find_one({"_id": id})) is not None:
#         return email

#     raise HTTPException(status_code=404, detail=f"Email {id} not found")


# @app.put("/{id}", response_description="Update an email", response_model=EmailModel)
# async def update_email(id: str, email: UpdateEmailModel = Body(...)):
#     email = {k: v for k, v in email.dict().items() if v is not None}

#     if len(email) >= 1:
#         update_result = await db["emails"].update_one({"_id": id}, {"$set": email})

#         if update_result.modified_count == 1:
#             if (
#                 updated_email := await db["emails"].find_one({"_id": id})
#             ) is not None:
#                 return updated_email

#     if (existing_email := await db["emails"].find_one({"_id": id})) is not None:
#         return existing_email

#     raise HTTPException(status_code=404, detail=f"Email {id} not found")


# @app.delete("/{id}", response_description="Delete an email")
# async def delete_email(id: str):
#     delete_result = await db["emails"].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"Email {id} not found")
