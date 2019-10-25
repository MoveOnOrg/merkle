import os
import subprocess
import sys

import pgpy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
    import settings
else:
    settings = {}

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
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
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
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description=('Decrypt PGP files with GPG.')
    )

    for argname, helptext in ARG_DEFINITIONS.items():
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pprint.PrettyPrinter(indent=2).pprint(main(args))
