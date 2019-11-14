import csv
import os
import sys

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Get summary of donations.'

ARG_DEFINITIONS = {
    'BASE_DIRECTORY': 'Path to where files are located.',
    'CSV': 'CSV of donation records.'
}

REQUIRED_ARGS = ['BASE_DIRECTORY', 'CSV']

def main(args):
    donations = []
    with open('%s%s' % (args.BASE_DIRECTORY, args.CSV), 'rt') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            date = row.get('donation_date')
            donations.append(float(row.get('donation_amount', 0)))
    return 'New import for %s: *%s* donations totalling *$%s*.' % (date, len(donations), "{0:.2f}".format(sum(donations)))

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
