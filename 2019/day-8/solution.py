#! /usr/bin/env python

import sys
import copy
import itertools

flatten = itertools.chain.from_iterable


class SIF:
    def __init__(self, data, width, height):
        self.width = width
        self.height = height

        if len(data) % (width * height) != 0:
            raise Exception(
                'SIF image data must be exactly a multiple of its dimensions!'
            )

        num_layers = len(data) // (width * height)

        self.layers = []
        for i in range(0, num_layers):
            layer = []
            for j in range(0, height):
                row = []

                for k in range(0, width):
                    layer_offset = i * height * width
                    row_offset = width * j

                    index = layer_offset + row_offset + k

                    row.append(int(data[index]))

                layer.append(row)

            self.layers.append(layer)


    def __str__(self):
        result = ''

        for i, layer in enumerate(self.layers):
            result += f'Layer {i}\n'
            for row in layer:
                result += str(row) + '\n'

        return result


    @staticmethod
    def parse_file(input_path, width, height):
        with open(input_path) as f:
           data = f.read()

           return SIF(data, width, height)


    def get_composite_image(self):
        # Yay painter's algorithm
        num_layers = len(self.layers)

        # Start by copying the bottom-most layer then running painter's
        # algorithm with all higher layers.
        composite_image = self.layers[num_layers - 1]

        for i in range(len(self.layers) - 2, -1, -1):
            layer = self.layers[i]

            for i, row in enumerate(layer):
                for j, pixel in enumerate(row):
                    if pixel == 2:
                        continue

                    composite_image[i][j] = pixel

        return composite_image


    def get_num_pixels_with_value_in_layer(self, value, layer_num):
        num_values = 0

        layer = self.layers[layer_num]

        for row in layer:
            for pixel in row:
                if pixel == value:
                    num_values += 1

        return num_values


    def get_layer_num_with_fewest_zeroes(self):
        result_layer_num = None

        min_zero_count = None

        for i in range(0, len(self.layers)):
            num_pixels = self.get_num_pixels_with_value_in_layer(0, i)

            if min_zero_count is None:
                min_zero_count = num_pixels
                result_layer_num = i
            elif num_pixels < min_zero_count:
                min_zero_count = num_pixels
                result_layer_num = i

        return result_layer_num


def get_part_1_result(input_path, width, height):
    image = SIF.parse_file(input_path, width, height)

    i = image.get_layer_num_with_fewest_zeroes()

    num_one_pixels = image.get_num_pixels_with_value_in_layer(1, i)
    num_two_pixels = image.get_num_pixels_with_value_in_layer(2, i)

    print(num_one_pixels, num_two_pixels)

    return num_one_pixels * num_two_pixels


def get_part_2_result(input_path, width, height):
    image = SIF.parse_file(input_path, width, height)

    composite = image.get_composite_image()

    for row in composite:
        output = ''.join([str(x) for x in row])
        output = output.replace('0', ' ')

        print(output)

    output_list = [str(x) for x in list(flatten(composite))]
    output_data = ''.join(output_list)

    sys.exit()

    return output_data


if __name__ == '__main__':
    # My input image is 25 x 6.
    result = get_part_2_result(sys.argv[1],
                               int(sys.argv[2]),
                               int(sys.argv[3]))

    print(result)
