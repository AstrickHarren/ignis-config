# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false, reportFunctionMemberAccess=false

from ignis.services.audio import AudioService
from ignis.services.network import NetworkService
from ignis.services.notifications import NotificationService
from ignis.services.recorder import RecorderService
from ignis.widgets import Widget

network = NetworkService.get_default()
notifications = NotificationService.get_default()
recorder = RecorderService.get_default()
audio = AudioService.get_default()


def indicator_icon(**kwargs):
    return Widget.Icon(
        style="padding-bottom: 0.00rem;", css_classes=["px-2", "ml-3", "mr-2"], **kwargs
    )


def wifi_icon():
    def check_visible(*args) -> bool:
        if len(network.wifi.devices) > 0:
            if network.ethernet.is_connected:
                if network.wifi.is_connected:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    icon = indicator_icon(image=network.wifi.bind("icon-name"))
    icon.visible = network.wifi.bind("devices", check_visible)
    icon.visible = network.ethernet.bind("is_connected", check_visible)
    icon.visible = network.wifi.bind("is_connected", check_visible)
    return icon


def ethernet_icon():
    def check_visible(*args) -> bool:
        if len(network.ethernet.devices) > 0:
            if network.wifi.is_connected:
                if network.ethernet.is_connected:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    icon = indicator_icon(image=network.ethernet.bind("icon_name"))
    icon.visible = network.ethernet.bind("devices", check_visible)
    icon.visible = network.wifi.bind("is_connected", check_visible)
    icon.visible = network.ethernet.bind("is_connected", check_visible)
    return icon


def dnd_icon():
    return indicator_icon(
        image="notification-disabled-symbolic",
        visible=notifications.bind("dnd"),
    )


def recorder_icon():
    def check_state(icon: Widget.Icon) -> None:
        if recorder.is_paused:
            icon.remove_css_class("active")
        else:
            icon.add_css_class("active")

    icon = indicator_icon(
        image="media-record-symbolic",
        visible=recorder.bind("active"),
    )

    icon.add_css_class("record-indicator")

    recorder.connect("notify::is-paused", lambda x, y: check_state(icon))

    return icon


def volume_icon():
    return indicator_icon(
        image=audio.speaker.bind("icon_name"),
    )
