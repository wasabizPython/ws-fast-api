from pydantic import BaseModel, Field


class CoinResponse(BaseModel):
    body: dict = Field(default={})
    operationId: str = Field(default='')
    code: int = Field(default=200)
    msg: str = Field(default='Success')

    class Config:
        schema_extra = {
            "example": {
                "body": {
                    "time": {
                        "updated": "Nov 16, 2022 15:59:00 UTC",
                        "updatedISO": "2022-11-16T15:59:00+00:00",
                        "updateduk": "Nov 16, 2022 at 15:59 GMT"
                    },
                    "disclaimer": "This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org",
                    "chartName": "Bitcoin",
                    "bpi": {
                        "USD": {
                            "code": "USD",
                            "symbol": "&#36;",
                            "rate": "16,402.5691",
                            "description": "United States Dollar",
                            "rate_float": 16402.5691
                        },
                        "GBP": {
                            "code": "GBP",
                            "symbol": "&pound;",
                            "rate": "13,705.8555",
                            "description": "British Pound Sterling",
                            "rate_float": 13705.8555
                        },
                    }
                },
                "operationId": "692acb6a-8f5d-432c-8549-2d0dff223c63",
                "code": 200,
                "msg": "Success",
            }
        }
