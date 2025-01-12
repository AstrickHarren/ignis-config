from ignis.base_widget import BaseWidget
from ignis.services.bluetooth import BluetoothDevice, BluetoothService
from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice
from ignis.variable import Variable
from ignis.widgets import Widget, label
from modules.ctrl_center.list import Item
from modules.ctrl_center.quick_setting import QuickSetting


class BluetoothItem(Item):
    def __init__(self, dev: BluetoothDevice):
        super().__init__(
            checked=dev.bind("connected"),
            label=dev.bind("name"),
            icon_name=dev.bind("icon_name"),
            on_click=lambda _: dev.connect_to,
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
                    f"{len(devs)} devices"
                    if len(devs) > 1
                    else (
                        devs[0].name
                        if len(devs) == 1
                        else self.service.state.capitalize()
                    )
                ),
            ),
            target=Widget.Scroll(
                css_classes=["mb-10"],
                height_request=400,
                child=Widget.Box(
                    vertical=True,
                    child=self.service.bind(
                        "devices",
                        lambda devs: [BluetoothItem(dev) for dev in devs if dev.name],
                    ),
                ),
            ),
        )

    def on_open(self):
        self.service.setup_mode = True
        super().on_open()
