from json import dumps
import os
import sys

import get_last
import check
import decrypt
import download
import import_to_ak
import split
import set_last
import summarize
import notify

from pywell.entry_points import run_from_cli, run_from_lamba


DESCRIPTION = 'Process files.'

ARG_DEFINITIONS = {
    'AK_BASEURL': 'ActionKit Base URL.',
    'AK_USER': 'ActionKit API username.',
    'AK_PASSWORD': 'ActionKit API password.',
    'AK_IMPORT_PAGE': 'ActionKit import page name.',
    'BASE_DIRECTORY': 'Path to where files are located.',
    'CSV': 'CSV file to split.',
    'DB_HOST': 'Database host IP or hostname',
    'DB_PORT': 'Database port number',
    'DB_USER': 'Database user',
    'DB_PASS': 'Database password',
    'DB_NAME': 'Database name',
    'LAST_RUN_DATE': 'Date of last run.',
    'LAST_RUN_SCRIPT': 'Script name.',
    'PGP_KEY': 'Full key for PGP',
    'PGP_PASS': 'Pass phrase for PGP',
    'SFTP_HOST': 'Host for SFTP connection.',
    'SFTP_USER': 'User for SFTP connection.',
    'SFTP_PASS': 'Pass for SFTP connection.',
    'SLACK_WEBHOOK': 'Web hook URL for Slack.',
    'SLACK_CHANNEL': 'Slack channel to send to.',
    'SINCE': 'Override date Since to import',
}

REQUIRED_ARGS = [
    'AK_BASEURL', 'AK_USER', 'AK_PASSWORD', 'AK_IMPORT_PAGE', 'BASE_DIRECTORY',
    'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME', 'LAST_RUN_SCRIPT',
    'PGP_KEY', 'PGP_PASS', 'SFTP_HOST', 'SFTP_USER', 'SFTP_PASS'
]

def date_short_to_iso(date):
    return '20' + date[4:] + '-' + date[:2] + '-' + date[2:4]


def date_iso_to_short(date):
    parts = date.split(' ')[0].split('-')
    return parts[1] + parts[2] + parts[0][2:]


def main(args):
    all_split_files = []
    print('Checking date last run...')
    if args.SINCE:
        last_run = args.SINCE
    else:
        last_run = date_iso_to_short(get_last.main(args))
        print('Checking for new dates since %s...' % last_run)
    args.SINCE = last_run
    new_dates = check.main(args)
    if len(new_dates) > 0:
        for date in new_dates:
            date_split_files = []
            args.DATE = date
            print('Downloading for %s...' % date)
            files = download.main(args)
            if len(files) > 0:
                for encrypted_file in files:
                    args.FILE = encrypted_file
                    print('Decrypting %s...' % args.FILE)
                    decrypted_file = decrypt.main(args)
                    if decrypted_file:
                        print('Splitting %s...' % decrypted_file)
                        args.CSV = decrypted_file
                        split_files = split.main(args)
                        date_split_files = date_split_files + split_files
            if len(date_split_files):
                print('Importing for %s...' % date)
                for split_file in date_split_files:
                    args.CSV = split_file
                    print('uploading to AK', split_file)
                    import_to_ak.main(args)
                args.FILES = ','.join(date_split_files)
                args.TEXT = summarize.main(args)
                print('Notifying...')
                notify.main(args)
            all_split_files = all_split_files + date_split_files
        iso_dates = sorted([date_short_to_iso(date) for date in new_dates])
        args.LAST_RUN_DATE = iso_dates[-1]
        print('Setting last import date to %s...' % args.LAST_RUN_DATE)
        set_last.main(args)
    else:
        print('No new dates found.')
    return all_split_files


def aws_lambda(event, context):
    """
    General entry point via Amazon Lambda event.
    """
    print('running aws_lambda')
    return run_from_lamba(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS, event)


if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
