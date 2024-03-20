"""
query data

Author: Yanzhong Huang
Email: bagelquant@gmail.com
"""

from pandas import DataFrame, read_sql
from sqlalchemy import Engine
from datetime import datetime
from typing import Iterable


def query_pv(engine: Engine,
             data_name: str,
             table_name: str,
             codes: Iterable[str],
             date_range: tuple[datetime, datetime]) -> DataFrame:
    sql: str = f"""
    SELECT trade_date, ts_code, {data_name} 
    FROM {table_name} 
    WHERE trade_date BETWEEN '{date_range[0]}' AND '{date_range[1]}' 
    AND ts_code IN {tuple(codes)}"""
    df = read_sql(sql, engine, parse_dates=['trade_date'])

    # pivot table ts_code as columns, trade_date as index
    df = df.pivot(index='trade_date', columns='ts_code', values=data_name)
    return df


def query_fundamental(engine: Engine,
                      data_name: str,
                      table_name: str,
                      codes: Iterable[str],
                      date_range: tuple[datetime, datetime]) -> DataFrame:
    sql: str = f"""
    SELECT f_ann_date, ts_code, {data_name}, end_date
    FROM {table_name} 
    WHERE f_ann_date BETWEEN '{date_range[0]}' AND '{date_range[1]}' 
    AND ts_code IN {tuple(codes)} 
    AND update_flag = 1"""
    df = read_sql(sql, engine, parse_dates=['f_ann_date', 'end_date'])

    # for row with save f_ann_date, ts_code, keep the lastest 'end_date' row
    df = df.sort_values('end_date').groupby(['f_ann_date', 'ts_code']).last().reset_index()

    # pivot table ts_code as columns, trade_date as index
    df = df.pivot(index='f_ann_date', columns='ts_code', values=data_name)
    df.index.name = 'trade_date'
    return df
