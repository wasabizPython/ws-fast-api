from typing import List

from pydantic import BaseModel, Field


class GetResponse(BaseModel):
    body: dict = Field(default={})
    operationId: str = Field(default='')
    code: int = Field(default=200)
    msg: str = Field(default='Success')

    class Config:
        schema_extra = {
            "example": {
                "body": {
                    "user_id": "test_1",
                    "name": "test",
                    "role": "user",
                    "created_datetime": "2022-11-16T15:54:45",
                    "updated_datetime": "2022-11-16T15:54:45"
                },
                "operationId": "692acb6a-8f5d-432c-8549-2d0dff223c63",
                "code": 200,
                "msg": "Success",
            }
        }


class AddPayload(BaseModel):
    user: List[dict] = []

    class Config:
        schema_extra = {
            "example": {
                "user": [
                    {
                        'name': 'Mike',
                        'role': 'Administrator'
                    },
                    {
                        'name': 'John',
                        'role': 'User'
                    }
                ]
            }
        }


class AddResponse(BaseModel):
    status: bool = Field(default=True)
    operationId: str = Field(default='')
    code: int = Field(default=200)
    msg: str = Field(default='Success')

    class Config:
        schema_extra = {
            "example": {
                "status": True,
                "operationId": "692acb6a-8f5d-432c-8549-2d0dff223c63",
                "code": 200,
                "msg": "Success",
            }
        }
