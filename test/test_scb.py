
from datetime import datetime,timedelta
import unittest

import pandas as pd

# tested component
from covid19sweden import Deaths

class TestSCB(unittest.TestCase):
    # single instance - faster test execution
    # Deaths() downloads on each instatiation
    _d = None
    @classmethod
    def setUpClass(cls):
        cls._d = Deaths()
        
    def test_country_15to20_day(self):
        x1,x2,x3 = self._d.country_15to20_day()
        
        # check column presence
        self.assertIn("date", x1.columns)
        self.assertIn("deaths", x1.columns)
        self.assertIn("date", x2.columns)
        self.assertIn("average", x2.columns)
        self.assertIn("year", x3.columns)
        self.assertIn("deaths", x3.columns)
        
        # column datatype
        self.assertTrue(x1["date"].dtype == datetime)
        self.assertEqual(str(x1["deaths"].dtype), "int64")
        self.assertTrue(all(isinstance(dt, str) for dt in x2["date"]))
        self.assertEqual(str(x2["average"].dtype), "float64")
        self.assertEqual(str(x3["year"].dtype), "int64")
        self.assertEqual(str(x3["deaths"].dtype), "int64")
        
        # value checks
        self.assertEqual(x1["date"][0], datetime(2015,1,1))
        self.assertEqual(x1["date"][2200], datetime(2020,12,31))
        self.assertTrue(all(x1["date"].diff()[1:] == timedelta(days=1)))
        self.assertTrue(all(x1["deaths"] >= 0.0))
        dateaxis = [(datetime(2020,1,1) + timedelta(days = i)).strftime("%m-%d") for i in range(366)]
        self.assertTrue(all(x2["date"] == pd.Series(dateaxis) ))
        
        
    
        
        