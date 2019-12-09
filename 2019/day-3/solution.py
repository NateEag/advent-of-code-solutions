#! /usr/bin/env python

# How am I going to find the points where paths intersect?
#
# Might as well go naive, because runtime doesn't matter for inputs this small.
#
# Parse the 'movements' into two lists of segments starting at (0, 0), then
# loop across both lists, checking whether any segment in one intersects with
# any of the others.

import sys

def parse_path(input_line):
    moves = input_line.split(',')

    points = [(0, 0)]
    for move in moves:
        direction, length = move[0], int(move[1])
        if direction == 'U':
            points.append((points[-1][0], points[-1][1] + length))
        elif direction == 'D':
            points.append((points[-1][0], points[-1][1] - length))
        elif direction == 'R':
            points.append((points[-1][0] + length, points[-1][1]))
        elif direction == 'L':
            points.append((points[-1][0] - length, points[-1][1]))
        else:
            print('ERROR PARSING PATH: unknown direction ' + direction)

            sys.exit(1)

    return points

def parse_input(input_path):
    paths = []

    with open(input_path, 'r') as f:
        for line in f:
            paths.append(parse_path(line))

    return paths


def main(input_path):
    # TODO Implement this
    path_one, path_two = parse_input(input_path)

    print(path_one, path_two); sys.exit()

    intersection = find_intersection(path_one, path_two)

    distance = compute_distance(intersection)

    print(distance)

if __name__ == '__main__':
    main(sys.argv[1])
