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


class UserLogin(BaseModel):
    username: str
    password: str
