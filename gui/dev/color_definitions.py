from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.factory import Factory
from screeninfo import get_monitors

demo = '''
<Root@MDBoxLayout>:
    orientation: 'vertical'

    MDTopAppBar:
        title: app.title

    MDTabs:
        id: android_tabs
        on_tab_switch: app.on_tab_switch(*args)
        size_hint_y: None
        height: "48dp"
        tab_indicator_anim: False

    MDBoxLayout:
        id: container
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'
        size_hint_y: None
        height: self.minimum_height

<ItemColor>:
    size_hint_y: None
    height: "48dp"
    MDCard:
        size_hint: None, None
        size: "200dp", "48dp"
        pos_hint: {"center_x": 0.5}
        md_bg_color: root.color  # Set background color of the card
        padding: "8dp"

        MDLabel:
            text: root.text  # Display the color name
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1  # Make sure the text is visible
'''

class Tab(MDBoxLayout, MDTabsBase):
    pass

class ItemColor(MDBoxLayout):
    text = StringProperty()
    color = ListProperty()

class Palette(MDApp):
    title = "Colors Definitions"

    def build(self):
        Builder.load_string(demo)
        self.screen = Factory.Root()

        for name_tab in colors.keys():
            tab = Tab(title=name_tab)
            self.screen.ids.android_tabs.add_widget(tab)
        return self.screen

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tabs_label, tab_text):
        container = self.screen.ids.container
        container.clear_widgets()

        if not tab_text:
            tab_text = 'Red'  # Default tab if none is selected

        for value_color, hex_value in colors[tab_text].items():
            container.add_widget(
                ItemColor(text=value_color, color=get_color_from_hex(hex_value))
            )

    def on_start(self):
        self.on_tab_switch(
            None,
            None,
            None,
            self.screen.ids.android_tabs.ids.layout.children[-1].text,
        )

        monitor_size = get_monitors()[0]

        Window.size = monitor_size.width, monitor_size.height
        Window.top = 0
        Window.left = 0

Palette().run()
