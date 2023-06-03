from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.routing import APIRoute

from api.routers.v1 import build_v1_router

app = FastAPI()
api_v1_router = build_v1_router()
app.include_router(api_v1_router, prefix="/v1")
