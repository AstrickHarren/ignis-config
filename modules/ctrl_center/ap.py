from typing import Callable, override

from gi.repository import NM  # type: ignore
from gi.repository import GLib, GObject  # type: ignore

from ignis.services.network import WifiAccessPoint


class Ap(WifiAccessPoint):
    def __init__(
        self,
        ap: WifiAccessPoint,
        conn: NM.RemoteConnection | None = None,
        on_conn_fail: Callable | None = None,
    ):
        super().__init__(ap._point, ap._client, ap._device)
        self.conn = conn
        self.on_conn_fail = on_conn_fail

    def is_saved(self) -> bool:
        return self.conn is not None

    def on_fail(self):
        def delete_conn_by_name(name: str):
            conns = self._client.get_connections()
            conns = [conn for conn in conns if conn.get_id() == name]
            for conn in conns:
                conn.delete_async(None, lambda _, r: conn.delete_finish(r))

        delete_conn_by_name(self.ssid)  # type: ignore
        self.conn = None
        self.on_conn_fail() if self.on_conn_fail else None
        print(f"deleting conn {self.ssid}")

    def connect_to(self, password: str | None = None) -> None:
        def finish(x, res):
            self._client.activate_connection_finish(res)
            ap = self._device.get_active_access_point()
            if ap is not None:
                ssid = ap.get_ssid().get_data().decode("utf-8")
                if ssid == self.ssid:
                    print(
                        f"connection successfully to {ap.get_ssid().get_data().decode("utf-8")}"
                    )
                    return
            print(f"connection failed, most likely incorrect psk")
            self.on_fail()

        if self.conn is not None:
            print("connecting with saved config")
            self._client.activate_connection_async(
                self.conn, self._device, None, None, finish
            )
            return
        if password is not None:
            print("connecting with psk")
            self.save_and_connect_to(password)
            return
        print("unreachable: cannot connect w/o psk")

    def save_and_connect_to(self, password: str | None = None) -> None:
        """
        Connect to this access point.

        Args
            password: Password to use. This has an effect only if the access point requires a password.
        """
        connection = NM.RemoteConnection()

        # WiFi settings
        wifi_setting = NM.SettingWireless.new()
        wifi_setting.props.ssid = GLib.Bytes.new(self.ssid.encode("utf-8"))
        connection.add_setting(wifi_setting)

        # WiFi security settings
        if self.security:
            wifi_sec_setting = NM.SettingWirelessSecurity.new()
            wifi_sec_setting.set_property("key-mgmt", "wpa-psk")
            wifi_sec_setting.set_property("psk", password)
            connection.add_setting(wifi_sec_setting)

        # IP4 settings
        ip4_setting = NM.SettingIP4Config.new()
        ip4_setting.set_property("method", "auto")
        connection.add_setting(ip4_setting)

        # IP6 settings
        ip6_setting = NM.SettingIP6Config.new()
        ip6_setting.set_property("method", "auto")
        connection.add_setting(ip6_setting)

        # Connection settings
        connection_setting = NM.SettingConnection.new()
        connection_setting.set_property("id", self.ssid)
        connection_setting.set_property("type", "802-11-wireless")
        connection_setting.set_property("uuid", NM.utils_uuid_generate())
        connection_setting.set_property("interface-name", self._device.get_iface())
        connection.add_setting(connection_setting)

        # Proxy settings
        proxy_setting = NM.SettingProxy.new()
        connection.add_setting(proxy_setting)

        def finish(_, res) -> None:
            try:
                self._client.add_and_activate_connection_finish(res)
                ap = self._device.get_active_access_point()
                if ap is not None:
                    ssid = ap.get_ssid().get_data().decode("utf-8")
                    if ssid == self.ssid:
                        print(
                            f"connection successfully to {ap.get_ssid().get_data().decode("utf-8")}"
                        )
                        return
                print(f"connection failed, most likely incorrect psk")
            except Exception as e:
                print(f"connection failed :{e}")
            finally:
                self.on_fail()

        self._client.add_and_activate_connection_async(
            connection,
            self._device,
            self._point.get_path(),
            None,
            finish,
        )
