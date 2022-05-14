from fastapi import APIRouter, Depends

from core.config import settings
from api.api_v1 import email
from api.api_v1 import login
from api.api_v1 import report

api_router = APIRouter()
# 各自模块的路由由各自模块负责
api_router.include_router(email.router,dependencies=[Depends(settings)])
api_router.include_router(login.router,dependencies=[Depends(settings)])
api_router.include_router(report.router,dependencies=[Depends(settings)])
