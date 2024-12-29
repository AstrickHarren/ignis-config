import datetime
from ignis.widgets import Widget
from ignis.app import IgnisApp
from ignis.utils import Utils
from ignis.variable import Variable

app = IgnisApp.get_default()

current_time = Variable(
    value=Utils.Poll(1000, lambda x: datetime.datetime.now().strftime("%H:%M")).bind(
        "output"
    )
)


def clock(monitor):
    return Widget.Button(
        child=Widget.Box(
            child=[
                Widget.Label(
                    label=current_time.bind("value"),
                ),
            ]
        ),
    )
