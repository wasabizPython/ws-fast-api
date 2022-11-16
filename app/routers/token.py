from fastapi import APIRouter

from app.auth import credential
from app.auth.jwt_handler import signJWT
from app.models.token import TokenSchema

token = APIRouter()


@token.post("/token")
def _(user: TokenSchema):
    if check_user(user):
        return signJWT(user.username)
    else:
        return {"code": 400, "msg": "Invalid login details"}


def check_user(data: TokenSchema):
    if data.username in credential.authorization:
        if data.password == credential.authorization[data.username]:
            return True
        else:
            return False
    else:
        return False
