"""

Author: Yanzhong Huang
Email: bagelquant@gmail.com
"""
import os
import json
from unittest import TestCase
from BagelFinance.database import MySQL
from BagelFinance.query import query_pv, query_fundamental
from datetime import datetime
from sqlalchemy import text


class TestQuery(TestCase):
    def setUp(self):
        """load database config from Tests/test_config.json"""
        # database
        with open(os.path.join(os.path.dirname(__file__), "test_config.json")) as f:
            self.db_config = json.load(f)['database_config']
        self.db = MySQL(**self.db_config)
        self.engine = self.db.get_engine()

        # test date range and codes
        self.date_range = (datetime(2020, 1, 1), datetime(2020, 12, 31))
        self.codes = ["000001.SZ", "000002.SZ", "000004.SZ"]

        # all stock ts_codes
        sql: str = "SELECT ts_code FROM stock_basic"
        with self.engine.begin() as conn:
            result = conn.execute(text(sql))
            self.all_codes = [row[0] for row in result.fetchall()]

        # long term date range
        self.long_term_date_range = (datetime(2000, 1, 1), datetime(2020, 12, 31))

    def test_query_pv(self):
        df = query_pv(
            self.engine,
            "close",
            "daily",
            self.codes,
            self.date_range
        )
        print(df)

        self.assertEqual(df.shape[1], 3)

    def test_query_fundamental(self):
        df = query_fundamental(
            self.engine,
            "total_share",
            "balancesheet",
            self.codes,
            self.date_range
        )
        print(df)

        self.assertEqual(df.shape[1], 3)

    def test_query_pv_long_term(self):
        df = query_pv(
            self.engine,
            "close",
            "daily",
            self.codes,
            self.long_term_date_range
        )
        print(df)

    def test_query_fundamental_long_term(self):
        df = query_fundamental(
            self.engine,
            "total_share",
            "balancesheet",
            self.codes,
            self.long_term_date_range
        )
        print(df)

    def test_query_pv_all_codes(self):
        df = query_pv(
            self.engine,
            "close",
            "daily",
            self.all_codes,
            self.date_range
        )
        print(df)

    def test_query_fundamental_all_codes(self):
        df = query_fundamental(
            self.engine,
            "total_share",
            "balancesheet",
            self.all_codes,
            self.date_range
        )
        print(df)

    def test_query_fundamental_all_codes_long_term(self):
        df = query_fundamental(
            self.engine,
            "total_share",
            "balancesheet",
            self.all_codes,
            self.long_term_date_range
        )
        print(df)

    def test_query_pv_all_codes_long_term(self):
        df = query_pv(
            self.engine,
            "close",
            "daily",
            self.all_codes,
            self.long_term_date_range
        )
        print(df)
