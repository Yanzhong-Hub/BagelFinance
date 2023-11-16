from pandas import Timestamp
from pandas import Series

from dataclasses import dataclass, field
from typing import Iterable

from abc import ABC, abstractmethod


@dataclass(slots=True)
class TimeSeries(ABC):
    
    code: str
    time_range: Iterable[Timestamp]

    data: Series = field(init=False)

    @abstractmethod
    def _set_data(self) -> None:
        # TODO self.data = SOMETHING HERE 
        pass


class Stock(TimeSeries):
    
    def _set_data(self) -> None:
        # TODO self.data = SOMETHING HERE 
        pass





    
    