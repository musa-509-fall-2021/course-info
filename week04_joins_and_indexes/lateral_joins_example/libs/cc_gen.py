#!/usr/bin/python
# -*- coding: utf-8 -*-
# by ..:: crazyjunkie ::.. 2014
# If you need a Good Wordlist ====> http://uploaded.net/folder/j7gmyz

"""
gencc: A simple program to generate credit card numbers that pass the
MOD 10 check (Luhn formula).
Usefull for testing e-commerce sites during development.

From https://github.com/eye9poob/python/blob/master/credit-card-numbers-generator.py

by ..:: crazyjunkie ::.. 2014
"""

from random import Random
import copy

visa_prefix_list = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']]

mastercard_prefix_list = [
        ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]

amex_prefix_list = [['3', '4'], ['3', '7']]

discover_prefix_list = [['6', '0', '1', '1']]

diners_prefix_list = [
        ['3', '0', '0'],
        ['3', '0', '1'],
        ['3', '0', '2'],
        ['3', '0', '3'],
        ['3', '6'],
        ['3', '8']]

enRoute_prefix_list = [['2', '0', '1', '4'], ['2', '1', '4', '9']]

jcb_prefix_list = [['3', '5']]

voyager_prefix_list = [['8', '6', '9', '9']]


def completed_number(rnd, prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
        digit = str(rnd.choice(range(0, 10)))
        ccnumber.append(digit)

    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = ccnumber[::-1]

    while pos < length - 1:

        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):

            sum += int(reversedCCnumber[pos + 1])

        pos += 2

    # Calculate check digit

    checkdigit = ((sum // 10 + 1) * 10 - sum) % 10

    ccnumber.append(str(checkdigit))

    return ''.join(ccnumber)


def credit_card_number(rnd, prefixList, length, disallowed=None, update_disallowed_set=False):

    if disallowed is None and update_disallowed_set:
        raise ValueError('Cannot update disallowed set None')

    while True:
        ccnumber = copy.copy(rnd.choice(prefixList))
        complete_ccnumber = completed_number(rnd, ccnumber, length)

        if disallowed is None or complete_ccnumber not in disallowed:
            break

    if update_disallowed_set:
        disallowed.add(complete_ccnumber)

    return complete_ccnumber

def output(title, numbers):

    result = []
    result.append(title)
    result.append('-' * len(title))
    result.append('\n'.join(numbers))
    result.append('')

    return '\n'.join(result)


#
# Main
#
if __name__ == '__main__':
    generator = Random()
    generator.seed()        # Seed from current time

    print("credit card generator by ..:: crazyjunkie ::..\n")

    mastercard = [credit_card_number(generator, mastercard_prefix_list, 16) for _ in range(10)]
    print(output("Mastercard", mastercard))

    visa16 = [credit_card_number(generator, visa_prefix_list, 16) for _ in range(10)]
    print(output("VISA 16 digit", visa16))

    visa13 = [credit_card_number(generator, visa_prefix_list, 13) for _ in range(5)]
    print(output("VISA 13 digit", visa13))

    amex = [credit_card_number(generator, amex_prefix_list, 15) for _ in range(5)]
    print(output("American Express", amex))

    # Minor cards

    discover = [credit_card_number(generator, discover_prefix_list, 16) for _ in range(3)]
    print(output("Discover", discover))

    diners = [credit_card_number(generator, diners_prefix_list, 14) for _ in range(3)]
    print(output("Diners Club / Carte Blanche", diners))

    enRoute = [credit_card_number(generator, enRoute_prefix_list, 15) for _ in range(3)]
    print(output("enRoute", enRoute))

    jcb = [credit_card_number(generator, jcb_prefix_list, 16) for _ in range(3)]
    print(output("JCB", jcb))

    voyager = [credit_card_number(generator, voyager_prefix_list, 15) for _ in range(3)]
    print(output("Voyager", voyager))
