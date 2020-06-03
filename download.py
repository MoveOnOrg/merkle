import os
import sys

import paramiko

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Download files.'

ARG_DEFINITIONS = {
    'BASE_DIRECTORY': 'Path to where files are located.',
    'DATE': 'Date of files to download.',
    'SFTP_HOST': 'Host for SFTP connection.',
    'SFTP_USER': 'User for SFTP connection.',
    'SFTP_PASS': 'Pass for SFTP connection.',
}

REQUIRED_ARGS = [
    'BASE_DIRECTORY', 'DATE', 'SFTP_HOST', 'SFTP_USER', 'SFTP_PASS'
]

def main(args):
    transport = paramiko.Transport((args.SFTP_HOST, 22))
    transport.connect(username = args.SFTP_USER, password = args.SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.chdir('Outgoing Files')
    file_list = sftp.listdir('.')
    downloaded = []
    for file_name in file_list:
        if args.DATE in file_name and 'csv' in file_name:
            sftp.get(file_name, '%s%s' % (args.BASE_DIRECTORY, file_name))
            downloaded.append(file_name)
    print('newly downloaded', downloaded)
    return downloaded

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
