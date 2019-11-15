import csv
import os
import sys

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Get summary of donations.'

ARG_DEFINITIONS = {
    'BASE_DIRECTORY': 'Path to where files are located.',
    'FILES': 'A comma-separated list of CSV file names in BASE_DIRECTORY.'
}

REQUIRED_ARGS = ['BASE_DIRECTORY', 'FILES']


def main(args):
    donations = []
    for filename in args.FILES.split(','):
        with open('%s%s' % (args.BASE_DIRECTORY, filename), 'rt') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                date = row.get('donation_date')
                donations.append(float(row.get('donation_amount', 0)))
    return 'New import for %s: *%s* donations totalling *$%s*.' % (date, len(donations), "{0:.2f}".format(sum(donations)))

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
