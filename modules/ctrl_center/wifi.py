from gi.repository import GLib  # type: ignore

from ignis.gobject import Binding
from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice
from ignis.variable import Variable
from ignis.widgets import Widget
from modules.ctrl_center.ap import Ap
from modules.ctrl_center.list import Item
from modules.ctrl_center.quick_setting import QuickSetting


class WifiItem(Widget.Box):
    def __init__(self, ap: Ap) -> None:
        self.expand = Variable(False)
        self.ap = ap

        def on_detail_accept(_):
            self.expand.value = False
            self.ap.connect_to(password=self.input.text)

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
        if self.ap.is_saved():
            self.ap.connect_to()
        else:
            self.expand.value = not self.expand.value


class WifiDev(WifiDevice):
    def __init__(self, dev: WifiDevice) -> None:
        super().__init__(dev._device, dev._client)


class Wifi(QuickSetting):
    def __init__(self):
        network = NetworkService.get_default()
        self.dev = WifiDev(network.wifi.devices[0])  # type: ignore

        def get_label():
            ap = self.dev._device.get_active_access_point()
            if ap is None:
                return "Not Connected"
            return ap.get_ssid().get_data().decode("utf-8")

        def get_aps():
            aps = self.dev.access_points
            conns = self.dev._device.get_available_connections()
            ret = {}
            for ap in aps:  # type: ignore
                ret[ap.ssid] = Ap(ap)
            for conn in conns:
                if conn.get_id() in ret:
                    ret[conn.get_id()].conn = conn

            return ret

        def itemize(_):
            return [WifiItem(ap) for ap in get_aps().values() if ap.ssid]

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
