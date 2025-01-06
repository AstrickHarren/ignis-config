from abc import abstractmethod
from typing import Sequence, override

from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.variable import Variable
from ignis.widgets import Widget


class Toggle:
    def __init__(
        self,
        name: str,
        target: BaseWidget,
        is_opened: Variable | None = None,
    ) -> None:
        self.name = name
        self.target = target
        self.is_opened = is_opened

    @abstractmethod
    def make_toggle(self, toggler) -> BaseWidget:
        pass

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


class PanelToggle(Toggle):
    def __init__(
        self,
        name: str,
        child: BaseWidget,
        target: BaseWidget,
        css_classes: list[str] = [],
        is_opened: Variable | None = None,
        **kwargs,
    ):
        self.child = child
        self.css_classes = css_classes
        self.kwargs = kwargs
        super().__init__(name, target, is_opened)

    @override
    def make_toggle(self, toggler) -> BaseWidget:
        summary = Widget.Box(
            css_classes=self.css_classes + ["m-2"], child=[self.child], **self.kwargs
        )
        return Widget.Button(
            hexpand=True, on_click=lambda _: toggler(self.name), child=summary
        )


class Panel(Widget.Box):
    def __init__(self, toggles: Sequence[Toggle], **kwargs) -> None:
        self.opened_menu = Variable()
        self.summary = Widget.Box(
            vertical=True,
            css_classes=["bg-3", "round-lg", "p-3", "mb-10"],
            child=[t.make_toggle(self.toggle_detail) for t in toggles],
        )
        self.detail = [t.content(self.opened_menu) for t in toggles]
        super().__init__(
            child=[self.summary] + self.detail,
            vertical=True,
            **kwargs,
        )

    def toggle_detail(self, name: str):
        if self.opened_menu.value == name:
            self.opened_menu.value = ""
        else:
            self.opened_menu.value = name
