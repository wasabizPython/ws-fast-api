import logging

from decouple import config
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

logger = logging.getLogger(config('LOG_NAME'))


class ApiForbiddenException(Exception):
    pass


class ApiForbiddenError(ApiForbiddenException):
    @classmethod
    def __call__(cls, ws_id: str) -> JSONResponse:
        """Raise when encountered api forbidden error"""
        msg = {
            'operationId': ws_id,
            'code': 403,
            'msg': 'Encountered forbidden error to access the external api resources.'
        }
        logger.error(f'{ws_id} - response: {msg}')
        return JSONResponse(status_code=HTTP_200_OK, content=msg)


class ApiInternalException(Exception):
    pass


class ApiInternalError(ApiInternalException):
    @classmethod
    def __call__(cls, ws_id: str) -> JSONResponse:
        """Raise when encountered api internal error"""
        msg = {
            'operationId': ws_id,
            'code': 500,
            'msg': 'Encountered internal error when access the external api resources.'
        }
        logger.error(f'{ws_id} - response: {msg}')
        return JSONResponse(status_code=HTTP_200_OK, content=msg)
