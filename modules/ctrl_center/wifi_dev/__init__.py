from typing import override

from gi.repository import GObject  # type: ignore

from ignis.gobject import IgnisGObject
from ignis.services.network import WifiAccessPoint as IgnisWifiAccessPoint
from ignis.services.network import WifiDevice as IgnisWifiDevice
from ignis.variable import Variable


class RemoteConn(IgnisGObject):
    def __init__(self, conn, dev) -> None:
        super().__init__()
        self._conn = conn
        self._device = dev._device
        self._client = dev._client
        self._dev = dev
        self._ssid = self._conn.get_id()

    def on_ok(self):
        print(f"successfully connected to {self._ssid}")

    def on_err(self):
        self._conn.delete_async(None, lambda _, r: self._conn.delete_finish(r))
        print(f"failed to connect to {self._ssid} deleting saved config")

    def connect_to(self):
        self._dev.connecting_to = self
        self._client.activate_connection_async(
            self._conn,
            self._device,
            None,
            None,
            lambda x, res: self._client.activate_connection_finish(res),
        )


class WifiAccessPoint(IgnisWifiAccessPoint):
    def __init__(self, point, dev):
        super().__init__(point, dev._client, dev._device)
        self._dev = dev

    def saved_conn(self):
        known_conns = self._device.get_available_connections()
        for conn in known_conns:
            if conn.get_id() == self.ssid:
                return RemoteConn(conn, self._dev)
        return None

    def on_ok(self):
        print(f"successfully connected to {self._ssid}")

    def on_err(self):
        conn = self.saved_conn()
        if conn is not None:
            conn.on_err()

    def connect_with_password(self, password: str | None = None) -> None:
        self._dev.connecting_to = self
        super().connect_to(password)


class WifiDevice(IgnisWifiDevice):
    def __init__(self, dev, pause_scan=Variable(False)):
        super().__init__(dev._device, dev._client)
        self.connecting_to = None
        self.pending_notification = False
        self.pause_scan = pause_scan
        pause_scan.connect("notify::value", lambda x, y: self.notify_pending())

    @GObject.Property
    def state(self):
        state = super().state
        if not self.connecting_to:
            return state

        if state == "activated":
            self.connecting_to.on_ok()
            self.connecting_to = None
        if state in ["failed", "disconnected"]:
            self.connecting_to.on_err()
            self.connecting_to = None

        return state

    @GObject.Property
    def access_points(self) -> list[IgnisWifiAccessPoint]:
        """
        - read-only

        A list of access points (Wi-FI networks).
        """
        aps = self._device.get_access_points()
        return [WifiAccessPoint(ap, self) for ap in aps]

    def notify_pending(self):
        if not self.pause_scan.value and self.pending_notification:
            print("flushing notification")
            self.notify("access_points")
            self.pending_notification = False

    @override
    def __add_access_point(self, _, ap, emit=True):
        if emit and not self.pause_scan.value:
            print("notifying access_points")
            self.notify("access-points")
            self.pending_notification = False
        elif emit:
            print("notification pending")
            self.pending_notification = True

    def __remove_access_point(self, device, ap):
        if not self.pause_scan.value:
            self.notify("access-points")
            self.pending_notification = False
        else:
            print("notification pending")
            self.pending_notification = True
