
from datetime import datetime,timedelta
import unittest

import pandas as pd

# tested component
from covid19sweden import fohm

class TestFOHM(unittest.TestCase):
    def test_municipalities(self):
        y = fohm.municipalities()
        self.assertIsInstance(y, pd.DataFrame)
        
    def test_regions(self):
        x = fohm.regions()
        self.assertIsInstance(x, pd.DataFrame)