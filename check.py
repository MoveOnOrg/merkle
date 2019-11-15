import os
import sys

import paramiko

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Check for new files.'

ARG_DEFINITIONS = {
    'SINCE': 'Date of files to find after.',
    'SFTP_HOST': 'Host for SFTP connection.',
    'SFTP_USER': 'User for SFTP connection.',
    'SFTP_PASS': 'Pass for SFTP connection.',
}

REQUIRED_ARGS = [
    'SINCE', 'SFTP_HOST', 'SFTP_USER', 'SFTP_PASS'
]

def sortable_date(date):
    return date[4:] + date[0:2] + date[2:4]

def main(args):
    since = sortable_date(args.SINCE)
    transport = paramiko.Transport((args.SFTP_HOST, 22))
    transport.connect(username = args.SFTP_USER, password = args.SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.chdir('Outgoing Files')
    file_list = sftp.listdir('.')
    new_dates = []
    for file_name in file_list:
        date = ''.join([char for char in file_name if char.isdigit()])
        if sortable_date(date) > since:
            new_dates.append(date)
    return list(set(new_dates))


if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
