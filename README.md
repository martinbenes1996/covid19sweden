
# Web Scraper of COVID-19 data for Sweden

Python package [covid19sweden](https://pypi.org/project/covid19sweden/) provides access to mortality and COVID-19 data of Sweden.

The data is scraped from:
* https://scb.se/om-scb/nyheter-och-pressmeddelanden/overdodligheten-fortsatter-att-sjunka-efter-toppen-i-april/

## Setup and usage

Install from [pip](https://pypi.org/project/covid19sweden/) with

```python
pip install covid19sweden
```

Only function currently is `death()`, fetching the data of deaths. Use it as

```python
import covid19sweden as SWE

data,data2,unknown = SWE.deaths()
```

Package is regularly updated. Update with

```bash
pip install --upgrade covid19sweden
```

## Parametrization

### Return value

The first obvious thing is interpretation of return values.

The function returns three values:

* first return value `data` is the main return value.
* second return value `data2` is often averaged or total values, where descriptors (age, gender) are marginalized out.
* third return value `unknown` is deaths, that were for some reason not assigned to weeks / days, for example when the death date is not known.

To find out interpretation of each value in each parameter configuration, see `scb.py` in the package source code.

### Level

Level is a setting for granularity of data

1. Country level (default)
2. State level
3. Municipality level

```python
import covid19sweden as SWE

# country level
x1a,x1b,x1u = SWE.deaths(level = 1)
# state level
x2a,x2b,x2u = SWE.deaths(level = 2)
# municipality level
x3a,x3b,x3u = SWE.deaths(level = 3)
```

By default the level is 1. Level settings can be implicitly changed in the function.

### Weekly

Weekly is a setting of time axis of the data.

* `True` - data are by weeks
* `False` - data are by days

Default is `False`, data by days.

```python
import covid19sweden as SWE

# weekly
xa,xb,xu = SWE.deaths(weekly = True)
```

Given setting will implicitly change `per_gender_age = True`, even though default is `False`. This behavior is described at section [Verbose and alt](#Verbose-and-alt).

Setting of `weekly` can be also implicitly changed if no data is available for given settings.

### Per gender or age

The settings `per_gender_age` is controlling the deaths to be splitted into groups by gender (M,F) and age groups (mostly 0-64,65-79,80-89,90+).

```python
import covid19sweden as SWE

# weekly
xa,xb,xu = SWE.deaths(per_gender_age = True)
```

Setting of `per_gender_age` can be implicitly changed if no data is available for given settings.

### Verbose and alt

Not for all the combinations of the parameters the data is available. E.g. for `level = 3`, only daily data without gender and age distinguishing is available. Hence to minimize error rate, implicit parameter changes are introduced.

If the data for given settings is not available, a set of rules is applied to reach data:

* if data is available for `not per_gender_age`, use them
* if data is available for `not weekly`, use them
* if data is available for `not per_gender_age`, `not_weekly`, use them

Implicit parameter change is announced on stdout. It can be switched off by setting `verbose = False`.

Sometimes multiple datasets with slight difference (or two conversions) are available. This is announced on stdout. Choosing an alternative data is done with `alt = True`.

## Commit

With a single call all the data handlers are called and their outputs as well as common input (xlsx file) is stored. *Commit* is stored directory `commit_YYMMDD` (in *cwd*) unless explicitly specified.

```python
import covid19sweden as SWE
SWE.commit() # store all files
```

Explicit specification of directory is done with

```python
SWE.commit("/var/latest_data")
```

Function will try to create the folder. It fails on existing files of the same name. Overwriting must be enabled

```python
SWE.commit("/var/latest_data", overwrite = True)
```

## Contribution

Developed by [Martin Benes](https://github.com/martinbenes1996).

Join on [GitHub](https://github.com/martinbenes1996/covid19sweden).



