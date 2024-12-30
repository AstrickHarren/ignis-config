# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false, reportFunctionMemberAccess=false

from typing import Callable

from gi.repository import GObject

from ignis.gobject import Binding
from ignis.widgets import Widget


class QSButton(Widget.Button):
    def __init__(
        self,
        icon_name: str | Binding,
        on_activate: Callable | None = None,
        on_deactivate: Callable | None = None,
        content: Widget.Revealer | None = None,
        **kwargs,
    ):
        self.on_activate = on_activate
        self.on_deactivate = on_deactivate
        self._active = False
        self._content = content
        super().__init__(
            child=Widget.Box(
                child=[
                    Widget.Icon(image=icon_name),
                ]
            ),
            on_click=self.__callback,
            css_classes=["qs-button", "unset"],
            hexpand=True,
            **kwargs,
        )

    def __callback(self, *args) -> None:
        if self.active:
            if self.on_deactivate:
                self.on_deactivate(self)
        else:
            if self.on_activate:
                self.on_activate(self)

    @GObject.Property
    def active(self) -> bool:  # type: ignore
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value
        if value:
            self.add_css_class("active")
        else:
            self.remove_css_class("active")

    @GObject.Property
    def content(self) -> Widget.Revealer | None:
        return self._content
