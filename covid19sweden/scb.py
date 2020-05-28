
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
        """Deaths on county level from 2018 to 2020.
        
        Returns:
            data (dataframe): daily county records from 2018 - 2020
            total (dataframe): total county records from 2018 - 2020
            unknown (dataframe): unknown records (not assigned to days)
        """
        # clean excel table
        sheet = self._wb["Tabell 3"]
        sheet.delete_rows(889,500)
        sheet.delete_rows(1,9)
        sheet.delete_cols(24,5)
        # parse to pandas
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0})
        # columns
        data.columns = ["date","year","SE010","SE021","SE022","SE023",
                        "SE091","SE092","SE093","SE094","SE041","SE044",
                        "SE0A1","SE0A2","SE061","SE024","SE025","SE062",
                        "SE063","SE071","SE072","SE081","SE082"]
        
        # separate
        unknown = data.iloc[-6:-3,:]
        total = data.iloc[-3:,:]
        data = data.iloc[:-6,:]
        # parse date
        locale.setlocale(locale.LC_TIME, "sv_SE")
        data["date"] = (data["date"]+" "+data["year"].apply(lambda x: str(x))).apply(self._parse_date)
        data = data.sort_values(['date'], ascending=[1]).reset_index(drop = True).drop(["year"], axis=1)
        # parse total
        total["date"] = total["year"].apply(lambda x: datetime.strptime(str(x), "%Y"))
        total = total.drop(["year"], axis=1).reset_index(drop = True)
        # parse unknown
        unknown["date"] = unknown["year"].apply(lambda x: datetime.strptime(str(x), "%Y"))
        unknown = unknown.drop(["year"], axis=1).reset_index(drop = True)
        
        return data, total, unknown
        
    def municipality_18to20_10days(self): # table 4
        # clean excel table
        sheet = self._wb["Tabell 4"]
        #sheet.delete_rows(889,500)
        sheet.delete_rows(1,12)
        sheet.delete_cols(41,3)
        # parse to pandas
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0})
        
        data.columns = ["year","code","municipality","total",*[f"{month}-{day+1};{month}-{day+10}" for month in range(1,13) for day in range(0,21,10) ], "unknown"]
        data = pd.melt(data, id_vars = ['date'],
                       value_vars = ['2015','2016','2017','2018','2019','2020'],
                       var_name = 'year', value_name = 'deaths')
        print(data)
    def country_15to20_week_sex(self): # table 5
        # clean excel table
        sheet = self._wb["Tabell 5"]
        #sheet.delete_rows(889,500)
        #sheet.delete_rows(1,12)
        #sheet.delete_cols(41,3)
        # parse to pandas
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0})
        print(data)
    def county_15to20_week(self): # table 6
        # clean excel table
        sheet = self._wb["Tabell 6"]
        #sheet.delete_rows(889,500)
        #sheet.delete_rows(1,12)
        #sheet.delete_cols(41,3)
        # parse to pandas
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0})
        print(data)
    def country_15to20_week_age_sex(self): # table 7
        # clean excel table
        sheet = self._wb["Tabell 7"]
        #sheet.delete_rows(889,500)
        #sheet.delete_rows(1,12)
        #sheet.delete_cols(41,3)
        # parse to pandas
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0})
        print(data)
    def country_20_day_release(self): # table 8
        # clean excel table
        sheet = self._wb["Tabell 8"]
        #sheet.delete_rows(889,500)
        #sheet.delete_rows(1,12)
        #sheet.delete_cols(41,3)
        # parse to pandas
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0})
        print(data)

if __name__ == "__main__":
    d = Deaths()
    d.country_20_day_release()
    