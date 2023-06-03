from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.utils.ldap import LDAP
from api.models.users import UserLogin, LdapUserInfo
from . import app

router = APIRouter()


@router.post(
    "/auth/login",
    tags=["Authenticaton"],
)
async def login(credentials: UserLogin):
    user: LdapUserInfo | None = LDAP.check_creds(
        credentials.username, credentials.password
    )
    if user:
        # do redis stuff lol
        return JSONResponse({"err": False, "token": "placeholder"})

    return JSONResponse({"err": True, "msg": "Invalid Credentials"})


@router.get(
    "/auth/logout",
    tags=["Authentication"],
)
async def logout():
    # do logout stuff
    pass
