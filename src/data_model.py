from pydantic import BaseModel
import pandas as pd

class BaseResponse(BaseModel):
    err: str | None = None

class BoolResponse(BaseResponse):
    result: bool = False

class DataFrameResponse(BaseResponse):
    data: dict

    class Config:
        arbitrary_types_allowed = True

