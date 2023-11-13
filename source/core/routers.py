from fastapi import APIRouter

from source.app.url.views import url_router

api_router = APIRouter()

api_router.include_router(url_router)
