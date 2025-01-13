# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

from ignis.utils import Utils
from ignis.widgets import Widget
from modules.bar.battery import Battery
from modules.bar.kb_layout import KeyboardLayout

from .clock import clock
from .indicator import wifi_icon
from .workspaces import workspaces


def bar(monitor_id: int = 0) -> Widget.Window:
    return Widget.Window(
        namespace=f"ignis_bar_{monitor_id}",
        monitor=monitor_id,
        anchor=["left", "top", "right"],
        exclusivity="exclusive",
        child=Widget.CenterBox(
            css_classes=["bg", "py-2", "px-6"],
            center_widget=Widget.Box(child=[workspaces()]),
            end_widget=Widget.Box(
                child=[Battery(), wifi_icon(), KeyboardLayout(), clock(monitor_id)]
            ),
        ),
    )
