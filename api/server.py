import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.routing import APIRoute

from api.routers.v1 import build_v1_router
from api.utils.opnstk import OpenStack, OpenStackAPI

app = FastAPI()
api_v1_router = build_v1_router()
app.include_router(api_v1_router, prefix="/v1")


@app.on_event("startup")
async def startup_event():
    from api.utils.redis import get_redis

    await get_redis()
    OpenStackAPI = OpenStack()


@app.exception_handler(RequestValidationError)
async def http_exception_handler(request, exc):
    if exc.raw_errors[0]._loc == ("header", "token"):
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
