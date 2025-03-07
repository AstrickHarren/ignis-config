import datetime

from ignis.app import IgnisApp
from ignis.utils import Utils
from ignis.variable import Variable
from ignis.widgets import Widget

from .indicator import wifi_icon

app = IgnisApp.get_default()

current_time = Variable(
    value=Utils.Poll(1000, lambda x: datetime.datetime.now().strftime("%H:%M")).bind(
        "output"
    )
)


def clock(monitor):
    window: Widget.Window = app.get_window("ignis_CONTROL_CENTER")  # type: ignore

    def on_click(x):
        if window.monitor == monitor:
            window.visible = not window.visible
        else:
            window.set_monitor(monitor)
            window.visible = True

    css = ["round-lg", "bg-2", "px-4", "txt", "hover:bg-4", "transition-all"]
    active = css + ["bg-4"]
    active.remove("hover:bg-4")

    return Widget.Button(
        child=Widget.Box(
            child=[
                Widget.Label(
                    label=current_time.bind("value"),
                ),
            ],
        ),
        css_classes=window.bind("visible", lambda value: active if value else css),
        on_click=on_click,
    )
