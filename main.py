import asyncio
import time

import uvicorn
from decouple import config
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_504_GATEWAY_TIMEOUT

from app.auth.jwt_bearer import JWTBearer
from app.routers.user import user
from app.routers.token import token
from app.routers.coin import coin
from setup import log

logger = log(
    name=config('LOG_NAME'),
    log_file=config("LOG_FILENAME"),
    log_format=config("LOG_FORMAT")
)

description = """
    ############
    # Features #
    ############
    1. Token Authentication (Bearer)
    2. Resource Management
    3. Database Connection
        - MySQl
            - select
            - insert
            - update
    4. Query to external API
    5. Custom Exception
"""

app = FastAPI(
    title="Web Service Fast API",
    version="v1.0.1",
    description=description
)


# Adding a middleware returning a 504 error if the request processing time is above a certain threshold
@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        return await asyncio.wait_for(call_next(request), timeout=int(config('REQUEST_TIMEOUT_ERROR')))
    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        msg = {
                'detail': 'Request processing timeout',
                'processing_time': process_time
            }
        logger.error(msg, exc_info=True)
        return JSONResponse(
            msg,
            status_code=HTTP_504_GATEWAY_TIMEOUT)


app.include_router(token, prefix=config('API_PREFIX'))
app.include_router(user, dependencies=[Depends(JWTBearer())], prefix=config('API_PREFIX'))
app.include_router(coin, dependencies=[Depends(JWTBearer())], prefix=config('API_PREFIX'))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
