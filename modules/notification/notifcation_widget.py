from ignis.services.notifications import Notification
from ignis.utils import Utils
from ignis.widgets import Widget
from modules.common import truncate_label


class NormalLayout(Widget.Box):
    def __init__(self, notification: Notification) -> None:
        self.icon = Widget.Icon(
            image=(
                notification.icon
                if notification.icon
                else "dialog-information-symbolic"
            ),
            pixel_size=48,
            halign="end",
            valign="center",
        )

        self.detail = Widget.Box(
            vertical=True,
            css_classes=["ml-7"],
            child=[
                Widget.Label(
                    label=truncate_label(notification.summary, max_len=30),
                    halign="start",
                    visible=notification.summary != "",
                    css_classes=["txt-lg", "bold"],
                ),
                Widget.Label(
                    label=truncate_label(notification.body, max_len=30),
                    halign="start",
                    css_classes=["txt-2"],
                    visible=notification.body != "",
                ),
            ],
        )

        super().__init__(
            vertical=True,
            hexpand=True,
            child=[
                Widget.Box(
                    hexpand=True,
                    child=[
                        self.icon,
                        self.detail,
                    ],
                ),
                Widget.Box(
                    child=[
                        Widget.Button(
                            child=Widget.Label(label=action.label),
                            on_click=lambda x, action=action: action.invoke(),
                            css_classes=["notification-action"],
                        )
                        for action in notification.actions
                    ],
                    homogeneous=True,
                    style="margin-top: 0.75rem;" if notification.actions else "",
                    spacing=10,
                ),
            ],
        )


class NotificationWidget(Widget.Box):
    def __init__(self, notification: Notification) -> None:
        layout = NormalLayout(notification)
        super().__init__(
            css_classes=["notification"],
            child=[layout],
        )
