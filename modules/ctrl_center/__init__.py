# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false
from ignis.app import IgnisApp
from ignis.base_widget import BaseWidget
from ignis.widgets import Widget
from modules.ctrl_center.bluetooth import Bluetooth
from modules.ctrl_center.ctrl_panel import Panel
from modules.ctrl_center.wifi import Wifi

app = IgnisApp.get_default()


class ControlCenter(Widget.RevealerWindow):
    def __init__(self, child):
        revealer = Widget.Revealer(
            transition_type="slide_left",
            child=Widget.Box(
                vertical=True,
                css_classes=["control-center"],
                child=[
                    Widget.Box(
                        vertical=True,
                        css_classes=["control-center-widget"],
                        child=child,
                    ),
                ],
            ),
            transition_duration=300,
            reveal_child=True,
        )

        invisible_toggle = Widget.Button(
            vexpand=True,
            hexpand=True,
            css_classes=["unset"],
            on_click=lambda x: app.close_window("ignis_CONTROL_CENTER"),
        )
        super().__init__(
            visible=False,
            popup=True,
            kb_mode="on_demand",
            layer="top",
            css_classes=["unset"],
            anchor=["top", "right", "bottom", "left"],
            namespace="ignis_CONTROL_CENTER",
            child=Widget.Box(
                child=[
                    invisible_toggle,
                    revealer,
                ],
            ),
            revealer=revealer,
        )
