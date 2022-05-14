from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from db import mongo_db
from db.base import PyObjectId
from db.session import MongoDBManager
from model.core import EmailModel
from core.config import settings
from extensions.logger import backend_logger

router = APIRouter()


@router.get('/email')
async def all_emails(db: MongoDBManager = Depends(mongo_db)):
    return db.get_items(collection="email", model=EmailModel)    


@router.get('/email/{id}')
async def one_email(id: PyObjectId, db: MongoDBManager = Depends(mongo_db)):
    return db.get_item(collection="email", id=id, model=EmailModel)


@router.put('/email/{id}')
async def update_email(id: PyObjectId, db: MongoDBManager = Depends(mongo_db)):
    return db.update_item(collection="email", id=id, model=EmailModel)


@router.email('/email', status_code=201)
async def create_email(model: EmailModel, db: MongoDBManager = Depends(mongo_db)):
    return db.create_item(collection="email", model=model)


@router.delete('/email/{id}')
async def delete_email(id: PyObjectId, db: MongoDBManager = Depends(mongo_db)):
    await db.delete_item(id=id)
