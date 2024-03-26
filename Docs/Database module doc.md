# Database Module

Database moduel using an abstract class to define the interface of the database. The database module is used to connect to Local database.

## Base class `Database`

Provides an abstract class to define the interface of the database.  
It is based on the `sqlalchemy` package. Using `get_engine()` to get a sqlalchemy engine object.

### Required Attributes

- `host`: The host of the database.
- `port`: The port of the database.
- `user`: The user of the database.
- `password`: The password of the database.
- `database`: The database name.

### Methods

- `_create_engine()`: Create a database engine.
- `get_engine()`: Get a sqlalchemy engine object.

### Example

```python
import pandas as pd
from bagelfinance.database import Database, MySQL
from sqlalchemy import Engine, text

# Create MySQL database object
mysql_database: Database = MySQL(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='test'
)

engine: Engine = mysql_database.get_engine()

# Use sqlalchemy style to interact with database
with engine.begin() as conn:
    table_names = conn.execute(text('SHOW TABLES')).fetchall()
    print([table_name[0] for table_name in table_names)

# Use pandas to interact with database
df = pd.read_sql('SELECT * FROM table_name', engine)
print(df)

```

## ALl subclasses of `Database`

- `MySQL`: Connect to MySQL database.
