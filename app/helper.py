import logging

from decouple import config
from fastapi import Request

logger = logging.getLogger(config('LOG_NAME'))


def visitor(ws_id: str, request: Request, payload: object) -> None:
    """
    Function use to store the visitor request info to logging
    :param ws_id:
    :param request:
    :param payload:
    :return:
    """

    client = request.client.host
    scheme = request.url.scheme
    path = request.url.path
    port = request.url.port
    host = f'{request.client.host}'
    url = f'{scheme}://{host}:{port}{path}'

    msg = {
        'host': host,
        'client': client,
        'url': url,
        'payload': payload
    }

    logger.info(f'{ws_id} - {msg}')
