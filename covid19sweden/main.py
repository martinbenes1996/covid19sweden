
import warnings

from bs4 import BeautifulSoup
from waybackmachine import WaybackMachine


def fetch_sweden():
    for response in WaybackMachine(url):
        print(response)
def fetch_regions():
    raise NotImplementedError

def fetch(level = 1, dt = None):
    if level == 1:
        return fetch_sweden()
    elif level == 2:
        return fetch_regions()
    else:
        warnings.warn("unsupported level")
        return None

__all__ = ["fetch"]