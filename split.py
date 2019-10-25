import csv
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(BASE_DIR, 'settings.py')):
    import settings
else:
    settings = {}

ARG_DEFINITIONS = {
    'BASE_DIRECTORY': 'Path to where files are located.',
    'CSV': 'CSV file to split.'
}

REQUIRED_ARGS = ['BASE_DIRECTORY', 'CSV']

def main(args):
    all_required_args_set = True

    for arg in REQUIRED_ARGS:
        if not getattr(args, arg, False):
            print('%s (%s) required, missing.' % (ARG_DEFINITIONS.get(arg), arg))
            all_required_args_set = False

    if all_required_args_set:
        prefix = args.CSV[:-4]
        set_only_columns = [
            'user_do_not_mail', 'user_sms_subscribed', 'home_phone',
            'mobile_phone', 'first_name', 'last_name', 'prefix'
        ]
        address_columns = [
            'address1', 'address2', 'city', 'state', 'zip'
        ]
        files = {
            'donations-user': [],
            'donations-email': [],
            'invalid-user': [],
            'invalid-email': [],
            'address-user': [],
            'address-email': []
        }
        for column in set_only_columns:
            files['%s-user' % column] = []
            files['%s-email' % column] = []

        with open('%s%s' % (args.BASE_DIRECTORY, args.CSV), 'rt') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                user_id = row.get('user_id')
                donation_payment_account = row.get('donation_payment_account')
                source = row.get('source')
                email = row.get('Email')
                if float(row.get('donation_amount', 0)) > 0:
                    if user_id != '':
                        files['donations-user'].append({
                            'user_id': user_id, 'source': source,
                            'donation_amount': row.get('donation_amount'),
                            'donation_import_id': row.get('donation_import_id'),
                            'donation_date': row.get('donation_date'),
                            'donation_currency': row.get('donation_currency'),
                            'donation_payment_account': donation_payment_account,
                            'action_occupation': row.get('action_occupation'),
                            'action_employer': row.get('action_employer'),
                        })
                    elif email != '':
                        files['donations-email'].append({
                            'email': email, 'source': source,
                            'donation_amount': row.get('donation_amount'),
                            'donation_import_id': row.get('donation_import_id'),
                            'donation_date': row.get('donation_date'),
                            'donation_currency': row.get('donation_currency'),
                            'donation_payment_account': donation_payment_account,
                            'action_occupation': row.get('action_occupation'),
                            'action_employer': row.get('action_employer'),
                        })
                for column in set_only_columns:
                    row_column = row.get(column, '')
                    if row_column != '':
                        if user_id != '':
                            files['%s-user' % column].append({
                                'user_id': user_id, 'source': source,
                                column: row.get(column),
                            })
                        elif email != '':
                            files['%s-email' % column].append({
                                'email': email, 'source': source,
                                column: row.get(column),
                            })

                if row.get('address1', False) == 'Invalid':
                    if user_id != '':
                        files['invalid-user'].append({
                            'user_id': user_id, 'source': source,
                            'address1': '-', 'address2': '-', 'city': '-',
                            'state': '-', 'zip': '-'
                        })
                    elif email != '':
                        files['invalid-email'].append({
                            'email': email, 'source': source,
                            'address1': '-', 'address2': '-', 'city': '-',
                            'state': '-', 'zip': '-'
                        })
                elif row.get('address1', False):
                    if user_id != '':
                        files['address-user'].append({
                            'user_id': user_id, 'source': source,
                            'address1': row.get('address1', ''),
                            'address2': row.get('address2', ''),
                            'city': row.get('city', ''),
                            'state': row.get('state', ''),
                            'zip': row.get('zip', '')
                        })
                    elif email != '':
                        files['address-email'].append({
                            'email': email, 'source': source,
                            'address1': row.get('address1', ''),
                            'address2': row.get('address2', ''),
                            'city': row.get('city', ''),
                            'state': row.get('state', ''),
                            'zip': row.get('zip', '')
                        })

        filenames = []

        for file in files:
            if len(files[file]) > 0:
                filename = prefix + '-' + file + '.csv'
                filenames.append(filename)
                with open('%s%s' % (args.BASE_DIRECTORY, filename), 'w') as csvfile:
                    fieldnames = list(files[file][0].keys())
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in files[file]:
                        writer.writerow(row)

        return filenames

if __name__ == '__main__':
    """
    Entry point via command line.
    """
    import argparse
    import pprint

    parser = argparse.ArgumentParser(
        description=('Split a donation import into separate files '
                     'to avoid erasing data with empty columns.')
    )

    for argname, helptext in ARG_DEFINITIONS.items():
        parser.add_argument(
            '--%s' % argname, dest=argname, help=helptext,
            default=getattr(settings, argname, False)
        )

    args = parser.parse_args()
    pprint.PrettyPrinter(indent=2).pprint(main(args))
