#! /usr/bin/env python

import sys
import math


def get_required_fuel_for_module(module_mass):

    return math.floor(module_mass / 3) - 2


def get_required_fuel_for_fuel(fuel_mass):

    required_fuel = get_required_fuel_for_module(fuel_mass)

    if required_fuel > 0:
        result = required_fuel + get_required_fuel_for_fuel(required_fuel)
        return result
    else:
        return 0


def get_fuel_requirements(input_path):

    total_required_fuel = 0
    for line in open(input_path, 'r'):
        required_fuel_for_module = get_required_fuel_for_module(int(line))
        required_fuel_for_fuel = get_required_fuel_for_fuel(required_fuel_for_module)

        total_required_fuel += required_fuel_for_module + required_fuel_for_fuel

    print(total_required_fuel)


if __name__ == '__main__':
   get_fuel_requirements(sys.argv[1])
