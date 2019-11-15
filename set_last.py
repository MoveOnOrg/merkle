import os
import sys

import psycopg2
import psycopg2.extras

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Set date of last run.'

ARG_DEFINITIONS = {
    'DB_HOST': 'Database host IP or hostname',
    'DB_PORT': 'Database port number',
    'DB_USER': 'Database user',
    'DB_PASS': 'Database password',
    'DB_NAME': 'Database name',
    'LAST_RUN_SCRIPT': 'Script name.',
    'LAST_RUN_DATE': 'Date of last run.'
}

REQUIRED_ARGS = [
    'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME', 'LAST_RUN_SCRIPT', 'LAST_RUN_DATE'
]

def main(args):
    database = psycopg2.connect(
        host=args.DB_HOST,
        port=args.DB_PORT,
        user=args.DB_USER,
        password=args.DB_PASS,
        database=args.DB_NAME
    )
    database_cursor = database.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    last_run_query = """
    UPDATE tech.script_last_run SET last_run = '%s'
    WHERE script = '%s'
    """ % (args.LAST_RUN_DATE, args.LAST_RUN_SCRIPT)
    database_cursor.execute(last_run_query)
    database.commit()
    return args.LAST_RUN_DATE

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
