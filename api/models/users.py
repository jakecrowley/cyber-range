from pydantic import BaseModel
from enum import Enum


class UserType(str, Enum):
    STUDENT = "STUDENT"
    STAFF = "STAFF"
    ADMIN = "ADMIN"


class LdapUserInfo(BaseModel):
    username: str
    display_name: str
    usertype: UserType
    project_id: str | None = None


class UserLogin(BaseModel):
    username: str
    password: str
