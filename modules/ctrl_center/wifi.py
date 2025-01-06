from ignis.base_widget import BaseWidget
from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice
from ignis.variable import Variable
from ignis.widgets import Widget
from modules.ctrl_center.ctrl_panel import PanelToggle
from modules.ctrl_center.quick_setting import QuickSetting


class WifiItem(Widget.Button):
    def __init__(self, ap: WifiAccessPoint):
        super().__init__(
            hexpand=True,
            on_click=lambda _: ap.connect_to(),
            child=Widget.Box(
                css_classes=["my-2", "p-2"],
                hexpand=True,
                child=[
                    Widget.Icon(
                        css_classes=["w-10"],
                        image="object-select-symbolic",
                        visible=ap.bind("is_connected"),
                        pixel_size=18,
                    ),
                    Widget.Box(
                        css_classes=["w-10"],
                        visible=ap.bind("is_connected", lambda x: not x),
                    ),
                    Widget.Box(
                        css_classes=["border-b-2", "border-solid", "border-separator"],
                        hexpand=True,
                        child=[
                            Widget.Label(
                                label=ap.ssid,
                                halign="start",
                                css_classes=["txt"],
                            ),
                            Widget.Icon(
                                hexpand=True,
                                halign="end",
                                image=ap.bind(
                                    "strength", transform=lambda _: ap.icon_name
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )


class Wifi(QuickSetting):
    def __init__(self):
        network = NetworkService.get_default()
        self.dev: WifiDevice = network.wifi.devices[0]  # type: ignore

        super().__init__(
            name="Wi-Fi",
            # icon_name=self.dev.ap.bind("icon-name"),  # type: ignore
            icon_name=self.dev.ap.bind("icon-name"),  # type: ignore
            label=self.dev.ap.bind(  # type: ignore
                "ssid", lambda ssid: ssid if ssid else "Wi-Fi"
            ),
            target=Widget.Scroll(
                height_request=400,
                child=Widget.Box(
                    vertical=True,
                    child=self.dev.bind(
                        "access_points",
                        lambda aps: [WifiItem(ap) for ap in aps if ap.ssid],
                    ),
                ),
            ),
        )

    def on_open(self):
        super().on_open()
        self.dev.scan()
