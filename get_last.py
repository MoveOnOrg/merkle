import os
import sys

import psycopg2
import psycopg2.extras

from pywell.entry_points import run_from_cli


DESCRIPTION = 'Get date of last run.'

ARG_DEFINITIONS = {
    'DB_HOST': 'Database host IP or hostname',
    'DB_PORT': 'Database port number',
    'DB_USER': 'Database user',
    'DB_PASS': 'Database password',
    'DB_NAME': 'Database name',
    'LAST_RUN_SCRIPT': 'Script name.'
}

REQUIRED_ARGS = [
    'DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME', 'LAST_RUN_SCRIPT'
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
    SELECT last_run
    FROM tech.script_last_run
    WHERE script = '%s'
    """ % args.LAST_RUN_SCRIPT
    database_cursor.execute(last_run_query)
    last_run_result = list(database_cursor.fetchall())
    return str(last_run_result[0].get('last_run'))

if __name__ == '__main__':
    run_from_cli(main, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)
