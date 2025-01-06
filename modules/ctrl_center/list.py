from ignis.gobject import Binding
from ignis.services.network import WifiAccessPoint
from ignis.widgets import Widget


class Item(Widget.Button):
    def __init__(
        self,
        checked: bool | Binding,
        label: str | Binding,
        icon_name: str | Binding,
        **kwargs
    ):
        unchecked = Binding(
            checked.target,  # type: ignore
            checked.target_property,  # type: ignore
            lambda x: (
                not checked.transform(x) if checked.transform else not x  # type: ignore
            ),
        )

        super().__init__(
            hexpand=True,
            child=Widget.Box(
                css_classes=["p-2"],
                hexpand=True,
                child=[
                    Widget.Icon(
                        css_classes=["w-10", "pb-2"],
                        image="object-select-symbolic",
                        visible=checked,
                        pixel_size=18,
                    ),
                    Widget.Box(css_classes=["w-10", "pb-2"], visible=unchecked),
                    Widget.Box(
                        css_classes=[
                            "border-b-2",
                            "border-solid",
                            "border-separator",
                            "pb-4",
                        ],
                        hexpand=True,
                        child=[
                            Widget.Label(
                                label=label,
                                halign="start",
                                css_classes=["txt"],
                            ),
                            Widget.Icon(
                                hexpand=True,
                                halign="end",
                                icon_name=icon_name,
                            ),
                        ],
                    ),
                ],
            ),
            **kwargs
        )
