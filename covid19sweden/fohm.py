
from datetime import datetime,timedelta
from io import BytesIO
import tempfile

from bs4 import BeautifulSoup
from waybackmachine import WaybackMachine

import openpyxl as pyxl
import pandas as pd
import requests


class FOHM:
    #_url = 'https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/'
    _url = 'https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data'
    _response = None
    def read_municipalities(self):
        # load
        if not self._response:
            self._response = requests.get(self._url)
        data     = pd.read_excel(BytesIO(self._response.content),'Veckodata Kommun_stadsdel')
        # columns
        data.columns = ["week","municipality_code","municipality","district",
                        "municipality_district","confirmed_total_per10K",
                        "confirmed_newly_per10K","confirmed_total","confirmed_newly"]
        # values
        data = data.where(pd.notnull(data), None)
        return data
    def read_regions(self):
        # load
        if not self._response:
            self._response = requests.get(self._url)
        data     = pd.read_excel(BytesIO(self._response.content),'Veckodata Region')
        # columns
        data.columns = ["week","region","confirmed","confirmed_total",
                        "icu","icu_total","deaths","deaths_total",
                        "confirmed_newly_per100K","confirmed_total_per100K"]
        # values
        data = data.where(pd.notnull(data), None)
        return data
        
def municipalities(filename = None):
    x = FOHM()
    municipalities = x.read_municipalities()
    if filename:
        municipalities.to_csv(filename, index = False)
    return municipalities
def regions(filename = None):
    x = FOHM()
    regions = x.read_regions()
    if filename:
        regions.to_csv(filename, index = False)
    return regions
    

__all__ = ["regions","municipalities"]