# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

import datetime
from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.app import IgnisApp
from ignis.services.audio import AudioService
from ignis.services.system_tray import SystemTrayService, SystemTrayItem
from ignis.services.hyprland import HyprlandService
from ignis.services.niri import NiriService
from ignis.services.notifications import NotificationService
from ignis.services.mpris import MprisService, MprisPlayer

from modules.clock import clock
from modules.workspaces import workspaces

app = IgnisApp.get_default()

app.apply_css(f"{Utils.get_current_dir()}/style.scss")


audio = AudioService.get_default()
system_tray = SystemTrayService.get_default()
hyprland = HyprlandService.get_default()
niri = NiriService.get_default()
notifications = NotificationService.get_default()
mpris = MprisService.get_default()


def bar(monitor_id: int = 0) -> Widget.Window:
    monitor_name = Utils.get_monitor(monitor_id).get_connector()  # type: ignore
    return Widget.Window(
        namespace=f"ignis_bar_{monitor_id}",
        monitor=monitor_id,
        anchor=["left", "top", "right"],
        exclusivity="exclusive",
        child=Widget.CenterBox(
            css_classes=["bar"],
            center_widget=Widget.Box(child = [workspaces()]),
            end_widget = Widget.Box(child = [clock(monitor_id)]),
        ),
    )


# this will display bar on all monitors
for i in range(Utils.get_n_monitors()):
    bar(i)
