from typing import Literal

from ignis.base_widget import BaseWidget
from ignis.services.audio import AudioService, Stream
from ignis.utils import Utils
from ignis.variable import Variable
from ignis.widgets import Widget
from ignis.widgets.arrow_button import ArrowButton
from modules.ctrl_center.ctrl_panel import PanelToggle, Toggle
from modules.ctrl_center.list import Item

AUDIO_TYPES = {
    "speaker": {"menu_icon": "audio-headphones-symbolic", "menu_label": "Sound Output"},
    "microphone": {
        "menu_icon": "microphone-sensitivity-high-symbolic",
        "menu_label": "Sound Input",
    },
}

audio = AudioService.get_default()


class DeviceItem(Item):
    def __init__(self, stream: Stream, _type: Literal["speaker", "microphone"]):
        super().__init__(
            checked=stream.bind("is_default"),
            label=stream.description,
            icon_name="audio-card-symbolic",
            on_click=lambda _: setattr(audio, _type, stream),
        )


class VolumeSlider(Toggle):
    def __init__(self, _type: Literal["speaker", "microphone"]):
        audio = AudioService.get_default()
        stream = getattr(audio, _type)
        self.is_opened = Variable(False)

        self._type = _type
        self.icon = Widget.Button(
            halign="start",
            child=Widget.Icon(
                image=stream.bind("icon_name"),
                pixel_size=18,
            ),
            css_classes=["px-4", "txt-bg-4"],
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
            rotated=self.is_opened.bind("value"),
        )

        super().__init__(
            "Volume",
            target=Widget.Scroll(
                css_classes=["mb-10"],
                height_request=200,
                child=Widget.Box(
                    vertical=True,
                    setup=lambda self: audio.connect(
                        f"{_type}-added",
                        lambda x, stream: self.append(DeviceItem(stream, _type)),
                    ),
                ),
            ),
            is_opened=self.is_opened,
        )

    def make_toggle(self, toggler) -> BaseWidget:
        return Widget.Box(
            hexpand=True,
            css_classes=["p-2"],
            child=[
                Widget.Overlay(
                    css_classes=["p-4"],
                    hexpand=True,
                    overlays=[self.icon],
                    child=self.scale,
                ),
                Widget.Button(
                    child=self.arrow,
                    on_click=lambda _: toggler(self.name),
                ),
            ],
        )


class Volume(VolumeSlider):
    def __init__(self):
        super().__init__("speaker")
