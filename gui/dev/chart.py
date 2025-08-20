from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout

# Custom widget for the line chart
class LineChartWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points = [(50, 100), (100, 200), (150, 150), (200, 250), (300, 100)]  # Example points

    def on_size(self, *args):
        self.draw_chart()

    def draw_chart(self):
        self.canvas.clear()

        with self.canvas:
            Color(0, 1, 1, 1)  # Set the color to blue
            # Draw the line chart
            Line(points=[(50, 100), (600, 100)], width=.3)
            Line(points=[(50, 200), (600, 200)], width=.3)
            Line(points=[(50, 300), (600, 300)], width=.3)
            Line(points=[(50, 400), (600, 400)], width=.3)
            Line(points=[(50, 500), (600, 500)], width=.3)

        with self.canvas:
            Color(0, 0, 1, 1)  # Set the color to blue
            # Draw the line chart
            Line(points=[point for point in self.points], width=1.5)


class LineChartApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation="vertical")
        chart_widget = LineChartWidget(size_hint=(1, 0.8))
        layout.add_widget(chart_widget)

        # Update chart on window resize
        # chart_widget.bind(size=chart_widget.on_size)

        return layout


if __name__ == "__main__":
    LineChartApp().run()
