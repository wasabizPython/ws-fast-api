from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)

    class Config:
        the_schema = {
            "example": {
                "username": "user",
                "password": "user123#"
            }
        }



