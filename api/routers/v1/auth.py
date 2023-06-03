from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from api.utils.ldap import LDAP
from api.models.users import UserLogin, LdapUserInfo
import aioredis
from api.utils.redis import get_redis
import api.utils.tokens as tokens

router = APIRouter()


class LoginResponse(BaseModel):
    err: bool
    token: str | None
    msg: str | None


async def authenticate(
    token: str = Header(...), redis: aioredis.Redis = Depends(get_redis)
):
    # Check if the token exists in Redis
    user_info_json = await redis.get(token)
    if not user_info_json:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Deserialize user info from JSON
    user_info = LdapUserInfo.parse_raw(user_info_json)

    return user_info


@router.post("/auth/login", tags=["Authenticaton"], response_model=LoginResponse)
async def login(
    credentials: UserLogin, redis_pool: aioredis.Redis = Depends(get_redis)
) -> LoginResponse:
    user: LdapUserInfo | None = LDAP.check_creds(
        credentials.username, credentials.password
    )
    if user:
        token = tokens.get_new_token()
        await redis_pool.set(token, user.json())
        return LoginResponse(err=False, token=token)

    return LoginResponse(err=True, msg="Invalid Credentials")


@router.get(
    "/auth/logout",
    tags=["Authentication"],
)
async def logout(
    user_info: LdapUserInfo = Depends(authenticate), token: str = Header(...)
):
    print(token)
