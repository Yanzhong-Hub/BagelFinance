"""
Database connection
Author: Yanzhong Huang
Email: bagelquant@gmail.com
"""

from sqlalchemy import create_engine, Engine
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass(slots=True)
class Database(ABC):
    """
    database module abstract class
    """

    host: str
    port: int
    user: str
    password: str
    database: str

    engine: Engine = field(init=False)

    def __post_init__(self):
        self.engine = self._create_engine()

    @abstractmethod
    def _create_engine(self) -> Engine:
        """create engine"""
        ...

    def get_engine(self) -> Engine:
        """get engine for outside usage"""
        return self.engine


class MySQL(Database):
    """
    MySQL database connection, use pymysql
    """

    def _create_engine(self) -> Engine:
        return create_engine(
            f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )
