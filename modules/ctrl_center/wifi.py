from gi.repository import GLib  # type: ignore

from ignis.gobject import Binding
from ignis.services.network import NetworkService, WifiAccessPoint
from ignis.variable import Variable
from ignis.widgets import Widget
from modules.ctrl_center.list import Item
from modules.ctrl_center.quick_setting import QuickSetting
from modules.ctrl_center.wifi_dev import WifiDevice


class WifiItem(Widget.Box):
    def __init__(self, ap) -> None:
        self.expand = Variable(False)
        self.ap = ap

        def on_detail_accept(_):
            self.expand.value = False
            print("connecting to ap")
            self.ap.connect_with_password(password=self.input.text)

        self.input = Widget.Entry(hexpand=True, on_accept=on_detail_accept)
        detail = Widget.Revealer(
            child=Widget.Box(child=[Widget.Label(label="password"), self.input]),
            reveal_child=self.expand.bind("value"),
        )

        item = Item(
            checked=ap.bind("is_connected"),
            label=ap.ssid,  # type: ignore
            icon_name=ap.bind("strength", lambda _: ap.icon_name),
            on_click=lambda _: self.on_click(),
        )
        super().__init__(vertical=True, child=[item, detail])

    def on_click(self):
        conn = self.ap.saved_conn()
        if conn:
            print("connecting to known wifi")
            conn.connect_to()
            return
        self.expand.value = not self.expand.value


class Wifi(QuickSetting):
    def __init__(self):
        network = NetworkService.get_default()
        self.dev = WifiDevice(network.wifi.devices[0])  # type: ignore

        def get_label():
            return (
                self.dev.ap.ssid
                if self.dev.state == "activated"
                else self.dev.state.capitalize()
            )

        def itemize(_):
            return [WifiItem(ap) for ap in self.dev.access_points if ap.ssid]

        super().__init__(
            name="Wi-Fi",
            icon_name=self.dev.ap.bind("icon-name"),  # type: ignore
            label=self.dev.ap.bind("icon-name", lambda _: get_label()),  # type: ignore
            target=Widget.Scroll(
                height_request=400,
                child=Widget.Box(
                    vertical=True,
                    child=self.dev.ap.bind("icon_name", itemize),
                ),
            ),
        )

    def on_open(self):
        super().on_open()
        self.dev.scan()
