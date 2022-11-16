# This file is responsible for signing, encoding, decoding and returning JWTs.
import logging
from datetime import datetime, timedelta

import jwt
from decouple import config
from fastapi import Request

from app.auth import credential

JWT_SECRET = config("SECRET")
JWT_ALGORITHM = config("ALGORITHM")

logger = logging.getLogger(config('LOG_NAME'))


# Function returns the generated Tokens (JWTs)
def token_response(token: str):
    return {
        "body": {
            "token": token,
            "expire": int(config("EXPIRED")) * 3600
        },
        "code": 200,
        "msg": "Success"
    }


# Function used for signing the JWT string
def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": (datetime.now() + timedelta(hours=int(config("EXPIRED")))).strftime("%Y%m%d%H%M%S")
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        current_time = datetime.now()
        expired_time = datetime.strptime(decode_token["expiry"], "%Y%m%d%H%M%S")

        return decode_token if expired_time >= current_time else None
    except Exception as e:
        logger.error(e, exc_info=True)
        return {}


def decodeUser(request: Request, token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        user_login = decode_token["userID"]

        logger.info((user_login, request.url, credential.resourceAccess[user_login]))

        pathAccess = '/'.join(str(request.url).split('?')[:-1])
        if not pathAccess:
            pathAccess = str(request.url)

        if pathAccess in credential.resourceAccess[user_login]:
            return True
        else:
            logger.error(f'user: {user_login} trying to access resources {request.url}.')
            return False

    except Exception as e:
        logger.error(e, exc_info=True)
        return False
