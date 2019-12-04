#! /usr/bin/env python

import sys
import os

# Make the input program a global so the operator functions have access to it
# via closure.
#
# Would be more modular to pass this to each of them. Oh well.
program = None

debug = False


def add_operator(left_address, right_address, output_address):
    program[output_address] = program[left_address] + program[right_address]


def multiply_operator(left_address, right_address, output_address):
    program[output_address] = program[left_address] * program[right_address]


def noop_operator(left_address, right_address, output_address):
    pass


opcodes = {
    1: {
        'function': add_operator
    },
    2: {
        'function': multiply_operator
    },
    99: {
        'function': noop_operator
    }
}

def run_intcode_program(input_path, word, verb, debug=False):
    program_file = open(input_path, 'r')

    # TODO Turn this into a 2D list, to make it easier to step between inputs?
    # Might make debugging easier too.
    global program
    program = [int(x) for x in program_file.read().split(',')]

    program[1] = word
    program[2] = verb

    halted = False
    instruction_index = 0

    while halted != True:
        opcode = program[instruction_index]

        if opcode == 99:
            halted = True
            break

        operator_function = opcodes[opcode]['function']
        operator_function(
            program[instruction_index + 1],
            program[instruction_index + 2],
            program[instruction_index + 3]
        )

        instruction_index += 4

    if debug:
        print(program)


if __name__ == '__main__':
    if 'DEBUG' in os.environ.keys():
        debug = True

    result = None
    for i in range(0, 100):
        for j in range(0, 100):
            run_intcode_program(sys.argv[1], i, j, debug)

            if program[0] == 19690720:
                print('Noun: %i, Verb: %i' % (i, j))

