"""

Author: Yanzhong Huang
Email: bagelquant@gmail.com
"""

import os
import json
from unittest import TestCase
from BagelFinance.database import Database, MySQL
from sqlalchemy import Engine, text


class TestDatabase(TestCase):
    
    def setUp(self):
        """load database config from Tests/test_config.json"""
        with open(os.path.join(os.path.dirname(__file__), "test_config.json")) as f:
            self.db_config = json.load(f)['database_config']
            
    def test_mysql(self):
        mysql: Database = MySQL(
            host=self.db_config['host'],
            port=self.db_config['port'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database']
        )

        with mysql.get_engine().connect() as conn:
            results = conn.execute(text("SHOW TABLES")).fetchall()
            print([_[0] for _ in results])
