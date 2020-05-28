
from datetime import datetime
from io import BytesIO
import locale
import tempfile

import openpyxl as pyxl
import pandas as pd
import requests


class Deaths:
    # TODO
    _url = 'https://scb.se/contentassets/edc2b33f85ad415d8e7909002253ed84/2020-05-22-preliminar_statistik_over_doda_inkl_eng.xlsx'    
    
    def _parse_date(self, d):
        try:
            return datetime.strptime(d, "%d %B %Y")
        except:
            if d[:2] == "29":
                self._leap_records.append(d)
            elif d[:5] == "Okänd":
                self._unknown_death_date.append(d)
            else: raise
            return d
    def __init__(self):
        u = requests.get(self._url)
        self._wb = pyxl.load_workbook( BytesIO(u.content) )
        self._leap_records, self._unknown_death_date = [], []
        
    def country_15to20_day(self): # table 1
        """Deaths on country level from 2015 to 2020 per day.
        
        Returns:
            data (dataframe): the deaths from each day
            average (dataframe): the average from each day
            unk (dataframe): yearly deaths with unknown day
        """
        # clean excel table
        sheet = self._wb["Tabell 1"]
        sheet.delete_rows(1,7)
        sheet.delete_cols(9,6)
        # parse to pandas
        data = pd.DataFrame(sheet.values)
        data.columns = ["date","2015","2016","2017","2018","2019","2020","average"]
        
        average = data[["date","average"]]
        
        data = pd.melt(data, id_vars = ['date'],
                       value_vars = ['2015','2016','2017','2018','2019','2020'],
                       var_name = 'year', value_name = 'deaths')
        data,unk = data[:-1],data[-1:]
        data['date'] = data['date'] + ' ' + data['year']
        
        locale.setlocale(locale.LC_TIME, "sv_SE")
        data["date"] = data["date"].apply(self._parse_date)
        # unknown deaths
        unk = data[data['date'].isin(self._unknown_death_date)]
        unk = unk.drop(['date'], axis=1).reset_index(drop = True)
        # date data
        data = data[~data['date'].isin(self._leap_records)]
        data = data[~data['date'].isin(self._unknown_death_date)]
        data = data.drop(["year"], axis=1)
        # average
        self._leap_records, self._unknown_death_date = [], []
        average["date"] += " 2020"
        average["date"] = average["date"].apply(self._parse_date)
        average = average[~average['date'].isin(self._unknown_death_date)]
        
        return data, average, unk
        
    def country_19to20_day_sex_age(self): # table 2
        """Deaths on country level from 2019 to 2020 per sex and age group.
        
        Returns:
            data (dataframe): Daily records from 2019-2020
            unknown (dataframe): unknown records (not assigned to days)
        """
        # clean excel table
        sheet = self._wb["Tabell 2"]
        sheet.delete_rows(1,8)
        sheet.delete_cols(20,4)
        # parse to pandas
        data = pd.DataFrame(sheet.values)
        data_2019 = data.iloc[:,:10]
        data_2020 = pd.concat([data.iloc[:,0], data.iloc[:,10:]], axis=1)
        data_2020.columns = data_2019.columns = ["date","total","M0-64","M65-79","M80-89","M90+","F0-64","F65-79","F80-89","F90+"]
        unknown_2019 = pd.concat([pd.DataFrame(), data_2019.iloc[-1:,1:]])
        unknown_2020 = data_2020.iloc[-1:,1:]
        # parse date
        locale.setlocale(locale.LC_TIME, "sv_SE")
        data_2019["date"] = (data_2019["date"] + " 2019").apply(self._parse_date)
        data_2020["date"] = (data_2020["date"] + " 2020").apply(self._parse_date)
        unknown_2019["year"] = 2019
        unknown_2020["year"] = 2020
        # result
        return pd.concat([data_2019, data_2020]), pd.concat([unknown_2019, unknown_2020])
    def county_18to20_day(self): # table 3
        # clean excel table
        sheet = self._wb["Tabell 3"]
        sheet.delete_rows(1,9)
        sheet.delete_cols(20,4)
        # parse to pandas
        data = pd.DataFrame(sheet.values)
        print(data)
    def municipality_18to20_10days(self): # table 4
        pass
    def country_15to20_week_sex(self): # table 5
        pass
    def county_15to20_week(self): # table 6
        pass
    def country_15to20_week_age_sex(self): # table 7
        pass
    def country_20_day_release(self): # table 8
        pass

if __name__ == "__main__":
    d = Deaths()
    d.county_18to20_day()