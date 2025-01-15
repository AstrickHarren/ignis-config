import os

from gi.repository import GdkPixbuf

import ignis.variable
from ignis.widgets import Widget


class Svg(Widget.Icon):
    def __init__(self, svg_name, **kwargs) -> None:
        svg = os.path.join(os.path.dirname(__file__), "../svg", svg_name + ".svg")
        svg = open(svg, "r").read()
        loader = GdkPixbuf.PixbufLoader()
        loader.write(svg.encode())
        loader.close()
        self.pixbuf = loader.get_pixbuf()
        super().__init__(image=self.pixbuf, **kwargs)


class Variable(ignis.variable.Variable):
    def __init__(self, refresh) -> None:
        self.refresh = refresh
        super().__init__(refresh())

    def subscribe(self, obj, signal):
        def call_back(*args):
            self.value = self.refresh()

        obj.connect(signal, call_back)

    def set_value(self, val):
        self.value = val
