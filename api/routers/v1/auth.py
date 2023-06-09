from fastapi import APIRouter, Depends, Cookie, HTTPException
from pydantic import BaseModel
from api.utils.ldap import LDAP
from api.models.users import UserLogin, LdapUserInfo
from api.models.auth import LoginResponse, LogoutResponse
import aioredis
from api.utils.redis import get_redis
import api.utils.tokens as tokens
from api.utils.opnstk import OpenStack

router = APIRouter()


async def authenticate(
    token: str = Cookie(...), redis: aioredis.Redis = Depends(get_redis)
):
    # Check if the token exists in Redis
    user_info_json = await redis.get(token)
    if not user_info_json:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Deserialize user info from JSON
    user_info = LdapUserInfo.parse_raw(user_info_json)

    return user_info


@router.post(
    "/auth/login",
    tags=["Authentication"],
    response_model=LoginResponse,
)
async def login(
    credentials: UserLogin, redis_pool: aioredis.Redis = Depends(get_redis)
) -> LoginResponse:
    user: LdapUserInfo | None = LDAP.check_creds(
        credentials.username, credentials.password
    )
    if user:
        openstack = OpenStack.Instance()
        project = openstack.get_project(f"cyberrange-{user.username}")
        if project is None:
            project = openstack.create_project(f"cyberrange-{user.username}")

        user.project_id = str(project.id)
        token = tokens.get_new_token()
        await redis_pool.set(token, user.json(), ex=86400)

        return LoginResponse(err=False, token=token)

    return LoginResponse(err=True, msg="Invalid Credentials")


@router.get(
    "/auth/logout",
    tags=["Authentication"],
    response_model=LogoutResponse,
)
async def logout(
    user_info: LdapUserInfo = Depends(authenticate),
    token: str = Cookie(...),
    redis_pool: aioredis.Redis = Depends(get_redis),
) -> LogoutResponse:
    redis_pool.delete(token)
    return LogoutResponse(msg="Successfully logged out")
