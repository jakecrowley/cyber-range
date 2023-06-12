from fastapi import APIRouter

from . import auth
from . import compute
from . import ws


def build_v1_router():
    api_v1_router = APIRouter()
    api_v1_router.include_router(auth.router)
    api_v1_router.include_router(compute.router)
    api_v1_router.include_router(ws.router)

    return api_v1_router
