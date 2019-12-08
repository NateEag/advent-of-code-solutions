#! /usr/bin/env python

import sys
import os

# A few module-level variables, because closures are an easy way to share
# state.
#
# Would be more modular to pass this to each of them. Oh well.
program = None
debug = False
instruction_index = 0

def get_param_value(param):
    # I imagine there will eventually be modes beyond 'position' and
    # 'immediate', but until there are this should be enough.
    return program[param['value']] if param['mode'] is 0 else param['value']


# TODO Abstract the operation of running an instruction? The ones that use two
# values look awful similar, and then they could share debugging info.

def add_instruction(left_param, right_param, output_param):
    left_value = get_param_value(left_param)
    right_value = get_param_value(right_param)

    program[output_param['value']] = left_value + right_value

    if debug:
        print('Left value',
              left_value,
              'right value',
              right_value,
              'result',
              program[output_param['value']])


def multiply_instruction(left_param, right_param, output_param):
    left_value = get_param_value(left_param)
    right_value = get_param_value(right_param)

    program[output_param['value']] = left_value * right_value

    if debug:
        print(program[output_param['value']])


def store_instruction(param):
    value = input('>')

    program[param['value']] = int(value)


def output_instruction(param):
    value = get_param_value(param)

    print('Output', value)


def jump_if_true_instruction(test_param, jump_param):
    test_value = get_param_value(test_param)
    address = get_param_value(jump_param)

    if test_value != 0:
        global instruction_index
        instruction_index = address


def jump_if_false_instruction(test_param, jump_param):
    test_value = get_param_value(test_param)
    address = get_param_value(jump_param)

    if test_value == 0:
        global instruction_index
        instruction_index = address


def less_than_instruction(left_param, right_param, output_param):
    left_value = get_param_value(left_param)
    right_value = get_param_value(right_param)

    output_address = output_param['value']

    if left_value < right_value:
        program[output_address] = 1
    else:
        program[output_address] = 0


def equals_instruction(left_param, right_param, output_param):
    left_value = get_param_value(left_param)
    right_value = get_param_value(right_param)

    output_address = output_param['value']

    if left_value == right_value:
        program[output_address] = 1
    else:
        program[output_address] = 0


def noop_instruction():
    pass


# TODO Infer num_params from the actual functions. DRYer. This should work for
# now, though.
opcodes = {
    1: {
        'function': add_instruction,
        'num_params': 3
    },
    2: {
        'function': multiply_instruction,
        'num_params': 3
    },
    3: {
        'function': store_instruction,
        'num_params': 1
    },
    4: {
        'function': output_instruction,
        'num_params': 1
    },
    5: {
        'function': jump_if_true_instruction,
        'num_params': 2
    },
    6: {
        'function': jump_if_false_instruction,
        'num_params': 2
    },
    7: {
        'function': less_than_instruction,
        'num_params': 3
    },
    8: {
        'function': equals_instruction,
        'num_params': 3
    },
    99: {
        'function': noop_instruction,
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
    global instruction_index

    while halted != True:
        cur_instruction_address = instruction_index
        opcode_string = str(program[instruction_index])
        opcode_string = opcode_string.zfill(5)

        opcode = int(opcode_string[-2:])
        modes = [int(char) for char in opcode_string[:-2]]
        # Since modes are read right to left, we flip their order. That makes
        # assigning them in the params array simpler.
        modes.reverse()

        if opcode == 99:
            halted = True
            # TODO Output the name of previous instruction? For day 5 it would
            # help understand what's going wrong.
            print('Halt instruction reached')
            break

        if debug:
            print('Instruction #:',
                  instruction_index,
                  'Instruction',
                  program[instruction_index],
                  'opcode',
                  opcode_string,
                  'modes',
                  modes)

        num_params = opcodes[opcode]['num_params']

        params = program[instruction_index + 1 : instruction_index + 1 + num_params]

        if debug:
            print('Params: ' + str(num_params) + ', ' + str(params))

        params = [{ 'mode': modes[i], 'value': param }
                  for i, param in enumerate(params)]

        operator_function = opcodes[opcode]['function']
        operator_function(*params)

        if cur_instruction_address == instruction_index:
            # No jump has been performed, so increment instruction pointer
            instruction_index += num_params + 1


if __name__ == '__main__':
    if 'DEBUG' in os.environ.keys():
        debug = True

    run_intcode_program(sys.argv[1], debug)
