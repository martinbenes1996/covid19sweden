
from datetime import datetime,timedelta
import tempfile

from bs4 import BeautifulSoup
from waybackmachine import WaybackMachine

import openpyxl as pyxl
import pandas as pd
import requests


class FOHM:
    _url = 'https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/'
    def __init__(self):
        pass
    def read(self):
        for response,version_time in WaybackMachine(self._url, end = "2020-03-11", step = timedelta(days=1)):
            tree = BeautifulSoup(response, features="lxml")
            link = tree.find("a", {"title": "Excel-fil"})['href']
            print(link)

def fohm():
    x = FOHM()
    x.read()

__all__ = ["fohm"]