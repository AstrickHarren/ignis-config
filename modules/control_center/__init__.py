# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

from ignis.app import IgnisApp
from ignis.widgets import Widget

app = IgnisApp.get_default()


def control_center_widget() -> Widget.Box:
    return Widget.Box(
        vertical=True,
        css_classes=["control-center"],
        child=[
            Widget.Box(
                vertical=True,
                css_classes=["control-center-widget"],
                child=[Widget.Label(label="hello, world")],
            ),
        ],
    )


def control_center() -> Widget.RevealerWindow:
    revealer = Widget.Revealer(
        transition_type="slide_left",
        child=control_center_widget(),
        transition_duration=300,
        reveal_child=True,
    )
    box = Widget.Box(
        child=[
            Widget.Button(
                vexpand=True,
                hexpand=True,
                css_classes=["unset"],
                on_click=lambda x: app.close_window("ignis_CONTROL_CENTER"),
            ),
            revealer,
        ],
    )
    return Widget.RevealerWindow(
        visible=False,
        popup=True,
        kb_mode="on_demand",
        layer="top",
        css_classes=["unset"],
        anchor=["top", "right", "bottom", "left"],
        namespace="ignis_CONTROL_CENTER",
        child=box,
        revealer=revealer,
    )
