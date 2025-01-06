from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice
from ignis.widgets import Widget
from modules.ctrl_center.list import Item
from modules.ctrl_center.quick_setting import QuickSetting


class WifiItem2(Item):
    def __init__(self, ap: WifiAccessPoint) -> None:
        super().__init__(
            checked=ap.bind("is_connected"),
            label=ap.ssid,  # type: ignore
            icon_name=ap.bind("strength", lambda _: ap.icon_name),
        )


class Wifi(QuickSetting):
    def __init__(self):
        network = NetworkService.get_default()
        self.dev: WifiDevice = network.wifi.devices[0]  # type: ignore

        super().__init__(
            name="Wi-Fi",
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
                        lambda aps: [WifiItem2(ap) for ap in aps if ap.ssid],
                    ),
                ),
            ),
        )

    def on_open(self):
        super().on_open()
        self.dev.scan()
