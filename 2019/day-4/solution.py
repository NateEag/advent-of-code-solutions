#! /usr/bin/env python

import re

matches = []
for password in range(136818, 685979 + 1):
    # least to most significant
    password_string = str(password)
    digits = [int(digit) for digit in password_string]

    digit_adjacency_found = False
    digit_decrease_found = False

    last_digit = -1
    for digit in digits:
        if digit < last_digit:
            digit_decrease_found = True

        if last_digit == digit:
            regex = str(digit) + '{3,}'
            # Part two additional constraint
            if re.search(regex, password_string) is None:
               digit_adjacency_found = True

        last_digit = digit

    if digit_adjacency_found and not digit_decrease_found:
        matches.append(password)

print(len(matches))
