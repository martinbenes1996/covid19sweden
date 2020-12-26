
from datetime import datetime,timedelta
from io import BytesIO
import pkg_resources
import tempfile

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
        data = pd.read_excel(BytesIO(self._response.content),'Veckodata Kommun_stadsdel', engine='openpyxl')
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
        data = pd.read_excel(BytesIO(self._response.content),'Veckodata Region', engine='openpyxl')
        # columns
        data.columns = ["year","week","region","confirmed","confirmed_total",
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
    nuts3 = {
        'Blekinge': 'SE221','Dalarna': 'SE312','Gotland': 'SE214','Gävleborg': 'SE313','Halland': 'SE231',
        'Jämtland Härjedalen': 'SE322','Jönköping': 'SE211','Kalmar': 'SE213','Kronoberg': 'SE212',
        'Norrbotten': 'SE332','Skåne': 'SE224','Stockholm': 'SE110','Sörmland': 'SE122','Uppsala': 'SE121',
        'Värmland': 'SE311','Västerbotten': 'SE331','Västernorrland': 'SE321','Västmanland': 'SE125',
        'Västra Götaland': 'SE232','Örebro': 'SE124','Östergötland': 'SE124'}
    regions["NUTS_ID"] = regions.region.apply(lambda r: nuts3[r])
    if filename:
        regions.to_csv(filename, index = False)
        
    return regions

    
__all__ = ["regions","municipalities"]