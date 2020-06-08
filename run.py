
import logging
logging.basicConfig(level = logging.INFO)
import sys
sys.path.append(".")

import covid19sweden
covid19sweden.commit(overwrite = True)