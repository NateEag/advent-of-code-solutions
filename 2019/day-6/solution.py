#! /usr/bin/env python

import sys

class TreeNode:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []


    def add_child(self, child):
        self.children.append(child)
        child.set_parent(self)


    def set_parent(self, parent):
        if self.parent is not None:
            raise Exception('Tried to set parent of ' + self.data + ', but ' +
                            'it is already ' + self.parent)

        self.parent = parent


    def get_depth(self):
        if self.parent is None:
            return 0
        else:
            return self.parent.get_depth() + 1


    def count_orbits(self):
        count = 0

        if self.parent is not None:
            # The direct orbit is worth one.
            count += 1

        # Count this node's indirect orbits
        count += max(self.get_depth() - 1, 0)

        if len(self.children) > 0:
            for child in self.children:
                count += child.count_orbits()

        return count


    def __str__(self):
        result = self.data

        for child in self.children:
            result += ' <-- ' + str(child) + '\n'

        return result


def parse_system_objects(input_path):
    objects = {}

    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            orbitee_id, orbiter_id = line.split(')')

            if orbitee_id in objects.keys():
                orbitee = objects[orbitee_id]
            else:
                orbitee = TreeNode(orbitee_id, None)
                objects[orbitee_id] = orbitee

            if orbiter_id in objects.keys():
                orbiter = objects[orbiter_id]
            else:
                orbiter = TreeNode(orbiter_id, None)
                objects[orbiter_id] = orbiter

            orbitee.add_child(orbiter)

    return objects


def find_root_node(objects):
    # Part 1 never specified clearly that everything indirectly orbits the
    # universal Center of Mass, but part 2 does (implicitly, by establishing
    # that you and Santa are always in the same tree, which means there is only
    # a single tree, not a forest), so now I can assume that.
    for key, obj in objects.items():
        if obj.parent is None:
            return obj


def count_orbits(input_path):
    system_objects = parse_system_objects(input_path)

    root_node = None
    for key, obj in system_objects.items():
        if obj.parent is None:
            root_node = obj

            break

    print(root_node.count_orbits())


if __name__ == '__main__':
    count_orbits(sys.argv[1])
