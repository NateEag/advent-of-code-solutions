#! /usr/bin/env python

import sys
import os

# Make the input program a global so the operator functions have access to it
# via closure.
#
# Would be more modular to pass this to each of them. Oh well.
program = None

debug = False


# FIXME I now have to update all these to take in
def add_operator(left_param, right_param, output_param):
    left_value = program[left_param['value']] if left_param['mode'] is 0 else left_param['value']
    right_value = program[right_param['value']] if right_param['mode'] is 0 else left_param['value']

    program[output_param['value']] = left_value + right_value


def multiply_operator(left_param, right_param, output_param):
    left_value = program[left_param['value']] if left_param['mode'] is 0 else left_param['value']
    right_value = program[right_param['value']] if right_param['mode'] is 0 else left_param['value']

    program[output_param['value']] = left_value * right_value


def store_operator(param):
    value = input('>')

    program[param['value']] = int(value)


def output_operator(param):
    address = program[param['value']] if param['mode'] is 0 else param['value']

    print(program[address])


def noop_operator():
    pass


# TODO Infer num_params from the actual functions. DRYer. This should work for
# now, though.
opcodes = {
    1: {
        'function': add_operator,
        'num_params': 3
    },
    2: {
        'function': multiply_operator,
        'num_params': 3
    },
    3: {
        'function': store_operator,
        'num_params': 1
    },
    4: {
        'function': output_operator,
        'num_params': 1
    },
    99: {
        'function': noop_operator,
        'num_params': 0
    }
}

def run_intcode_program(input_path, debug=False):
    program_file = open(input_path, 'r')

    # TODO Turn this into a 2D list, to make it easier to step between inputs?
    # Might make debugging easier too.
    global program
    program = [int(x) for x in program_file.read().split(',')]

    halted = False
    instruction_index = 0

    while halted != True:
        opcode_string = str(program[instruction_index])
        opcode_string = opcode_string.zfill(5)

        opcode = int(opcode_string[-2:])
        modes = [int(char) for char in opcode_string[:-2]]
        # Since modes are read right to left, we flip their order. That makes
        # assigning them in the params array simpler.
        modes.reverse()

        if opcode == 99:
            halted = True
            break

        num_params = opcodes[opcode]['num_params']

        params = program[instruction_index + 1 : instruction_index + 1 + num_params]

        if debug:
            print('Params: ' + str(num_params) + ', ' + str(params))

        params = [{ 'mode': modes[i], 'value': param }
                  for i, param in enumerate(params)]

        operator_function = opcodes[opcode]['function']
        operator_function(*params)

        instruction_index += num_params
        if debug:
            print(instruction_index)


if __name__ == '__main__':
    if 'DEBUG' in os.environ.keys():
        debug = True

    run_intcode_program(sys.argv[1], debug)
