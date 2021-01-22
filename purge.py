#!/usr/bin/env python3
import os
import re
import sys
from argparse import ArgumentParser
import pd
import json
import dateparser
import datetime
import dateutil

parser = ArgumentParser()
parser.add_argument(
    '-t', '--token', dest='token', required=True,
    help='PagerDuty API token to use'
)
parser.add_argument(
    '-b', '--before', dest='before', required=True,
    help='Delete sessions before this time/date'
)
parser.add_argument(
    '-m', '--mobile_only', default=False, action='store_true', dest='mobile_only',
    help='Only delete mobile app sessions'
)
parser.add_argument(
    '-f', '--force', default=False, action='store_true', dest='force',
    help='Don\'t prompt to confirm, just delete the sessions (dangerous maybe?)'
)
parser.add_argument(
    '-d', '--dry-run', default=False, action='store_true', dest='dry_run',
    help='Dry run - don\'t actually delete anything'
)

args = parser.parse_args()

token = args.token

before_local = dateparser.parse(args.before).astimezone()
before_utc = datetime.datetime.utcfromtimestamp(float(before_local.strftime("%s")))
before_utc = before_utc.replace(microsecond=0)
before_utc_timestamp = f"{before_utc.isoformat()}Z"
before_local_human = before_local.strftime("%c %Z")
before_utc_human = before_utc.strftime("%c UTC")

if not args.force:
    question = f"Delete all sessions before {before_local_human} ({before_utc_human})? [y/N]: "
    do_it = str(input(question)).lower().strip() == 'y'
    if not do_it:
        print("OK, aborting.")
        sys,exit(0)

print("Getting users... ", end='', flush=True)
users = pd.fetch(token=token, endpoint='users')
print(f"got {len(users)}")

pattern = re.compile('.*')
if args.mobile_only:
    pattern = re.compile('^PagerDuty Mobile')

for user in users:
    print(f"Getting sessions for user {user['email']} ({user['id']})... ", end='', flush=True)
    sessions = pd.fetch(token=token, endpoint=f"users/{user['id']}/sessions")
    print(f"got {len(sessions)}")
    for session in sessions:
        created_at = dateparser.parse(session['created_at'])
        created_at_utc = datetime.datetime.utcfromtimestamp(float(created_at.strftime("%s")))
        if (created_at_utc < before_utc and pattern.search(session['summary'])):
            message = f"Delete session {session['id']} ({session['summary']}) created at {created_at_utc.strftime('%c UTC')}"
            if args.dry_run:
                print(f"  (dry run) {message}")
            else:
                print(f"  {message}... ", end='', flush=True)
                try:
                    pd.request(token=token, endpoint=f"users/{user['id']}/sessions/{session['type']}/{session['id']}", method="DELETE")
                except:
                    print("Failed!")
                print("done")
        else:
            print(f"  Skip session {session['id']} ({session['summary']}) created at {created_at_utc.strftime('%c UTC')}")
