
import logging
logging.basicConfig(level = logging.INFO)
import sys
sys.path.append(".")

import covid19sweden
covid19sweden.fohm.regions(filename = "regions.csv")
covid19sweden.fohm.municipalities(filename = "municipalities.csv")