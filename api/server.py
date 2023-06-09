import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.routing import APIRoute

from api.routers.v1 import build_v1_router
from api.utils.opnstk import OpenStack
from api.utils.networking import get_unused_private_subnet

origins = [
    "http://cyberrangedev.jakecrowley.com:3000",
    "https://cyberrange.jakecrowley.com",
]

app = FastAPI()
api_v1_router = build_v1_router()
app.include_router(api_v1_router, prefix="/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    from api.utils.redis import get_redis

    get_redis()


@app.exception_handler(RequestValidationError)
async def http_exception_handler(request, exc):
    if exc.raw_errors[0]._loc == ("cookie", "token"):
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})


# Debug mode
if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.8", port=8000, reload=True)
