"""
This is public api which use to test only
"""

import logging

import requests
from decouple import config
from starlette.responses import JSONResponse

from app.exceptions.custom import (
    ApiForbiddenException,
    ApiInternalException
)

logger = logging.getLogger(config('LOG_NAME'))


class CoinDesk:
    def __init__(self, ws_id: str):
        self.ws_id = ws_id
        self.endpoint = 'https://api.coindesk.com/v1'
        self.timeout = 5

    def current_price(self) -> JSONResponse:
        url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        headers = {}
        payload = {}
        logger.info(f'{self.ws_id} - url: {url}, payload: {payload}, headers: {headers}')
        response = requests.get(url, data=payload, headers=headers, timeout=self.timeout)
        logger.info(f'{self.ws_id} - status: {response.status_code}')

        if response.status_code == 403:
            raise ApiForbiddenException

        if response.status_code == 500:
            raise ApiInternalException

        response = response.json()
        logger.info(f'{self.ws_id} - result: {response}')
        return response
