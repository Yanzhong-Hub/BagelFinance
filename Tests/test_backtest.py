"""test backtest module"""

import os
import json
import pandas as pd
import unittest
from unittest import TestCase

from BagelFinance.database import MySQL
from BagelFinance.backtest import Backtest
from datetime import datetime
import matplotlib.pyplot as plt


class TestBackTest(TestCase):
    
    def setUp(self):
        """load database config from Tests/test_config.json"""
        with open(os.path.join(os.path.dirname(__file__), "test_config.json")) as f:
            self.db_config = json.load(f)['database_config']
        
        self.mysql = MySQL(**self.db_config)
        self.engine = self.mysql.get_engine()

        # backtest setting
        self.start = datetime(2019, 1, 1)
        self.end = datetime(2021, 12, 31)

    def test_backtest(self):

        """test database"""
        bt = Backtest(self.engine, self.start, self.end)
        bt.initial_capital = 10_000_000
        bt.add_transaction_df(
            pd.DataFrame(
                {'000001.SZ': [100, 200],
                 '000002.SZ': [100, 100],
                 '000003.SZ': [100, 100],
                 '000004.SZ': [100, 100],
                 '000005.SZ': [100, 100],}, 
                 index=[datetime(2019, 1, 3),
                        datetime(2019, 1, 4)]
            )
        )

        bt.run()
        # bt.plot_price_accumulate_return()
        # bt.plot_price()
        # bt.plot_transactions()
        # bt.plot_drifts_hist('000001.SZ')
        # bt.plot_drifts_hist('000002.SZ')
        bt.plot_cash()
        bt.plot_portfolio()
        bt.plot_portfolio_accumulate_return()
        bt.plot_drifts_hist('portfolio')
        plt.show()


if __name__ == '__main__':
    unittest.main()
