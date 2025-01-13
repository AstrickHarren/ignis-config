from ignis.services.upower import UPowerDevice, UPowerService
from ignis.widgets import Widget

upower = UPowerService.get_default()


class BatteryItem(Widget.Box):
    def __init__(self, device: UPowerDevice):
        self.scale = Widget.Scale(
            css_classes=["battery-slider"],
            value=100,
            step=5,
            hexpand=True,
            sensitive=False,
        )
        self.label = Widget.Label(
            label=device.bind("percent", lambda x: f"{int(x)}%"),
            css_classes=["txt", "mx-2"],
        )

        super().__init__(
            css_classes=["mx-9"],
            setup=lambda self: device.connect("removed", lambda x: self.unparent()),
            child=[
                self.label,
                self.scale,
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
