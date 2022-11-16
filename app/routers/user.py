import hashlib
import logging
import uuid
from datetime import datetime

import pymysql
from decouple import config
from fastapi import APIRouter, Request

from app.db import Database
from app.exceptions import (
    InternalError,
    NotFoundError,
    DatabaseConnectionError,
    DatabaseSyntaxError
)
from app.helper import visitor
from app.models.user import GetResponse, AddPayload, AddResponse

logger = logging.getLogger(config('LOG_NAME'))

user = APIRouter()

Items = {
    1: {
        'name': 'Mike',
        'role': 'Administrator',
        'created': '2022-01-01 01:01:00'
    },
    2: {
        'name': 'John',
        'role': 'Normal',
        'created': '2022-01-02 11:01:00'
    }
}


@user.get("/user/get", response_model=GetResponse)
def user_get(userId: str, request: Request):
    ws_id = uuid.uuid4().__str__()
    try:
        """store requestor info"""
        visitor(ws_id, request, userId)

        """get user id from db"""
        db = Database(ws_id)
        _select_ = db.select(
            sql='SELECT * FROM `template_web_service`.`user_profile` WHERE user_id=%s',
            value=userId
        )

        if not _select_:
            return NotFoundError.__call__(ws_id)

        db.close()

        response = {
            'body': _select_,
            'operationId': ws_id
        }

        logger.info(f'{ws_id} - response: {response}')
        return response
    except Exception as e:
        logger.error(e, exc_info=True)
        return InternalError.__call__(ws_id)


@user.post("/user/add", response_model=AddResponse)
def user_add(post: AddPayload, request: Request):
    ws_id = uuid.uuid4().__str__()
    try:
        """store requestor info"""
        visitor(ws_id, request, post)

        """create db connection"""
        db = Database(ws_id)

        for i in post.user:
            """generate encoded user id"""
            user_id = i['name'] + datetime.now().strftime('%Y%m%d%H%M%S')
            hashId = hashlib.md5()
            hashId.update(user_id.encode('utf-8'))
            user_id = str(int(hashId.hexdigest(), 16))[0:8]
            name = i['name']
            role = i['role']
            db.insert(
                sql=f'insert into `template_web_service`.`user_profile` (`user_id`, `name`, `role`) values (%s,%s,%s)',
                value=(user_id, name, role)
            )

        db.close()

        response = {
            'operationId': ws_id
        }

        logger.info(f'{ws_id} - response: {response}')
        return response
    except pymysql.err.ProgrammingError as e:
        logger.error(e, exc_info=True)
        return DatabaseSyntaxError.__call__(ws_id)
    except pymysql.err.OperationalError as e:
        logger.error(e, exc_info=True)
        return DatabaseConnectionError.__call__(ws_id)
    except Exception as e:
        logger.error(e, exc_info=True)
        return InternalError.__call__(ws_id)
