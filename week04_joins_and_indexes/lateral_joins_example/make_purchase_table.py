"""
Make a table with the fields:

    purchase_id integer,
    cc_number text,
    purchase_dt timestamp with timezone,
    purchase_amount decimal

"""

from csv import reader as csvreader, writer as csvwriter
from datetime import datetime, timedelta
from random import Random
from sys import stdin, stdout, stderr

from libs.record_time import print_time

# Seed the random number generator with some number. Any number will do. Using
# a seed in a random number generator guarantees that the same numbers will be
# generated in the same order every time we run the script.
rnd = Random()
rnd.seed(869280)

def rand_datetime(rnd, min_datetime, max_seconds):
    purchase_seconds = rnd.randint(0, max_seconds)
    purchase_datetime = min_datetime + timedelta(seconds=purchase_seconds)
    return purchase_datetime.isoformat()

number_of_purchases = 1_000_000

print('Reading CC numbers...', file=stderr, end='')
with print_time('{duration} seconds', file=stderr):
    reader = csvreader(stdin)
    header = next(reader)
    assert header[0] == 'cc_number'
    cc_number_choices = [row[0] for row in reader]

print('Choosing credit cards...', file=stderr, end='')
with print_time('{duration} seconds', file=stderr):
    cc_numbers = [
        rnd.choice(cc_number_choices)
        for _ in range(number_of_purchases)
    ]

print('Choosing purchase datetimes...', file=stderr, end='')
with print_time('{duration} seconds', file=stderr):
    min_datetime, max_datetime = datetime(2010, 1, 1, 0, 0, 0), datetime(2021, 10, 11, 0, 0, 0)
    max_seconds = (max_datetime - min_datetime).total_seconds()
    purchase_datetimes = [
        rand_datetime(rnd, min_datetime, max_seconds)
        for _ in range(number_of_purchases)
    ]

print('Choosing purchase amounts...', file=stderr, end='')
with print_time('{duration} seconds', file=stderr):
    purchase_amounts = [
        round(rnd.expovariate(lambd=0.02), 2)
        for _ in range(number_of_purchases)
    ]

writer = csvwriter(stdout)
writer.writerow(['purchase_id', 'cc_number', 'purchase_dt', 'purchase_amount'])
writer.writerows(zip(range(1, number_of_purchases + 1), cc_numbers, purchase_datetimes, purchase_amounts))
