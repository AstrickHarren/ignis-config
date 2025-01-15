import shutil

from ignis.services.recorder import util
from ignis.utils import Utils
from ignis.widgets import Widget
from modules.common import Svg


class Screenshot(Widget.Button):
    def __init__(self):
        # self.icon = Widget.Icon(icon_name="applets-screenshooter-symbolic")
        self.icon = Svg("screenshot", css_classes=["icon-4xl"])
        sh = "hyprshot -m region -o $HOME/Pictures/Screenshots"
        super().__init__(
            visible=self.check_visible(),
            style="padding-right: 1.03rem;",
            css_classes=[
                "px-4",
                "mx-2",
                "hover:bg-4",
                "round",
                "transition-all",
            ],
            child=self.icon,
            on_click=lambda _: Utils.exec_sh_async(sh),
        )

    def check_visible(self) -> bool:
        return shutil.which("hyprshot") is not None
