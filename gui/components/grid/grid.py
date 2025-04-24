import math
import uuid
from functools import partial

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import DictProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.toast import toast
from kivymd.uix.floatlayout import MDFloatLayout

import numpy
from scipy.signal import convolve2d

from gui.components.cell.cell import Cell

Builder.load_file("components/grid/grid.kv")


class Grid(MDFloatLayout):
    parameters = DictProperty(
        {
            "dimension": None,
            "life_color": None,
            "death_color": None,
            "lines_color": None,
            "show_lines": None,
            "lines_width": None,
            "cell_size": None,
        }
    )

    def __init__(self, *args, **kwargs):
        self.content = None
        self.name = ""
        self._parameters = {}
        self.new_cells = []
        self.new_cells_count = 0
        self.minimum_cell_size = None
        self.maximum_cell_size = None
        self.zoomable = False
        self.cells = {}
        self.running = False
        self.simulator = None

        super().__init__(*args, **kwargs)

        Window.bind(on_key_down=self._on_key_down)


    def on_kv_post(self, base_widget):
        self.minimum_cell_size = (Window.width - ((self.cols + 1) * self.lines_width if self.show_lines else 0)) // self.cols
        self.maximum_cell_size = (Window.width//16) - (self.lines_width * 9)

        Clock.schedule_once(self.set_content, 1)


    def set_content(self, dt):
        parameters_keys = Grid.parameters.get(self).keys()
        parameters = {}

        self.content = self.get_content()
        self.ids.ground.add_widget(self.content)

        for key in parameters_keys:
            parameters[key] = getattr(self, key)

        self.parameters = parameters


    def get_content(self):
        content = self.content or self.generate_content()

        return content


    def generate_content(self):
        cols = self.dimension[0]
        rows = self.dimension[1]

        if self.minimum_cell_size > self.cell_size:
            self.cell_size = self.minimum_cell_size

        elif self.maximum_cell_size < self.cell_size:
            self.cell_size = self.maximum_cell_size

        content = GridLayout(
            cols=cols,
            rows=rows,
            size_hint=(None, None),
            size=((self.cell_size * cols) + ((cols + 1) * self.lines_width if self.show_lines else 0), (self.cell_size * rows) + ((rows + 1) * self.lines_width if self.show_lines else 0))
        )

        if self.show_lines:
            content.spacing = self.lines_width
            content.padding = self.lines_width

        Clock.schedule_once(
            partial(
                self.update_content,
                {
                    "dimension": self.dimension
                }
            ), .0
        )

        return content


    def update_content(self, updates, dt=.0):
        def update_dimension(content, dimension):
            def add_cells(count):
                def add_next_cell(_dt):
                    if self.new_cells:
                        content.add_widget(self.new_cells.pop(0))

                        return True

                    else:
                        return False

                def add_batch(_dt):
                    size = 100

                    if self.new_cells_count:
                        if self.new_cells_count > size:
                            self.new_cells_count -= size

                        else:
                            size = self.new_cells_count
                            self.new_cells_count = 0

                        self.new_cells.extend(
                            [
                                Cell(
                                    size=(self.cell_size, self.cell_size),
                                    death_color=self.death_color,
                                    life_color=self.life_color,
                                    alive=False
                                ) for j in range(size)
                            ]
                        )

                        Clock.schedule_interval(
                            add_next_cell,
                            .0
                        )

                        return True

                    else:
                        return False

                self.new_cells_count = count

                Clock.schedule_interval(
                    add_batch,
                    .0
                )

                # todo: add batch adding | batch size =

            def remove_cells(count):
                pass

            def update_ratio():
                # todo: update self.rows and self.cols
                pass

            current_size = len(self.content.children)
            new_size = math.prod(dimension)
            size_difference = abs(current_size - new_size)

            if current_size < new_size:
                add_cells(size_difference)

            elif current_size > new_size:
                remove_cells(size_difference)

        def update_cell_size(content, direction):
            scale_value = 1

            to_scale = False

            match direction:
                case "+":
                    if self.cell_size + scale_value <= self.maximum_cell_size:
                        print("+", self.cell_size)
                        self.cell_size += scale_value

                        to_scale = True

                case "-":
                    if self.cell_size - scale_value >= self.minimum_cell_size:
                        print("-", self.cell_size)
                        self.cell_size -= scale_value

                        to_scale = True

                case _:
                    raise ValueError(f"{direction} is missing in zoom parameters so can not be updated")

            if to_scale:
                content.size = (
                    (self.cell_size * self.cols) + ((self.cols + 1) * self.lines_width if self.show_lines else 0),
                    (self.cell_size * self.rows) + ((self.rows + 1) * self.lines_width if self.show_lines else 0))

        for key, value in updates.items():
            match key:
                case "dimension":
                    update_dimension(self.content, value)

                case "cell_size":
                    update_cell_size(self.content, value)

                case _:
                    raise ValueError(f"{key} is missing in parameters so can not be updated")


    def idle(self):
        simulator = self.get_simulator()
        print(hash(str(simulator.content)))
        print(hash(str(simulator.content)))
        simulator.tick()
        print(hash(str(simulator.content)))
        print(hash(str(simulator.content)))
        self.set_simulator()


    def set_simulator(self):
        cells = list(reversed(self.content.children))
        frame = []

        for row in self.simulator.content:
            frame.extend(row)

        else:
            for i in range(len(frame)):
                cells[i].alive = frame[i] == 1

    def get_simulator(self):
        if not self.simulator:
            cells = list(reversed(self.content.children))
            frame = []

            for i in range(self.rows):
                frame.append([1 if cell.alive else 0 for cell in cells[:self.cols]])
                cells = cells[self.cols:]

            else:
                self.simulator = Simulator(frame)

        return self.simulator



    def on_parameters(self, instance, value):
        _parameters = self._parameters

        if _parameters:
            print(value)
            print(_parameters)

            # todo: when dimension changes, call set_grid
            # todo: when others change, call update grid with a dict of parameters and values
            # todo: update the grid

        self._parameters = _parameters


    def on_touch_down(self, touch):
        if self.zoomable:
            if touch.button == 'scrollup':
                Clock.schedule_once(
                    partial(
                        self.update_content,
                        {
                            "cell_size": "-"
                        }
                    )
                )

            elif touch.button == 'scrolldown':
                Clock.schedule_once(
                    partial(
                        self.update_content,
                        {
                            "cell_size": "+"
                        }
                    )
                )

            return True

        return super().on_touch_down(touch)


    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        key_string = Window._system_keyboard.keycode_to_string(key)

        if key_string == 'z' and 'ctrl' in modifiers:
            self.zoomable = not self.zoomable
            toast(f"Zoom : {self.zoomable}", duration=2.5)

        elif key_string == '6' and 'ctrl' in modifiers:
            Clock.schedule_once(
                partial(
                    self.update_content,
                    {
                        "cell_size": "-"
                    }
                )
            )

        elif key_string == '=' and 'ctrl' in modifiers:
            Clock.schedule_once(
                partial(
                    self.update_content,
                    {
                        "cell_size": "+"
                    }
                )
            )

        elif key_string == "spacebar":
            self.idle()


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
