# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false, reportFunctionMemberAccess=false
from typing import Callable

from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice
from ignis.utils import Utils
from ignis.widgets import Widget

from .menu import Menu
from .qs_button import QSButton

network = NetworkService.get_default()


class WifiNetworkItem(Widget.Button):
    def __init__(self, access_point: WifiAccessPoint):
        super().__init__(
            css_classes=["wifi-network-item", "unset"],
            on_click=lambda x: access_point.connect_to_graphical(),
            child=Widget.Box(
                child=[
                    Widget.Icon(
                        image=access_point.bind(
                            "strength", transform=lambda value: access_point.icon_name
                        ),
                    ),
                    Widget.Label(
                        label=access_point.ssid,
                        halign="start",
                        css_classes=["wifi-network-label"],
                    ),
                    Widget.Icon(
                        image="object-select-symbolic",
                        halign="end",
                        hexpand=True,
                        visible=access_point.bind("is_connected"),
                    ),
                ]
            ),
        )


class WifiMenu(Menu):
    def __init__(self, device: WifiDevice):
        super().__init__(
            name="wifi",
            child=[
                Widget.Box(
                    vertical=True,
                    child=device.bind(
                        "access_points",
                        transform=lambda value: [
                            WifiNetworkItem(i)
                            for i in value
                            if i.ssid != "" and i.ssid is not None
                        ],
                    ),
                ),
            ],
        )


class WifiButton(QSButton):
    def __init__(self, device: WifiDevice):
        menu = WifiMenu(device)

        def get_icon(icon_name: str) -> str:
            if device.ap.is_connected:
                return icon_name
            else:
                return "network-wireless-symbolic"

        def toggle_list(x) -> None:
            device.scan()
            menu.toggle()

        super().__init__(
            icon_name=device.ap.bind("icon-name", get_icon),
            on_activate=toggle_list,
            on_deactivate=toggle_list,
            active=network.wifi.bind("enabled"),
            content=menu,
        )


def wifi_control() -> list[QSButton]:
    return [WifiButton(dev) for dev in network.wifi.devices]
