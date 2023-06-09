import jwt
from api.models.users import LdapUserInfo, UserType
from api.config.config import JWT_SECRET


def encode_token(user_info: LdapUserInfo) -> str:
    return jwt.encode(
        {
            "username": user_info.username,
            "display_name": user_info.display_name,
            "usertype": user_info.usertype,
            "project_id": user_info.project_id,
        },
        JWT_SECRET,
        algorithm="HS256",
    )


def decode_token(token: str) -> LdapUserInfo:
    try:
        info = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return LdapUserInfo(**info)
    except jwt.exceptions.DecodeError:
        return None
