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
    'DATE': 'Date of files to decrypt.',
    'PGP_KEY': 'Full key for PGP',
    'PGP_PASS': 'Pass phrase for PGP'
}

REQUIRED_ARGS = [
    'DATE', 'PGP_KEY', 'PGP_PASS'
]

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
        rt_message = pgpy.PGPMessage.from_file('/tmp/MOVEONRT%s.csv.pgp' % args.DATE)
        dm_message = pgpy.PGPMessage.from_file('/tmp/MOVEONDM%s.csv.pgp' % args.DATE)
        private_key, _ = pgpy.PGPKey.from_blob(args.PGP_KEY)

        with private_key.unlock(args.PGP_PASS):
            rt_csv = private_key.decrypt(rt_message).message.decode("utf-8")
            dm_csv = private_key.decrypt(dm_message).message.decode("utf-8")

        rt_file = open("/tmp/MOVEONRT%s.csv" % args.DATE, "w")
        rt_file.write(rt_csv)
        rt_file.close()
        dm_file = open("/tmp/MOVEONDM%s.csv" % args.DATE, "w")
        dm_file.write(dm_csv)
        dm_file.close()

        return ['MOVEONDM%s.csv' % args.DATE, 'MOVEONRT%s.csv' % args.DATE]

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
