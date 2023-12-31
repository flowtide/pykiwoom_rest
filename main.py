from fastapi import Depends, FastAPI
from pykiwoom.kiwoom import Kiwoom
from ohlcv.ohlcv_def import MinuteDF, MinuteTicks
from src.data_model import BoolResponse, DataFrameResponse
import logging

logger = logging.getLogger(__name__)

app = FastAPI()
kiwoom_inst = Kiwoom(login=True)

class KiwoomState:
    def __init__(self):
        self.kiwoom = kiwoom_inst

    @staticmethod
    def get_state():
        return KiwoomState()

@app.get("/login")
def login(stat: KiwoomState = Depends(KiwoomState.get_state)) -> BoolResponse:
    if not stat.kiwoom.connected:
        stat.kiwoom.CommConnect(block=True)
        logger.debug(f'[/login] login={stat.kiwoom.connected}')
    else:
        logger.debug(f'[/login] already login')
    return BoolResponse(result=True)

@app.get("/ohlcv_min/{symbol}")
def ohlcv_min(symbol: str, tick: MinuteTicks, stat: KiwoomState = Depends(KiwoomState.get_state)) -> DataFrameResponse:
    logger.debug(f'[/ohlcv_min/{symbol}] tick={tick}')
    df = stat.kiwoom.block_request("opt10080",
                                종목코드=symbol,
                                틱범위=tick.value,
                                output="분봉차트조회요청 ",
                                next=0)
    # 분봉 검색 결과는 "현재가	거래량	체결시간	시가	고가	저가" 필드 데이터만 있음
    logger.debug(f'[/ohlcv_min/{symbol}] df={df}')
    df = MinuteDF.preprocess_data(df)
    return DataFrameResponse(data=df.to_dict())
