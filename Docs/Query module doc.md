# Query module

Query module provides functions to interact with database. It is based on the `database` module and `sqlalchemy.Engine`.

## Data structure

Since all financial data is time series data, and a corresponding code, and it store under a specifc table. We need at least 5 parameters to query a data point.

For example: `Close` price for stock `000001.SZ` in `2020-01-01` From `daily` table.

- `engine`: `sqlalchemy.Engine`, the engine object to connect to database.
- `data_name`: `str`,  `Close`
- `table_name`: `str`, `daily`
- `codes`: `Iterable[str]`, `['000001.SZ']`, must be iterable object, even if it only contains one element.
- `date_range`: `Tuple[datetime, datetime]`, `(datetime(2020, 1, 1), datetime(2020, 1, 1))`, tuple contains start and end date.

## Query functions

All query functions in this module follows the requirements paramethers above.  

- `query_pv(engine, data_name, table_name, codes, date_range)` -> `pd.DataFrame`: Query price or volume data.
- `query_fundamental(engine, data_name, table_name, codes, date_range)` -> `pd.DataFrame`: Query fundamental data.

### Example

```python
from BagelFinance.database import MySQL  # connect to database
from BagelFinance.query import query_pv  # import query function
from datetime import datetime

# Create MySQL database object
mysql_database: Database = MySQL(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='test'
)

# query close price for stock [`000001.SZ`, `000002.SZ`] from `2019-01-01` to `2020-01-01`
df = query_pv(
    engine=mysql_database.get_engine(),
    data_name='Close',
    table_name='daily',
    codes=['000001.SZ', '000002.SZ'],
    date_range=(datetime(2019, 1, 1), datetime(2020, 1, 1))
)

print(df.head())
```
