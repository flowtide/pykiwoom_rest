from fastapi import Depends, FastAPI, Query
import pykiwoom
from ohlcv.ohlcv_def import MinuteDF, MinuteTicks, DayDF
from src.data_model import BoolResponse, DataFrameResponse
import logging

logger = logging.getLogger(__name__)

app = FastAPI()
km = pykiwoom.KiwoomManager()

class KiwoomState:
    def __init__(self):
        self.km = km

    @staticmethod
    def get_state():
        return KiwoomState()

@app.get("/login")
def login(stat: KiwoomState = Depends(KiwoomState.get_state)) -> BoolResponse:
    # if not stat.km.connected:
    #     stat.km.CommConnect(block=True)
    #     logger.debug(f'[/login] login={stat.km.connected}')
    # else:
    #     logger.debug(f'[/login] already login')
    return BoolResponse(result=True)

@app.get("/ohlcv_min/{symbol}")
def ohlcv_min(symbol: str, tick: MinuteTicks
              , stat: KiwoomState = Depends(KiwoomState.get_state)) -> DataFrameResponse:
    logger.debug(f'[/ohlcv_min/{symbol}] tick={tick}')
    tr_cmd = {
        'rqname': "opt10080",
        'trcode': 'opt10080',
        'next': '0',
        'screen': '1000',
        'input': {
            "종목코드": symbol,
            "틱범위": tick.value
            #"기준일자": "20220612",
            #"수정주가구분": "0",
        },
        'output': MinuteDF.column_names
    }

    stat.km.put_tr(tr_cmd)
    df, remain = stat.km.get_tr()
    df = MinuteDF.preprocess_data(df)
    return DataFrameResponse(data=df.to_dict('records'))

@app.get("/ohlcv_day/{symbol}")
def ohlcv_min(symbol: str, yyyymmdd: str = Query(None, format="yyyymmdd", pattern="^(19|20)\d\d(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$")
              , stat: KiwoomState = Depends(KiwoomState.get_state)) -> DataFrameResponse:
    logger.debug(f'[/ohlcv_day/{symbol}] yyyymmdd={yyyymmdd}')
    tr_cmd = {
        'rqname': "opt10081",
        'trcode': 'opt10081',
        'next': '0',
        'screen': '1001',
        'input': {
            "종목코드": symbol,
            "기준일자": yyyymmdd,
            #"수정주가구분": "0",
        },
        'output': DayDF.column_names
    }

    stat.km.put_tr(tr_cmd)
    df, remain = stat.km.get_tr()
    print(f'df={df}')
    df = DayDF.preprocess_data(df)
    return DataFrameResponse(data=df.to_dict('records'))
