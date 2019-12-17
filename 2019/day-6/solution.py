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


    def contains(self, node):
        # This approach only works if all TreeNodes in a program are
        # singletons. True here but unwise generally - use unique IDs for a
        # generic data structure.
        if node is self:
            return True

        if node in self.children:
            return True

        for child in self.children:
           if child.contains(node):
               return True

        # When there are no children we'll fall through to here.

        return False


    # REFACTOR Merge this with get_depth(), where ancestor is optional and
    # defaults to None, so by default you get depth from root.
    def depth(self, ancestor):
        depth = 0

        # As elsewhere, object identity is only correct if TreeNodes are
        # singletons. They are in this case, though.
        #
        # Also kinda crappy that I'm assuming ancestor *is* in fact an
        # ancestor. It is for my usage, but again, a general structure would
        # need to define a protocol for handling that - return -1, throw
        # exception, etc
        test_node = self
        while test_node is not ancestor:
            test_node = test_node.parent
            depth += 1

        return depth


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

def find_common_ancestor(left_node, right_node):
    left_ancestor = left_node

    while not left_ancestor.contains(right_node):
        left_ancestor = left_ancestor.parent

    return left_ancestor


def count_orbits(input_path):
    system_objects = parse_system_objects(input_path)

    root_node = None
    for key, obj in system_objects.items():
        if obj.parent is None:
            root_node = obj

            break

    print(root_node.count_orbits())


def count_orbital_transfers_to_santa(input_path):
    system_objects = parse_system_objects(input_path)

    my_node = system_objects['YOU']
    santa_node = system_objects['SAN']

    common_ancestor = find_common_ancestor(my_node, santa_node)

    transfers_to_common_ancestor = my_node.depth(common_ancestor) - 1

    transfers_to_santa = santa_node.depth(common_ancestor) - 1

    return transfers_to_common_ancestor + transfers_to_santa


if __name__ == '__main__':
    result = count_orbital_transfers_to_santa(sys.argv[1])

    print(result)
