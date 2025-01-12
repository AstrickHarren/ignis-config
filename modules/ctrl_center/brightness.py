from ignis.services.backlight import BacklightService
from ignis.widgets import Widget
from modules.ctrl_center.ctrl_panel import Toggle

backlight = BacklightService.get_default()


class Brightness(Toggle):
    def __init__(self):
        self.icon = Widget.Icon(
            image="display-brightness-symbolic",
            css_classes=["material-slider-icon"],
            pixel_size=18,
        )

        self.scale = (
            Widget.Scale(
                min=0,
                max=backlight.max_brightness,
                hexpand=True,
                value=backlight.bind("brightness"),
                css_classes=["material-slider"],
                on_change=lambda x: backlight.set_brightness(x.value),
            ),
        )
        super().__init__("Brightness")

    def make_toggle(self, toggler):
        return Widget.Box(
            visible=backlight.bind("available"),
            hexpand=True,
            child=[self.icon, self.scale],
        )
