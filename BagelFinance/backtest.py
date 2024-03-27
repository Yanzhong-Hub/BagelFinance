"""Backtest module for BagelFinance"""

import pandas as pd
from dataclasses import dataclass, field
from datetime import datetime
from sqlalchemy import Engine
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from .query import query_pv


@dataclass(slots=True)
class Backtest:
    """Backtest class"""

    # required
    engine: Engine = field(repr=False)
    start: datetime
    end: datetime
    initial_capital: float = 1_000_000.0

    # auto generated
    codes: list[str] = field(default_factory=list, repr=False)
    transcations: pd.DataFrame = field(default_factory=pd.DataFrame, repr=False)
    price: pd.DataFrame = field(init=False, repr=False)
    drifts: pd.DataFrame = field(init=False, repr=False)
    amounts: pd.DataFrame = field(init=False, repr=False)
    portfolio: pd.DataFrame = field(init=False, repr=False)

    """utility"""
    def _query_price(self) -> None:
        # add codes from transactions
        self.codes = self.transcations.columns.tolist()

        self.price = query_pv(engine=self.engine, 
                              data_name='close',
                              table_name='daily',
                              codes=self.codes,
                              date_range=(self.start, self.end)).sort_index()
        
        self.drifts = self.price.pct_change().fillna(0)
    
    """transaction"""
    def add_transaction(self, trade_date: datetime, code: str, amount: int) -> None:
        add_data = pd.DataFrame(
            {code: [amount]}, index = [trade_date]
        )

        self.transcations = self.transcations.add(add_data, fill_value=0)

    def add_transaction_df(self, transaction_df: pd.DataFrame) -> None:
        self.transcations = self.transcations.add(transaction_df, fill_value=0)
    

    """plot""" 
    def plot_price(self) -> Figure:
        fig, ax = plt.subplots()
        self.price.plot(grid=True, ax=ax, title='Daily Close', ylabel='Price')
        return fig

    def plot_transactions(self) -> Figure:
        fig, ax = plt.subplots()
        self.transcations.plot(grid=True, ax=ax, title='Transactions', ylabel='Amount')
        return fig

    def plot_price_accumulate_return(self) -> Figure:
        fig, ax = plt.subplots()
        _accumulate_return = (self.drifts + 1).cumprod() - 1
        _accumulate_return.plot(grid=True, ax=ax, title='Accumulate Return', ylabel='Return')
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        return fig

    def plot_drifts_hist(self, code: str, bins: int=20) -> Figure:
        if code not in self.codes and code != 'portfolio':
            raise ValueError(f'{code} not in transactions')
        
        fig, ax = plt.subplots()
        self.drifts[code].plot(kind='hist', ax=ax, bins=bins, grid=True, title=f'{code} Drifts')
        plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
        return fig

    def plot_cash(self) -> Figure:
        fig, ax = plt.subplots()
        self.portfolio['cash'].plot(grid=True, ax=ax, title='Cash', ylabel='Cash')
        return fig
    
    def plot_portfolio(self) -> Figure:
        fig, ax = plt.subplots()
        self.portfolio['portfolio'].plot(grid=True, ax=ax, title='Portfolio', ylabel='Portfolio')
        return fig
    
    def plot_portfolio_accumulate_return(self) -> Figure:
        fig, ax = plt.subplots()
        _accumulate_return = (self.drifts['portfolio'] + 1).cumprod() - 1
        _accumulate_return.plot(grid=True, ax=ax, title='Portfolio Accumulate Return', ylabel='Return')
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        return fig
    
    """calculate portfolio"""
    def run(self) -> None:
        # query price and calculate portfolio
        if not hasattr(self, 'price'):
            self._query_price()

        # make amounts and price have the same shape
        self.amounts = self.transcations.cumsum()
        self.amounts = self.amounts.reindex(self.price.index, method='ffill').fillna(0)
        self.portfolio = self.amounts * self.price
        self.portfolio['stocks'] = self.portfolio.sum(axis=1)
        
        cash_change = self.transcations.mul(self.price, fill_value=0).sum(axis=1).cumsum() * -1
        self.portfolio['cash'] = cash_change + self.initial_capital

        self.portfolio['portfolio'] = self.portfolio['stocks'] + self.portfolio['cash']
        self.drifts['portfolio'] = self.portfolio['portfolio'].pct_change()
