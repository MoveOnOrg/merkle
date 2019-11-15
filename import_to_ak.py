import os
import sys

from actionkit.api.user import AKUserAPI

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Import file.'

ARG_DEFINITIONS = {
    'BASE_DIRECTORY': 'Path to where files are located.',
    'CSV': 'CSV file to import.',
    'AK_BASEURL': 'ActionKit Base URL.',
    'AK_USER': 'ActionKit API username.',
    'AK_PASSWORD': 'ActionKit API password.',
    'AK_IMPORT_PAGE': 'ActionKit import page name.'
}

REQUIRED_ARGS = [
    'BASE_DIRECTORY', 'CSV', 'AK_BASEURL', 'AK_USER', 'AK_PASSWORD', 'AK_IMPORT_PAGE'
]

def main(args):
    api = AKUserAPI(args)
    result = api.bulk_upload(args.AK_IMPORT_PAGE, open('%s%s' % (args.BASE_DIRECTORY, args.CSV), 'rb'), 1)
    return result

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
