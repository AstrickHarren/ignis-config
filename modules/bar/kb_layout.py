from ignis.services.hyprland import HyprlandService
from ignis.widgets import Widget

hyprland = HyprlandService.get_default()


class KeyboardLayout(Widget.Button):
    def __init__(self):
        super().__init__(
            css_classes=[
                "mx-2",
                "px-2",
                "py-2",
                "hover:bg-4",
                "transition-all",
                "round",
            ],
            on_click=lambda x: hyprland.switch_kb_layout(),
            visible=hyprland.is_available,
            child=Widget.Label(
                label=hyprland.bind(
                    "kb_layout", transform=lambda value: value[:2].lower().capitalize()
                )
            ),
        )
