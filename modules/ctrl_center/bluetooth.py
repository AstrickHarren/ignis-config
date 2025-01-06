from ignis.base_widget import BaseWidget
from ignis.services.bluetooth import BluetoothDevice, BluetoothService
from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice
from ignis.variable import Variable
from ignis.widgets import Widget, label
from modules.control_center.menu import Menu
from modules.control_center.qs_button import QSButton
from modules.ctrl_center.ctrl_panel import PanelToggle
from modules.ctrl_center.quick_setting import QuickSetting


class BluetoothItem(Widget.Button):
    def __init__(self, dev: BluetoothDevice):
        super().__init__(
            css_classes=["wifi-network_item", "unset"],
            on_click=lambda x: dev.connect_to(),
            child=Widget.Box(
                child=[
                    Widget.Icon(
                        image=dev.icon_name,
                    ),
                    Widget.Label(
                        label=dev.name,
                        halign="start",
                    ),
                    Widget.Icon(
                        image="object-select-symbolic",
                        halign="end",
                        hexpand=True,
                        visible=dev.bind("connected"),
                    ),
                ]
            ),
        )


class Bluetooth(QuickSetting):
    def __init__(self):
        self.service = BluetoothService.get_default()
        super().__init__(
            name="Bluetooth",
            icon_name="bluetooth",
            label=self.service.bind(
                "connected_devices",
                lambda devs: (
                    f"{len(devs)} devices" if len(devs) > 0 else "not connected"
                ),
            ),
            target=Widget.Box(
                vertical=True,
                child=self.service.bind(
                    "devices",
                    lambda devs: [BluetoothItem(dev) for dev in devs if dev.name],
                ),
            ),
        )

    def on_open(self):
        self.service.setup_mode = True
        super().on_open()
