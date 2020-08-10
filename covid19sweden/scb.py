
import csv
from io import StringIO
import pkg_resources

import pandas as pd
import requests

def _parse_deaths():
    url = 'http://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0101/BE0101I/DodaFodelsearK'
    query = { 
        "query": [{
            "code": "Region",
            "selection": {
                "filter": "agg:RegionNUTS3_2008",
                "values": [
                    "SE110","SE121","SE122","SE123","SE124",
                    "SE125","SE211","SE212","SE213","SE214",
                    "SE221","SE224","SE231","SE232","SE311",
                    "SE312","SE313","SE321","SE322","SE331","SE332"
                ]
            }
        },{
            "code": "Alder",
            "selection": {
                "filter": "agg:Ålder10år",
                "values": ["-4","5-14","15-24","25-34","35-44","45-54","55-64","65-74","75-84","85-94","95+"]
            }
        },{
            "code": "Kon",
            "selection": {
                "filter": "item",
                "values": ["1","2"]
            }
        }],
        "response": {"format": "csv"}
    }
    # get data
    res = requests.post(url, json = query)
    x = pd.read_csv( StringIO(res.text) )
    # parse data
    x.columns = ["region","age","sex"] + [str(y) for y in range(1968,2020)]
    x.sex = x.sex.apply(lambda i: "F" if i == "kvinnor" else "M")
    x["region_code"] = x.region.apply(lambda i: i.split(" ")[0])
    x["region_name"] = x.region.apply(lambda i: " ".join(i.split(" ")[1:]) )
    x.drop("region", axis = 1, inplace = True)
    x.age = x.age.apply(lambda i: i[:-3])
    x = x[["region_code","region_name","age","sex"] + [str(y) for y in range(1968,2020)]]
    # save
    x.to_csv(pkg_resources.resource_filename(__name__, "data/deaths.csv"), index = False)
    return x

def deaths(offline = True):
    x = _parse_deaths()
    return x

__all__ = ["deaths"]
    