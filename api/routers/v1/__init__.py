from fastapi import APIRouter

from . import auth


def build_v1_router():
    api_v1_router = APIRouter()
    api_v1_router.include_router(auth.router)

    return api_v1_router
