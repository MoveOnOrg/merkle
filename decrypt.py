import os
import subprocess
import sys

import pgpy

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Decrypt PGP files with GPG.'

ARG_DEFINITIONS = {
    'BASE_DIRECTORY': 'Path to where files are located.',
    'FILE': 'File to decrypt.',
    'PGP_KEY': 'Full key for PGP',
    'PGP_PASS': 'Pass phrase for PGP'
}

REQUIRED_ARGS = [
    'BASE_DIRECTORY', 'FILE', 'PGP_KEY', 'PGP_PASS'
]

def main(args):
    message = pgpy.PGPMessage.from_file('%s%s' % (args.BASE_DIRECTORY, args.FILE))
    private_key, _ = pgpy.PGPKey.from_blob(args.PGP_KEY)

    with private_key.unlock(args.PGP_PASS):
        csv = private_key.decrypt(message).message.decode("utf-8")

    new_file_name = '.'.join(args.FILE.split('.')[:-1])
    file = open("%s%s" % (args.BASE_DIRECTORY, new_file_name), "w")
    file.write(csv)
    file.close()

    return new_file_name

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
