from typing import Literal

from ignis.base_widget import BaseWidget
from ignis.services.audio import AudioService, Stream
from ignis.utils import Utils
from ignis.variable import Variable
from ignis.widgets import Widget
from ignis.widgets.arrow_button import ArrowButton
from modules.ctrl_center.ctrl_panel import PanelToggle, Toggle

AUDIO_TYPES = {
    "speaker": {"menu_icon": "audio-headphones-symbolic", "menu_label": "Sound Output"},
    "microphone": {
        "menu_icon": "microphone-sensitivity-high-symbolic",
        "menu_label": "Sound Input",
    },
}


class VolumeSlider(Toggle):
    def __init__(self, _type: Literal["speaker", "microphone"]):
        audio = AudioService.get_default()
        stream = getattr(audio, _type)
        is_opened = Variable(False)

        self._type = _type
        self.icon = Widget.Button(
            child=Widget.Icon(
                image=stream.bind("icon_name"),
                pixel_size=18,
            ),
            css_classes=["material-slider-icon", "unset", "hover-surface"],
            on_click=lambda x: stream.set_is_muted(not stream.is_muted),
        )

        self.scale = Widget.Scale(
            css_classes=["material-slider", "m-10"],
            value=stream.bind("volume"),
            step=5,
            hexpand=True,
            on_change=lambda x: stream.set_volume(x.value),
            sensitive=stream.bind("is_muted", lambda value: not value),
        )

        self.arrow = Widget.Arrow(
            css_classes=["txt-2"],
            halign="end",
            hexpand=True,
            pixel_size=20,
            rotated=is_opened.bind("value"),
        )

        super().__init__(
            "Volume",
            target=Widget.Label(label="hello"),
            is_opened=is_opened,
        )

    def make_toggle(self, toggler) -> BaseWidget:
        return Widget.Box(
            vertical=True,
            hexpand=True,
            child=[
                Widget.Box(
                    child=[
                        self.icon,
                        self.scale,
                        ArrowButton(
                            arrow=self.arrow, on_click=lambda _: toggler(self.name)
                        ),
                    ]
                ),
            ],
            css_classes=[f"volume-mainbox-{self._type}"],
        )


class Volume(VolumeSlider):
    def __init__(self):
        super().__init__("speaker")
