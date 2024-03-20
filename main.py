"""
main
Author: Yanzhong Huang
Email: bagelquant@gmail.com
"""

import json
from time import perf_counter
from BagelFinance.database import MySQL


def main() -> None:
    with open("Tests/test_config.json") as f:
        db_config = json.load(f)['database_config']
    db = MySQL(**db_config)

    #


if __name__ == '__main__':
    start = perf_counter()
    main()
    time_cost = perf_counter() - start
    print(f"Time cost: {time_cost:.2f} seconds")
