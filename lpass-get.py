#!/bin/python

import re
import subprocess
import sys
import argparse
from collections import namedtuple

# CLI Parser

parser = argparse.ArgumentParser('Query passwords from LastPass easily (Provide at least one query criteria)')
parser.add_argument('app_name', help='Name of website or application or part thereof, example, spotify. (optional)')
parser.add_argument('user_name', nargs='?', help='User name or part thereof, example, alfred. (optional)')
parser.add_argument('-p', '--print-password', action='store_true', help='Print password (default is copy to the X11 clipboard)')
args = parser.parse_args()


# Query all accounts

subprocess.call(['lpass', 'sync'])  # Synchronizing database
process = subprocess.Popen(['lpass', 'ls', '-l'], stdout=subprocess.PIPE)  # Listing data of all accounts
out, err = process.communicate()
if err:
    print('Error: {}'.format(err))
    sys.exit(1)
lpass_data = out.decode('UTF-8').strip().split('\n')


# Extract App and User name

LpassEntry = namedtuple('LpassEntry', ('id', 'app_name', 'user_name'))
entries = []
for entry in lpass_data:
    matched = re.match(r'[0-9-]* [0-9:]* (.*) \[id: ([0-9]*)\] \[username: (.*)\]', entry)
    if matched is not None:
        entries.append(LpassEntry(id=matched.group(2), app_name=matched.group(1).split('/')[-1], user_name=matched.group(3)))


# Filter entries

matches = list(filter(lambda e: args.app_name in e.app_name, entries))

if args.user_name is not None:
    matches = list(filter(lambda e: args.user_name in e.user_name, matches))
elif len(matches) == 0:
    matches = list(filter(lambda e: args.app_name in e.user_name, entries))


# Results

if len(matches) == 0:
    print("No Matches")
    sys.exit(1)

if len(matches) > 1:
    print('Multiple Matches')
    print('Application\t\t\tUsername')
    for entry in matches:
        print("{}\t\t{}".format(entry.app_name, entry.user_name))
    sys.exit(1)

match = matches[0]
print('Match found: <{}> <{}>'.format(match.app_name, match.user_name))


# Execute command

command = ['lpass', 'show', '--password']
if not args.print_password:
    command.append('--clip')
command.append(match.id)

process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()
if process.returncode == 0:
    if args.print_password:
        print('Password:', process.stdout.read().decode().strip())
    else:
        print('Password copied to clipboard')
    sys.exit(0)
else:
    print('Failed to fetch password. Error: {}'.format(process.stderr.read().decode().strip()))
    sys.exit(process.returncode)
