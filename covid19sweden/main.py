
import warnings

from . import fohm
from . import scb


def deaths(offline = True):
    x = scb.deaths(offline = offline)
    return x

def covid_deaths(level = 2):
    if level in {1,2}:
        x = fohm.regions()
        x = x[["week","NUTS_ID","region","deaths","confirmed","icu","confirmed_newly_per100K"]]
        x.columns = ["week", "region", "region_name", "deaths", "confirmed", "icu", "confirmed_per100k"]
        if level == 2:
            return x
        else:
            return x.groupby("week").sum().reset_index()

    elif level == 3:
        return fohm.municipalities()

if __name__ == "__main__":
    covid_deaths()
    
    

#def fetch_sweden():
#    for response in WaybackMachine(url):
#        print(response)
#def fetch_regions():
#    raise NotImplementedError

#def fetch(level = 1, dt = None):
#    if level == 1:
#        return fetch_sweden()
#    elif level == 2:
#        return fetch_regions()
#    else:
#        warnings.warn("unsupported level")
#        return None

__all__ = ["deaths","covid_deaths"]
