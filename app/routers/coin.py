import logging
import uuid

from decouple import config
from fastapi import APIRouter, Request

from app.exceptions.custom import (
    ApiForbiddenError,
    ApiForbiddenException,
    ApiInternalException,
    ApiInternalError
)
from app.exceptions import (
    InternalError
)
from app.external_api.coindesk import CoinDesk
from app.helper import visitor
from app.models.coin import CoinResponse

logger = logging.getLogger(config('LOG_NAME'))

coin = APIRouter()


@coin.get("/coin/get", response_model=CoinResponse)
def coin_get(request: Request):
    ws_id = uuid.uuid4().__str__()
    try:
        """store requestor info"""
        visitor(ws_id, request)

        """query to public api"""
        initiate = CoinDesk(ws_id)
        price = initiate.current_price()

        response = {
            'body': price,
            'operationId': ws_id
        }

        logger.info(f'{ws_id} - response: {response}')
        return response
    except ApiInternalException as e:
        logger.error(e, exc_info=True)
        return ApiInternalError.__call__(ws_id)
    except ApiForbiddenException as e:
        logger.error(e, exc_info=True)
        return ApiForbiddenError.__call__(ws_id)
    except Exception as e:
        logger.error(e, exc_info=True)
        return InternalError.__call__(ws_id)
