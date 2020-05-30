
import warnings

#from bs4 import BeautifulSoup
#from waybackmachine import WaybackMachine

from . import scb

def deaths(weekly = False, level = 1, per_gender_age = False, verbose = True, alt = False):
    # initialize
    d = scb.Deaths()
    total_used = True
    
    # daily country deaths
    if not weekly and level == 1 and not per_gender_age:
        total_used = False
        if verbose:
            print("To return data by release day, add parameter alt = True.")
        # regular
        if not alt:
            data,avg,unk = d.country_15to20_day()
        # by release (alt = True)
        else:
            data,unk = d.country_20_day_release()
            avg = None
    
    # daily country deaths, per gender and age
    elif not weekly and level == 1 and per_gender_age:
        total_used = False
        data,unk = d.country_19to20_day_sex_age()
        avg = None
    
    # daily regional deaths
    elif not weekly and level == 2:
        if per_gender_age and verbose:
            print("Using per_gender_age = False despite the settings.")
        data,total,unk = d.county_18to20_day()
    
    # daily city level
    elif level == 3:
        if per_gender_age or weekly:
            print("Using weekly = False, per_gender_age = False despite the settings.")
        data,total,unk = d.municipality_18to20_10days()
    
    # weekly country level per gender (and age)
    elif weekly and level == 1:
        if not per_gender_age and verbose:
            print("Using per_gender_age = True despite the settings.")
        if verbose:
            warnings.warn("2015-2019 only averaged weeks. To return data for each year (but without age groups), add parameter alt = True.")
        # per age and gender, 2015 - 2019 averaged
        if not alt:
            data,total,unk = d.country_15to20_week_age_sex()
        # per age
        else: 
            data = d.country_15to20_week_sex()
            total,unk = None,None
    
    # weekly regional level
    elif weekly and level == 2:
        if per_gender_age and verbose:
            print("Using per_gender_age = False despite the settings.")
        data,total,unk = d.county_15to20_week()
    
    # otherwise wrong error
    else:
        if verbose:
            warnings.warn("no data for given parameter settings")
            return None,None,None
    
    if total_used:
        return data,total,unk
    else:
        return data,avg,unk
        
        

        
    
    

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

__all__ = ["deaths"]