import datetime

from ignis.app import IgnisApp
from ignis.utils import Utils
from ignis.variable import Variable
from ignis.widgets import Widget
from modules.bar import bar
from modules.ctrl_center import ControlCenter
from modules.ctrl_center.bluetooth import Bluetooth
from modules.ctrl_center.brightness import Brightness
from modules.ctrl_center.calendar import Calendar
from modules.ctrl_center.ctrl_panel import Panel
from modules.ctrl_center.volume import Volume
from modules.ctrl_center.wifi import Wifi
from modules.notification import NotificationPopup

app = IgnisApp.get_default()
app.apply_css(f"{Utils.get_current_dir()}/style.scss")

ControlCenter(
    [
        Panel([Volume()]),
        Panel([Wifi(), Bluetooth()]),
        Calendar(),
    ]
)
for monitor in range(Utils.get_n_monitors()):
    bar(monitor)
for monitor in range(Utils.get_n_monitors()):
    NotificationPopup(monitor)
