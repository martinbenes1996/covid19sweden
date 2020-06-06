
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
    
    def _start_parsing_date(self):
        locale.setlocale(locale.LC_TIME, "sv_SE")
        self._leap_records, self._unknown_death_date = [], []
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
    def __init__(self, offline = False):
        if not offline:
            u = requests.get(self._url)
            fd = BytesIO(u.content)
        else:
            fd = "2020-05-22-preliminar_statistik_over_doda_inkl_eng.xlsx"
        self._wb = pyxl.load_workbook( fd )
        self._leap_records, self._unknown_death_date = [], []
    def get_xlsx_input(self):
        return self._wb
        
    def country_15to20_day(self): # table 1
        """Deaths on country level from 2015 to 2020 per day.
        
        Returns:
            data (dataframe): the deaths from each day
            average (dataframe): the average from each day
            unk (dataframe): yearly deaths with unknown day
        """
        # parse table
        sheet = self._wb["Tabell 1"]
        data = pd.DataFrame(sheet.values)
        data = data.iloc[7:,:-6]
        data.columns = ["date","2015","2016","2017","2018","2019","2020","average"]
        # separate average
        average = data[["date","average"]]
        # wide to long
        data = pd.melt(data, id_vars = ['date'], var_name = 'year', value_name = 'deaths',
                       value_vars = ['2015','2016','2017','2018','2019','2020'])
        # separate data and unknown
        data,unk = data[:-1],data[-1:]
        # parse date
        data['date'] = data['date'] + ' ' + data['year']
        self._start_parsing_date()
        data["date"] = data["date"].apply(self._parse_date)
        # unknown deaths
        unk = data[data['date'].isin(self._unknown_death_date)]
        unk = unk.drop(['date'], axis=1).reset_index(drop = True)
        # process dates
        data = data[~data['date'].isin(self._leap_records)]
        data = data[~data['date'].isin(self._unknown_death_date)]
        data = data.drop(["year"], axis=1)
        # average
        average["date"] += " 2020"
        self._start_parsing_date()
        average["date"] = average["date"].apply(self._parse_date)
        average = average[~average['date'].isin(self._unknown_death_date)]
        
        return data, average, unk
        
    def country_19to20_day_sex_age(self): # table 2
        """Deaths on country level from 2019 to 2020 per sex and age group.
        
        Returns:
            data (dataframe): Daily records from 2019-2020
            unknown (dataframe): unknown records (not assigned to days)
        """
        # parse table
        sheet = self._wb["Tabell 2"]
        data = pd.DataFrame(sheet.values)
        data_2019 = data.iloc[8:,:10]
        data_2020 = pd.concat([data.iloc[8:,0], data.iloc[8:,10:19]], axis=1)
        data_2020.columns = data_2019.columns = ["date","total",
                                                 "M0-64","M65-79","M80-89","M90+",
                                                 "F0-64","F65-79","F80-89","F90+"]
        # unknown
        unknown_2019 = pd.concat([pd.DataFrame(), data_2019.iloc[-1:,1:]])
        unknown_2020 = data_2020.iloc[-1:,1:]
        # parse date
        self._start_parsing_date()
        data_2019["date"] = (data_2019["date"] + " 2019").apply(self._parse_date)
        data_2020["date"] = (data_2020["date"] + " 2020").apply(self._parse_date)
        unknown_2019["year"] = 2019
        unknown_2020["year"] = 2020
        # result
        return pd.concat([data_2019, data_2020]), None, pd.concat([unknown_2019, unknown_2020])
    
    def county_18to20_day(self): # table 3
        """Deaths on county level from 2018 to 2020.
        
        Returns:
            data (dataframe): daily county records from 2018 - 2020
            total (dataframe): total county records from 2018 - 2020
            unknown (dataframe): unknown records (not assigned to days)
        """
        # parse table
        sheet = self._wb["Tabell 3"]
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0})
        data = data.iloc[9:888,:23]
        data.columns = ["date","year","SE010","SE021","SE022","SE023","SE091","SE092",
                        "SE093","SE094","SE041","SE044","SE0A1","SE0A2","SE061","SE024",
                        "SE025","SE062","SE063","SE071","SE072","SE081","SE082"]
        # separate unknown, total, unknown
        unknown = data.iloc[-6:-3,:]
        total = data.iloc[-3:,:]
        data = data.iloc[:-6,:]
        self._start_parsing_date()
        data["date"] = (data["date"]+" "+data["year"].apply(lambda x: str(x))).apply(self._parse_date)
        data = data.sort_values(['date'], ascending=[1]).reset_index(drop = True).drop(["year"], axis=1)
        total["date"] = total["year"].apply(lambda x: datetime.strptime(str(x), "%Y"))
        total = total.drop(["year"], axis=1).reset_index(drop = True)
        unknown["date"] = unknown["year"].apply(lambda x: datetime.strptime(str(x), "%Y"))
        unknown = unknown.drop(["year"], axis=1).reset_index(drop = True)
        
        return data, total, unknown
        
    def municipality_18to20_10days(self): # table 4
        """Deaths on county level from 2018 to 2020.
        
        Returns:
            data (dataframe): daily municipality records from 2018 - 2020
            total (dataframe): total municipality records from 2018 - 2020
            unknown (dataframe): unknown records (not assigned to days)
        """
        # parse table
        sheet = self._wb["Tabell 4"]
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0})
        data = data.iloc[12:,:-3]
        tendays = [f"{month}-{day+1}"
                   for month in range(1,13) for day in range(0,21,10) ]
        data.columns = ["year","code","municipality","total",*tendays,"unknown"]
        # total/unknown per municipality
        aggregated = data.loc[:,["year","code","municipality","total","unknown"]]
        aggregated["date"] = aggregated["year"].apply(lambda x: datetime.strptime(str(x), "%Y"))
        total = aggregated.drop(["year","unknown"], axis=1)
        unknown = aggregated.drop(["year","total"], axis=1)
        # wide to long
        data = pd.melt(data, id_vars = ['year','code','municipality'],
                       var_name = 'date', value_name = 'deaths', value_vars = tendays)
        data['date'] = (data['year'] + "-" + data['date']).apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        data = data.drop("year", axis=1)
        
        return data,total,unknown
    
    def country_15to20_week_sex(self): # table 5
        """Deaths on country level from 2015 to 2020 by week by sex.
        
        Returns:
            data (dataframe): daily municipality records from 2018 - 2020
        """
        # parse table
        sheet = self._wb["Tabell 5"]
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0})
        data = data.iloc[11:64,:24].reset_index(drop = True)
        years = [str(y) for y in range(2015,2021)]
        data.columns = ["week",*years, "avg", "empty1", *["F"+y for y in [*years,"avg"]], "empty2", *["M"+y for y in [*years,"avg"]]]
        data = data.drop(["empty1","empty2"], axis=1)
        
        return data, None, None
        
    def county_15to20_week(self): # table 6
        """Deaths on county level from 2015 to 2020 by week
        
        Returns:
            data (dataframe): daily municipality records from 2018 - 2020
            total (dataframe): total municipality records from 2018 - 2020
            unknown (dataframe): unknown records (not assigned to days)
        """
        # parse table
        sheet = self._wb["Tabell 6"]
        df = pd.DataFrame(sheet.values)
        df = df.replace({'..': 0})
        data = df.iloc[12:66,:45]
        # parse counties
        counties = df.iloc[8,3:]
        counties = counties[~counties.isnull()]
        # columns
        county_columns = []
        for c in counties:
            county_columns.append(f"avg1519_{c}")
            county_columns.append(f"2020_{c}")
        data.columns = ["week","avg1519","2020",*county_columns]
        # parse unknown
        unknown = data.iloc[-1:,1:].reset_index(drop = True)
        data = data.iloc[:-1,:].reset_index(drop = True)
        # parse total
        total = data[["week","avg1519","2020"]]
        data = data.drop(["avg1519","2020"], axis=1)
        
        return data, total, unknown
    
    def country_15to20_week_age_sex(self): # table 7
        """Deaths on county level from 2015 to 2020 by week by age by sex.
        
        Returns:
            data (dataframe): weekly records per gender and age group for 2015 - 2019 (average) and in 2020
            total (dataframe): total weekly deaths (throughout genders and ages) in 2015 - 2019 (average) and 2020
            unknown (dataframe): unknown records (not assigned to weeks)
        """
        # parse table
        sheet = self._wb["Tabell 7"]
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0})
        data = data.iloc[9:-3,:-3].reset_index(drop = True)
        # columns
        age = ["0-64","65-79","80-89","90+"]
        gender = [g + "_" + a for g in ["M","F"] for a in age]
        cols1519 = [y + "_" + g for y in ["2015-2019"] for g in gender ]
        cols20 = [y + "_" + g for y in ["2020"] for g in gender ]
        data.columns = ["week", "2015-2019", *cols1519, "2020", *cols20]
        # unknown, total
        unknown = data.iloc[-1:, 1:]
        total = data[["week","2015-2019","2020"]]
        data = data.iloc[:-1,:].drop(["2015-2019","2020"], axis=1)

        return data, total, unknown
    
    def country_20_day_release(self): # table 8
        # parse date
        sheet = self._wb["Tabell 8"]
        data = pd.DataFrame(sheet.values)
        data = data.replace({'..': 0}).replace({None: 0})
        data = data.iloc[6:,:].reset_index(drop = True)
        # columns
        self._start_parsing_date()
        dates = (data.iloc[0,1:] + " 2020").apply(self._parse_date).apply(lambda c: c.strftime("%Y-%m-%d")).tolist()
        data = data.iloc[1:,:].reset_index(drop = True)
        data.columns = ["date", *dates]
        # unknown
        unknown = data.iloc[-1:,1:].reset_index(drop = True)
        unknown = pd.melt(unknown, var_name = 'release', value_name = 'deaths', value_vars = dates)
        data = data.iloc[:-1,:].reset_index(drop = True)
        # parse dates
        data["date"] = (data["date"] + " 2020").apply(self._parse_date)
        data = pd.melt(data, id_vars = ['date'],
                       var_name = 'release', value_name = 'deaths', value_vars = dates)
        data["release"] = data["release"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        
        return data,None,unknown

if __name__ == "__main__":
    d = Deaths(offline = True)
    data = d.country_15to20_week_sex()
    print(data)
    