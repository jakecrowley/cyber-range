from pydantic import BaseModel


class DefaultResponse(BaseModel):
    err: bool
    msg: str | None


class CreateNetworkInfo(BaseModel):
    name: str
    cidr: str


class CreateNetworkResponse(BaseModel):
    err: bool
    msg: str | None
