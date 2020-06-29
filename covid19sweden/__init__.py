# -*- coding: utf-8 -*-
"""Webscraper for Swedish data.
 
Reference: https://www.scb.se/hitta-statistik/statistik-efter-amne/befolkning/befolkningens-sammansattning/befolkningsstatistik/pong/tabell-och-diagram/preliminar-statistik-over-doda/
Todo:
    * caching
"""

import pkg_resources
from .main import *

from . import fohm
from .scb import *

from .backup import *

try:
    __version__ = pkg_resources.get_distribution("covid19sweden").version
except:
    __version__ = None