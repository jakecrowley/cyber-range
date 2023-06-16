from pydantic import BaseModel


class DefaultResponse(BaseModel):
    err: bool
    msg: str | None
