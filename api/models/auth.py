from pydantic import BaseModel


class LoginResponse(BaseModel):
    err: bool
    token: str | None
    msg: str | None


class LogoutResponse(BaseModel):
    msg: str | None
