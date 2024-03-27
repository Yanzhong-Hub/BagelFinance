# Backtest

This Python module, `backtest.py`, is part of the BagelFinance project. It is responsible for backtesting financial strategies over a specified period.

## Backtest Class

The `Backtest` class is a data class that represents a backtest of a financial strategy. It has the following attributes:

Required attributes:

- `engine`: An instance of `sqlalchemy.Engine` for database interaction. This is not represented in the string representation of the class.
- `start`: A `datetime.datetime` object representing the start date of the backtest.
- `end`: A `datetime.datetime` object representing the end date of the backtest.
- `initial_capital`: A float representing the initial capital for the backtest. The default value is 1,000,000.0.

## Usage

1. Initialize a `Backtest` object with the required attributes.
2. Add `transactions` to the backtest using the `add_transaction` or `add_transaction_df` methods.
3. Use `Backtest.run()` to run the backtest and get the results.
4. Use `Backtest.plot_portfolio()` to plot the portfolio value over time. Or other plot methods to plot other metrics.

```python
from bagelfinance.backtest import Backtest
from bagelfinance.database import MySQL
import matplotlib.pyplot as plt

# Create MySQL database object
mysql_database: Database = MySQL(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='test'
)

engine = mysql_database.get_engine()

# Initialize a Backtest object
backtest = Backtest(
    engine=engine,
    start=datetime(2019, 1, 1),
    end=datetime(2020, 1, 1),
    initial_capital=1000000.0
)

# Add transactions to the backtest
backtest.add_transaction(
    trade_date=datetime(2019, 1, 3),
    code='000001.SZ',
    amount=100
)

backtest.add_transaction_df(
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

# Run the backtest
backtest.run()

# Results and plots
print(backtest.portfolio['portfolio'])
print(backtest.portfolio['cash'])

backtest.plot_price()
backtest.plot_portfolio()
backtest.plot_portfolio_accumulate_return()
backtest.plot_drifts_hist('portfolio')

plt.show()
```
