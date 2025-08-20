import numpy
from scipy.signal import convolve2d


class Simulator:
    def __init__(self, initial):
        verificators = {
            "is_list": isinstance(initial, list),
            "is_list_of_lists": {
                isinstance(element, list)
                for element in initial
            } == {True},
            "are_same_size_lists": len(
                {
                    len(element)
                    for element in initial
                }
            ) == 1,
            "only_0_and_1_values": {
                value for line in initial for value in line
            } in [{0}, {1}, {0, 1}]
        }

        for key, value in verificators.items():
            if not value:
                raise ValueError(f"Simulator.initial verification failed : {key}")

        self.content = numpy.array(initial)
        self.water = numpy.zeros((256, 256), dtype=numpy.int8)

    def pool(self, direction):
        water = self.water
        water_size = water.shape
        content = self.content
        content_size = content.shape

        start_x = (water_size[0] - content_size[0]) // 2
        start_y = (water_size[1] - content_size[1]) // 2

        match direction:
            case "in":
                self.water[start_x:start_x + content_size[0], start_y:start_y + content_size[1]] = content

            case "out":
                self.content = self.water[start_x:start_x + content_size[0], start_y:start_y + content_size[1]]
                self.water = numpy.zeros((256, 256), dtype=numpy.int8)

            case _:
                raise ValueError("direction not supported")

    def tick(self, count=1):
        if count:
            self.pool("in")
            water = self.water

            # Kernel to count 8 neighbors
            kernel = numpy.array([[1, 1, 1],
                               [1, 0, 1],
                               [1, 1, 1]])

            # Count neighbors using convolution (zero-padded at the edges)
            neighbors = convolve2d(water, kernel, mode="same", boundary="fill", fillvalue=0)

            # Apply Game of Life rules
            born = (water == 0) & (neighbors == 3)
            survive = (water == 1) & ((neighbors == 2) | (neighbors == 3))

            # Create new water
            new_water = numpy.zeros_like(water)
            new_water[born | survive] = 1

            self.water = new_water

            self.pool("out")

            self.tick(count - 1)

    def switch(self, x, y):
        value = self.content[x][y]

        if value:
            new_value = 0

        else:
            new_value = 1

        self.content[x][y] = new_value

    def clear(self, region=None):
        pass

    def load(self):
        pass

    def save(self):
        pass

    def export(self):
        pass
