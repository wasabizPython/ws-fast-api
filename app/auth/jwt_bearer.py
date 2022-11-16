# The function of this file is to check whether the request is authorized or not [ Verification of the protected route]

import logging
from decouple import config

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_handler import decodeJWT, decodeUser

logger = logging.getLogger(config('LOG_NAME'))


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                logger.error('Invalid authentication scheme.')
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                logger.error('Invalid token or expired token.')
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            if not decodeUser(request, credentials.credentials):
                logger.error('Invalid resource access.')
                raise HTTPException(status_code=403, detail="Invalid resource access.")

            return credentials.credentials
        else:
            logger.error('Invalid auth code.')
            raise HTTPException(status_code=403, detail="Invalid auth code.")

    @classmethod
    def verify_jwt(cls, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid
