from enum import Enum
from sqlite3 import Timestamp
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from bson import ObjectId
from typing import Optional, List

from tomlkit import datetime
from datacenter.model.base import PyObjectId, BaseDBModel

class EmailStatus(str, Enum):
    sync = 'sync'
    send = 'send'    

class EmailType(str, Enum):
    text = 'text'
    html = 'html'

class EmailModel(BaseDBModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    sender: EmailStr = Field(...)
    receivers: List[EmailStr] = []
    ccs: List[EmailStr] = []
    bccs: List[EmailStr] = []
    message: str = Field(...)
    type: EmailType
    timestamp: datetime = Field(...)
    status: EmailStatus

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "安全SDP自动化测试报告-2022-04-06",
                "sender": "app.secpf@h3c.com",
                "receivers": ["receiver1@h3c.com", "receiver2@h3c.com", "receiver3@h3c.com"],
                "ccs": ["receiver1@h3c.com", "receiver2@h3c.com"],
                "bccs": ["receiver3@h3c.com"],
                "message": "此封邮件仅仅是为测试之用",
                "type": "text"
            }
        }

class SiteModel(BaseDBModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    domain: HttpUrl = Field(...)
    description: str = []
    owner: str = Field(...)
    email: EmailStr = Field(...)
    phone: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "安全SDP自动化测试报告-2022-04-06",
                "domain": "http://saat.secpf.h3c.com",
                "description": "安全SDP自动化测试报告-2022-04-06",
                "owner": "Zhang San",
                "email": "receiver1@h3c.com",
                "phone": "12345678978"
            }
        }


