from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.services.network import WifiAccessPoint
from ignis.widgets import Widget


def truncate_label(label, max_len=40):
    if isinstance(label, Binding):
        label._transform = lambda l: truncate_label(l, max_len)
        return label

    if len(label) > max_len:
        return label[: max_len - 1] + "..."
    return label


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
            checked.target_properties,  # type: ignore
            lambda x: (
                not checked.transform(x) if checked.transform else not x  # type: ignore
            ),
        )

        super().__init__(
            hexpand=True,
            css_classes=["hover:bg-3", "transition-all"],
            child=Widget.Box(
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
                            "pt-4",
                            "pb-4",
                            "px-2",
                        ],
                        hexpand=True,
                        child=[
                            Widget.Label(
                                label=truncate_label(label),
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
