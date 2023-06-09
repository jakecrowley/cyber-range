from fastapi import APIRouter, Depends, Cookie, HTTPException
from pydantic import BaseModel
from api.utils.ldap import LDAP
from api.models.users import UserLogin, LdapUserInfo
from api.models.auth import LoginResponse, LogoutResponse
from api.utils.opnstk import OpenStack
import api.utils.jwt as jwt

router = APIRouter()


async def authenticate(token: str = Cookie(...)):
    user_info = jwt.decode_token(token)
    if user_info is None:
        raise HTTPException(status_code=401, detail="Invalid Token")

    return user_info


@router.post(
    "/auth/login",
    tags=["Authentication"],
    response_model=LoginResponse,
)
async def login(credentials: UserLogin) -> LoginResponse:
    user: LdapUserInfo | None = LDAP.check_creds(
        credentials.username, credentials.password
    )
    if user:
        openstack = OpenStack.Instance()
        project = openstack.get_project(f"cyberrange-{user.username}")
        if project is None:
            project = openstack.create_project(f"cyberrange-{user.username}")

        user.project_id = str(project.id)
        token = jwt.encode_token(user)

        return LoginResponse(err=False, token=token)

    return LoginResponse(err=True, msg="Invalid Credentials")
