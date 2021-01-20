# PDsessionpurge

Purge PD user sessions that were created before a date/time

## Installation:

* Clone this repo and `cd` to it
* Create a virtual environment with Python 3: `python3 -m venv venv`
* Activate the virtual environment: `. venv/bin/activate`
* Get the dependencies: `pip install -r requirements.txt`

## Usage:

```
purge.py [-h] -t TOKEN -b BEFORE [-f] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        PagerDuty API token to use
  -b BEFORE, --before BEFORE
                        Delete sessions before this time/date
  -f, --force           Don't prompt to confirm, just delete the sessions (dangerous maybe?)
  -d, --dry-run         Dry run - don't actually delete anything
```

`-b` flag will accept most human-readable date/time formats, like '1/1/2020 3pm EST' and '2 years ago'

## Examples

```
# Dry run: Delete all sessions older than 1 year:
./purge.py -t MY_API_TOKEN -b '1 year ago' -d

# OK now do it for real:
./purge.py -t MY_API_TOKEN -b '1 year ago'

# OK now do it without prompting me
./purge.py -t MY_API_TOKEN -b '1 year ago' -f
```
