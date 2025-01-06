from typing import Sequence

from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.variable import Variable
from ignis.widgets import Widget


class PanelToggle(Widget.Box):
    def __init__(
        self,
        name: str,
        child: BaseWidget,
        target: BaseWidget,
        css_classes: list[str] = [],
        is_opened: Variable | None = None,
        **kwargs,
    ):
        super().__init__(css_classes=css_classes + ["m-2"], child=[child], **kwargs)
        self.name = name
        self.target = target
        self.is_opened = is_opened

    def content(self, opened_menu: Variable) -> Widget.Revealer:
        if self.is_opened:
            self.is_opened.value = opened_menu.value == self.name

        return Widget.Revealer(
            child=self.target,
            reveal_child=opened_menu.bind("value", lambda x: self._reveal_child(x)),
            transition_duration=300,
            transition_type="slide_down",
        )

    def on_open(self):
        if self.is_opened:
            self.is_opened.value = True

    def on_close(self):
        if self.is_opened:
            self.is_opened.value = False

    def _reveal_child(self, opened_menu: str):
        if opened_menu == self.name and self.is_opened and not self.is_opened.value:
            self.on_open()
        if opened_menu != self.name and self.is_opened and self.is_opened.value:
            self.on_close()
        return opened_menu == self.name


class Panel(Widget.Box):
    def __init__(self, toggles: Sequence[PanelToggle], **kwargs) -> None:
        self.opened_menu = Variable()
        self.summary = Widget.Box(
            vertical=True,
            css_classes=["bg-3", "round-lg", "my-10"],
            child=[self._make_toggle(t) for t in toggles],
        )
        self.detail = [t.content(self.opened_menu) for t in toggles]
        super().__init__(
            child=[self.summary] + self.detail,
            vertical=True,
            **kwargs,
        )

    def _make_toggle(self, t):
        return Widget.Button(
            hexpand=True, on_click=lambda _: self.toggle_detail(t.name), child=t
        )

    def toggle_detail(self, name: str):
        if self.opened_menu.value == name:
            self.opened_menu.value = ""
        else:
            self.opened_menu.value = name
