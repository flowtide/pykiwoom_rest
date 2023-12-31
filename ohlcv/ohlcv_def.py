from datetime import datetime
from enum import Enum

import pandas as pd

class MinuteDF:
    """분봉 데이터 프레임 정의"""
    
    # 데이터프레임에서 컬럼의 순서를 지정하는 튜플입니다.
    column_orders = ('체결시간', '시가', '고가', '저가', '현재가', '거래량')
    
    # 각 컬럼의 데이터 타입을 지정하는 딕셔너리입니다.
    column_types = {
        '체결시간': str, '시가': float, '고가': float, '저가': float, '현재가': float, '거래량': int
    }

    # 이 클래스 메소드는 데이터프레임의 컬럼 이름을 재정의합니다.
    @classmethod
    def preprocess_data(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df[cls.column_orders]   # 필요한 필드만 사용함, 분봉의 경우 다른 필드는 값이 채워져 있지 않음

        # 컬럼 순서를 바꾼다
        for column_name in cls.column_orders[::-1]:
            df.insert(0, column_name, df.pop(column_name))

        # 문자열을 가격 데이터를 숫자로 변환하고, 하락을 의미하는 음수로 표시를 제거함
        for column_name in cls.column_orders:
            if column_name == '체결시간':
                df[column_name] = df[column_name].apply(lambda x: datetime.strptime(x, '%Y%m%d%H%M%S'))
            elif column_name == '거래량':
                df[column_name] = df[column_name].apply(lambda x: abs(int(x)))
            else:
                df[column_name] = df[column_name].apply(lambda x: abs(float(x)))
        return df

class MinuteTicks(int, Enum):
    """분봉 Tick Value"""
    MIN_1 = 1
    MIN_3 = 3
    MIN_5 = 5
    MIN_10 = 10
    MIN_15 = 15
    MIN_30 = 30
    MIN_45 = 45
    MIN_60 = 60
