#! /usr/bin/env python

import sys
import math


def get_required_fuel_for_module(module_mass):

    return math.floor(module_mass / 3) - 2

def get_fuel_requirements(input_path):

    total_required_fuel = 0
    for line in open(input_path, 'r'):
        total_required_fuel += get_required_fuel_for_module(int(line))

    print(total_required_fuel)

if __name__ == '__main__':
   get_fuel_requirements(sys.argv[1])
