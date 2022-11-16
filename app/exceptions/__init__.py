import logging

from decouple import config
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK
)

logger = logging.getLogger(config('LOG_NAME'))


class Error(Exception):
    """Base class for other exceptions"""
    pass


class InternalError(Error):
    @classmethod
    def __call__(cls, ws_id: str) -> JSONResponse:
        """Raise when internal exception is happening"""
        msg = {
            'operationId': ws_id,
            'code': 400,
            'msg': 'Encountered the internal error.'
        }
        logger.error(f'{ws_id} - response: {msg}')
        return JSONResponse(status_code=HTTP_200_OK, content=msg)


class NotFoundError(Error):
    @classmethod
    def __call__(cls, ws_id: str) -> JSONResponse:
        """Raise when unable to find the details"""
        msg = {
            'operationId': ws_id,
            'code': 404,
            'msg': 'Detail not found.'
        }
        logger.error(f'{ws_id} - response: {msg}')
        return JSONResponse(status_code=HTTP_200_OK, content=msg)


class DatabaseConnectionError(Error):
    @classmethod
    def __call__(cls, ws_id: str) -> JSONResponse:
        """Raise when encountered database connection error"""
        msg = {
            'operationId': ws_id,
            'code': 502,
            'msg': 'Encountered database connection error.'
        }
        logger.error(f'{ws_id} - response: {msg}')
        return JSONResponse(status_code=HTTP_200_OK, content=msg)


class DatabaseSyntaxError(Error):
    @classmethod
    def __call__(cls, ws_id: str) -> JSONResponse:
        """Raise when encountered database syntax error"""
        msg = {
            'operationId': ws_id,
            'code': 502,
            'msg': 'Encountered database syntax error.'
        }
        logger.error(f'{ws_id} - response: {msg}')
        return JSONResponse(status_code=HTTP_200_OK, content=msg)
