
from datetime import datetime,timedelta
import unittest

import pandas as pd

# tested component
import covid19sweden as SE

class TestCovid(unittest.TestCase):
    def test_level_1(self):
        x = SE.covid_deaths(level = 1)
        self.assertIsInstance(x, pd.DataFrame)
        print(1)
        print(x)
    def test_level_2(self):
        x = SE.covid_deaths(level = 2)
        self.assertIsInstance(x, pd.DataFrame)
        print(2)
        print(x)
        

__all__ = ["TestCovid"]