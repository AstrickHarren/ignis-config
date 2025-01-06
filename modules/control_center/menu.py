from gi.repository import GObject  # type: ignore

from ignis.base_widget import BaseWidget
from ignis.variable import Variable
from ignis.widgets import Widget

opened_menu = Variable()


class Menu(Widget.Revealer):
    def __init__(self, name: str, child: list[BaseWidget], **kwargs):
        self._name = name
        self._box = Widget.Box(
            vertical=True,
            css_classes=["control-center-menu"],
            child=child,
        )

        super().__init__(
            transition_type="slide_down",
            transition_duration=300,
            reveal_child=opened_menu.bind("value", lambda value: value == self._name),
            child=self._box,
            **kwargs,
        )

    def toggle(self) -> None:
        print(f"toggling Menu: {opened_menu}")

        if self.reveal_child:
            opened_menu.value = ""
        else:
            opened_menu.value = self._name

    @GObject.Property
    def box(self) -> Widget.Box:
        return self._box
