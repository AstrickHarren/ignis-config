import os

from gi.repository import GdkPixbuf

import ignis
from ignis.services.upower import UPowerDevice, UPowerService
from ignis.widgets import Widget
from modules.common import Svg, Variable

upower = UPowerService.get_default()


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
            child=Svg("flash", css_classes=["icon-sm"]),
            reveal_child=connected_to_power.bind("value"),
            transition_type="crossfade",
        )

        super().__init__(
            css_classes=["mr-7", "ml-2"],
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
