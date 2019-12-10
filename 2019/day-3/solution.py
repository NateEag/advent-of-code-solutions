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
        direction, length = move[0], int(move[1:])
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


def between(n, left, right):
    """Return True if 'n' is between 'left' and 'right', else return False."""

    return ((left <= n <= right) or (left >= n >= right))


def unsorted_range(a, b):
    """Return a list of numbers between a and b, inclusive.

    Just a wrapper around range() that sorts the input."""

    if a > b:
        return range(b, a)
    else:
        return range(a, b)


def intersection(left_list, right_list):
    result_set = set(left_list).intersection(right_list)

    return [val for val in result_set]


def find_intersections(left_segment, right_segment):
    left_seg_vertical = left_segment[0][0] == left_segment[1][0]
    left_seg_horizontal = not left_seg_vertical
    right_seg_vertical = right_segment[0][0] == right_segment[1][0]
    right_seg_horizontal = not right_seg_vertical

    if left_seg_horizontal:
        if right_seg_vertical:
            if (between(right_segment[0][0], left_segment[0][0], left_segment[1][0]) and
                between(left_segment[0][1], right_segment[0][1], right_segment[1][1])):

                return [(right_segment[0][0], left_segment[0][1])]
        elif right_seg_horizontal:
            if left_segment[0][1] == right_segment[0][1]:
                # Parallel line segments at same y-pos, so they may overlap.
                # There is an intersection at every point contained in both
                # lines.
                left_segment_x_vals = unsorted_range(left_segment[0][0],
                                                     left_segment[1][0])
                right_segment_x_vals = unsorted_range(right_segment[0][0],
                                                      right_segment[1][0])

                shared_x_vals = intersection(left_segment_x_vals, right_segment_x_vals)

                print(left_segment)
                print(right_segment)
                print(shared_x_vals)

                return [(x, left_segment[0][1]) for x in shared_x_vals]
    elif left_seg_vertical:
        if right_seg_vertical:
            # FIXME My input never actually used this branch. You could apply
            # the same logic I used for the analogous horizontal case if you
            # really wanted to.
            if (between(right_segment[0][0], left_segment[0][0], left_segment[1][0]) and
                between(left_segment[0][1], right_segment[0][1], right_segment[1][1])):
                print('Parallel overlapping lines. Implement.')
                sys.exit(1)
        elif right_seg_horizontal:
            if (between(right_segment[0][1], left_segment[0][1], left_segment[1][1]) and
                between(left_segment[0][0], right_segment[0][0], right_segment[1][0])):

                return [(left_segment[0][0], right_segment[0][1])]


def find_all_intersections(left_path, right_path):
    intersections = []

    for i in range(0, len(left_path) - 1):
        left_path_segment = (left_path[i], left_path[i + 1])
        for j in range(0, len(right_path) - 1):
            right_path_segment = (right_path[j], right_path[j + 1])

            results = find_intersections(left_path_segment,
                                         right_path_segment)

            if results is not None:
                intersections = intersections + results

    return intersections


def get_closest_distance(intersections):
    closest_distance = None

    for intersection in intersections:
        if intersection[0] == 0 and intersection[1] == 0:
            continue

        distance = abs(intersection[0]) + abs(intersection[1])

        if closest_distance is None or distance < closest_distance:
            closest_distance = distance

    return closest_distance


def main(input_path):
    # TODO Implement this
    path_one, path_two = parse_input(input_path)

    print(path_one, path_two)

    intersections = find_all_intersections(path_one, path_two)

    print(intersections)

    distance = get_closest_distance(intersections)

    if distance is None:
        print('No intersections found. Go fix your bugs. :(')
        sys.exit()

    print(distance)

if __name__ == '__main__':
    main(sys.argv[1])
