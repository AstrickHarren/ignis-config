from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.variable import Variable
from ignis.widgets import Widget
from modules.ctrl_center.ctrl_panel import PanelToggle


class QuickSetting(PanelToggle):
    def __init__(
        self,
        name: str,
        icon_name: str | Binding,
        label: str | Binding,
        target: BaseWidget,
        **kwargs
    ):
        is_opened = Variable(False)
        toggle = Widget.Box(
            hexpand=True,
            child=[
                Widget.Icon(
                    halign="start",
                    icon_name=icon_name,
                    css_classes=["round-full", "p-5", "m-3", "bg-blue"],
                    pixel_size=18,
                ),  # type: ignore
                Widget.Box(
                    halign="start",
                    valign="center",
                    css_classes=["p-2"],
                    vertical=True,
                    child=[
                        Widget.Label(
                            halign="start",
                            label=name,
                            css_classes=["txt", "bold", "m-1"],
                        ),
                        Widget.Label(
                            halign="start", label=label, css_classes=["txt-2", "m-1"]
                        ),
                    ],
                ),
                Widget.Arrow(
                    halign="end",
                    hexpand=True,
                    pixel_size=20,
                    rotated=is_opened.bind("value"),
                ),
            ],
        )

        super().__init__(
            name, child=toggle, target=target, is_opened=is_opened, **kwargs
        )
