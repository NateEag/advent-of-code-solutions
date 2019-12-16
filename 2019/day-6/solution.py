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


def main(input_path):
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

            orbitee.add_child(orbiter)

    root_nodes = []
    for key, obj in objects.items():
        if obj.parent is None:
            root_nodes.append(obj)

    print('Root nodes', len(root_nodes))

    total_num_orbits = 0
    for node in root_nodes:
        total_num_orbits += node.count_orbits()

    # First time I've submitted a wrong answer. Oh well.
    #
    # Site says my number is too low. Time to go digging.
    print(total_num_orbits)


if __name__ == '__main__':
    main(sys.argv[1])
