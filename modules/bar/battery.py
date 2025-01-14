import os

from gi.repository import GdkPixbuf

import ignis
from ignis.services.upower import UPowerDevice, UPowerService
from ignis.widgets import Widget

upower = UPowerService.get_default()


def flash_icon():
    svg = os.path.join(os.path.dirname(__file__), "../../svg/flash.svg")
    svg = open(svg, "r").read()
    loader = GdkPixbuf.PixbufLoader()
    loader.write(svg.encode())
    loader.close()
    return loader.get_pixbuf()


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


class BatteryItem(Widget.Box):
    def __init__(self, device: UPowerDevice):
        def css_classes():
            base = ["battery-slider"]
            normal = "battery-slider-normal"
            critical = "battery-slider-critical"
            charging = "battery-slider-charging"
            if device.charging or device.charged:
                return base + [charging]
            if device.percent <= 20:
                return base + [critical]
            return base + [normal]

        css_classes = Variable(css_classes)
        css_classes.subscribe(device, "notify::percent")
        css_classes.subscribe(device, "notify::charging")
        css_classes.subscribe(device, "notify::charged")

        self.scale = Widget.Scale(
            css_classes=css_classes.bind("value"),
            value=device.bind("percent"),
            step=1,
            max=100,
            hexpand=True,
            sensitive=False,
        )
        self.label = Widget.Label(
            label=device.bind("percent", lambda x: f"{int(x)}%"),
            css_classes=["txt", "mx-2"],
        )

        connected_to_power = Variable(lambda: device.charging or device.charged)
        connected_to_power.subscribe(device, "notify::charging")
        connected_to_power.subscribe(device, "notify::charged")

        self.charging_icon = Widget.Revealer(
            child=Widget.Icon(image=flash_icon(), css_classes=["icon-sm"]),
            reveal_child=connected_to_power.bind("value"),
            transition_type="crossfade",
        )

        super().__init__(
            css_classes=["mx-9"],
            setup=lambda self: device.connect("removed", lambda x: self.unparent()),
            child=[
                self.label,
                Widget.Overlay(
                    child=self.scale,
                    overlays=[self.charging_icon],
                ),
                Widget.Box(
                    valign="center",
                    css_classes=["battery-tip"],
                ),
            ],
        )


class Battery(Widget.Box):
    def __init__(self):
        super().__init__(
            setup=lambda self: upower.connect(
                "battery-added", lambda x, device: self.append(BatteryItem(device))
            ),
        )
