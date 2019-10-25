import csv
import pytest

from split import main

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Test:

    def test_split(self):
        # Write a sample CSV file
        with open('/tmp/merkletest.csv', 'w') as csvfile:
            fieldnames = ['user_id', 'first_name', 'last_name', 'address1', 'donation_amount', 'home_phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'user_id': '44',
                'first_name': 'Barack',
                'last_name': 'Obama',
                'address1': 'Invalid',
                'donation_amount': 100,
                'home_phone': ''
            })
            writer.writerow({
                'user_id': '46',
                'first_name': 'Elizabeth',
                'last_name': 'Warren',
                'address1': '1600 Pennsylvania Ave',
                'donation_amount': 0,
                'home_phone': ''
            })
        args = {
            'BASE_DIRECTORY': '/tmp/',
            'CSV': 'merkletest.csv'
        }
        args = Struct(**args)
        # Run split on sample CSV file
        files = main(args)
        # Make sure correct files were created
        correct_files = [
            'merkletest-address-user.csv',
            'merkletest-donations-user.csv',
            'merkletest-first_name-user.csv',
            'merkletest-invalid-user.csv',
            'merkletest-last_name-user.csv'
        ]
        assert set(files) == set(correct_files)
        # Make sure file contents are correct
        with open('/tmp/merkletest-invalid-user.csv', 'rt') as csvfile:
            csvreader = csv.DictReader(csvfile)
            rows = list(csvreader)
            assert len(rows) == 1
            assert rows[0].get('address1', '') == '-'
        with open('/tmp/merkletest-donations-user.csv', 'rt') as csvfile:
            csvreader = csv.DictReader(csvfile)
            rows = list(csvreader)
            assert len(rows) == 1
            assert rows[0].get('donation_amount', '') == '100'
        with open('/tmp/merkletest-first_name-user.csv', 'rt') as csvfile:
            csvreader = csv.DictReader(csvfile)
            rows = list(csvreader)
            assert len(rows) == 2
