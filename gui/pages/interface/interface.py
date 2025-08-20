from datetime import datetime, timezone
from functools import partial

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp


Builder.load_file("pages/interface/interface.kv")

class Interface(MDScreen):
    def __init__(self, *args, **kwargs):
        self.new_size = {
            "task": None,
            "value": None
        }

        super().__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        Window.bind(size=self.on_window_resize)

    def on_window_resize(self, instance, size):
        new_size = self.new_size

        if new_size["task"]:
            new_size["task"].cancel()

        self.new_size = {
            "task": Clock.schedule_once(partial(self.resize, size), .5),
            "value": size
        }


    def resize(self, size, dt):
        side = min([size[0], size[1]])

        Window.size = (side, side)

        whole = self.ids["whole"]
        whole.size_hint = (None, None)
        whole.size = (side, side)
        whole.pos_hint = {
            "center_x": .5,
            "center_y": .5,
        }

        self.new_size = {
            "task": None,
            "value": None
        }
