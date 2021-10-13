"""
Make a table with the fields:

    cc_number text primary key,
    cc_type text,
    cc_exp_date date

"""

from csv import writer as csvwriter
from datetime import date, timedelta
from random import Random
from sys import stdout, stderr

from libs.cc_gen import (
    credit_card_number,
    mastercard_prefix_list,
    visa_prefix_list,
    amex_prefix_list
)
from libs.record_time import print_time

# Seed the random number generator with some number. Any number will do. Using
# a seed in a random number generator guarantees that the same numbers will be
# generated in the same order every time we run the script.
rnd = Random()
rnd.seed(869280)

cc_type_map = {
    'mastercard': (mastercard_prefix_list, 16),
    'visa': (visa_prefix_list, 16),
    'amex': (amex_prefix_list, 15),
}

cc_type_choices = tuple(cc_type_map.keys())

number_of_ccs = 100_000

print('Generating CC types...', file=stderr, end='')
with print_time('{duration} seconds', file=stderr):
    cc_types = [
        rnd.choice(cc_type_choices)
        for _ in range(number_of_ccs)
    ]

# Choose a bunch of random credit card numbers and exp dates.
print('Generating CC numbers...', file=stderr, end='')
with print_time('{duration} seconds', file=stderr):
    pre_existing_numbers = set()
    cc_numbers = [
        credit_card_number(
            rnd,
            cc_type_map[cc_type][0],
            cc_type_map[cc_type][1],
            disallowed=pre_existing_numbers,
            update_disallowed_set=True,
        )
        for cc_type in cc_types
    ]

def rand_date(rnd, min_date, max_days):
    exp_days = rnd.randint(0, max_days)
    exp_date = min_date + timedelta(days=exp_days)
    return exp_date.isoformat()

print('Generating CC exp dates...', file=stderr, end='')
with print_time('{duration} seconds', file=stderr):
    min_date, max_date = date(2022, 6, 1), date(2025, 12, 29)
    date_range = max_date - min_date
    max_days = date_range.days
    cc_exp_dates = [
        rand_date(rnd, min_date, max_days)
        for cc_type in cc_types
    ]

print('Outputting CC data...', file=stderr, end='')
with print_time('{duration} seconds', file=stderr):
    writer = csvwriter(stdout)
    writer.writerow(['cc_number', 'cc_type', 'cc_exp_date'])
    writer.writerows(zip(cc_numbers, cc_types, cc_exp_dates))
