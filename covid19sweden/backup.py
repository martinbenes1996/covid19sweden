
from datetime import datetime
import json
import logging
import os
from pathlib import Path

import pandas as pd

from . import scb

_log = logging.getLogger(__name__)

class OverwriteError(Exception):
    pass
def _run_method(f, name, overwrite):
    x = f()
    if x is None:
        x = (pd.DataFrame(),pd.DataFrame(),pd.DataFrame())
    x = [i if i is not None else pd.DataFrame() for i in x]
    x1,x2,x3 = x
    for fname in [f"{name}_1.csv",f"{name}_2.csv",f"{name}_3.csv"]:
        if os.path.exists(fname):
            if not overwrite:
                _log.error(f"File {fname} exists! Set overwrite = True to proceed.")
                raise OverwriteError
            else:
                os.remove(fname)
    x1.to_csv(f"{name}_1.csv", index = False)
    x2.to_csv(f"{name}_2.csv", index = False)
    x3.to_csv(f"{name}_3.csv", index = False)
def _write_meta(rq, name, overwrite):
    meta = {
        "source": rq.get_file_location(),
        "timestamp": rq.get_timestamp().strftime("%Y-%m-%d %H:%M:%S"),
        "filename": rq.get_file_name()
    }
    if os.path.exists(name):
        if not overwrite:
            _log.error(f"File {name} exists! Set overwrite = True to proceed.")
            raise OverwriteError
        else:
            os.remove(name)
    with open(name, "w") as fd:
        json.dump(meta, fd)

def commit(name = None, overwrite = False):
    # commit path name
    name = f"commit_{datetime.now().strftime('%Y%m%d')}" if name is None else name
    folder = Path(name)
    addmsg = " Overwritting on." if overwrite else ""
    _log.info(f"Committing to {name}.{addmsg}")
    
    try:
        os.mkdir(folder)
        _log.info(f"Directory {folder} created.")
    except OSError:
        _log.info(f"Directory {folder} exists.")
    
    # download
    _log.info("Fetching data.")
    try:
        d = scb.deaths()
    except Exception as e:
        _log.error(f"Fetching of input data failed: {e}")
        return
    _log.info("Calling parser methods, saving their outputs.")
    
    # === save ===
    d.to_csv(folder / "deaths.csv", index = False)
    
    _log.info("All done.")
    
__all__ = ["commit"]
