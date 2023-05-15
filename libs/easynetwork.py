# EasyNetwork https://github.com/funnygeeker/micropython-easynetwork
# 参考资料：https://docs.micropython.org/en/v1.9.3/esp8266/library/network.html

import network


class AP:
    def __init__(self):
        self.ssid = None
        self.password = None
        self.wlan = network.WLAN(network.AP_IF)  # 指定用ap模式

    def create(self, essid: str,
               password: str = '',
               authmode: int = None,
               hidden: int = 0,
               channel: int = 0,
               dhcp_hostname: str = 'EasyNetwork'):
        """
        创建一个 AP，网关默认为 192.168.4.1

        Args:
            essid: 热点名称
            password: 连接密码（需大于八位）
            authmode: 认证模式（不填写则自动管理）
                0 - 无密码
                1 - WEP认证
                2 - WPA-PSK
                3 - WPA2-PSK
                4 - WPA/WPA2-PSK
            hidden: 是否隐藏
            channel: wifi信道
            dhcp_hostname: DHCP主机名
        """
        if authmode is None:
            if password:
                if len(password) >= 8:
                    authmode = 4
                else:
                    authmode = 0
                    print('[ERROR] The password length should not be less than 8.')
            else:
                authmode = 0
        self.ssid = essid
        self.password = password
        self.wlan.active(True)  # 启用wifi前需要先激活接口
        self.wlan.config(essid=essid, password=password, authmode=authmode, hidden=hidden, channel=channel,
                         dhcp_hostname=dhcp_hostname)  # 设置热点

    def close(self):
        """
        关闭 AP
        """
        self.ssid = None
        self.password = None
        self.wlan.active(False)


class Client:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.ssid = None
        self.password = None

    def scan(self) -> list:
        """
        扫描附件无线网络

        Returns:
            List[Tuple[Union[bytes, int, bool]]]
            [(ssid, bssid, channel, RSSI, authmode, hidden), ...]
        """
        if not self.wlan.active():  # wlan 不常用时尽量减小功耗
            self.wlan.active(True)
            result = self.wlan.scan()
            self.wlan.active(False)
            return result
        else:
            return self.wlan.scan()

    def status(self):
        """
        获取网络连接状态

        Returns:
            str
        """
        result = self.wlan.status()
        if result == network.STAT_IDLE:
            return 'not_connected'
        elif result == network.STAT_CONNECTING:
            return 'connecting'
        elif result == network.STAT_GOT_IP:
            return 'connected'
        elif result == network.STAT_NO_AP_FOUND:
            return 'no_ap_found'
        elif result == network.STAT_WRONG_PASSWORD:
            return 'wrong_password'
        elif result == network.STAT_ASSOC_FAIL:
            return 'assoc_fail'
        elif result == network.HANDSHAKE_TIMEOUT:
            return 'handshake_timeout'
        else:
            return 'unknown'
        
    def connect(self, ssid: str, password: str = None):
        """
        连接无线网络

        Args:
            ssid: 无线网络名称
            password: 无线网络密码

        Returns:
            Tuple[str]: 已连接，网络连接信息
            True: 操作成功
            None: 运行出错
        """
        if not self.wlan.isconnected() or self.ssid != ssid:
            if self.ssid != ssid:
                self.disconnect()
            self.wlan.active(True)  # 开启wifi接口
            if password and len(password) < 8:
                print("[ERROR] The password length should not be less than 8.")
                return None
            try:
                self.ssid = ssid
                self.password = password
                self.wlan.connect(ssid, password)
                return True
            except OSError:
                print("[ERROR] Wireless network connection failed, please check the wireless network!")
                self.ssid = None
                self.password = None
                return None
        else:
            return self.wlan.ifconfig()

    def ifconfig(self):
        """
        获取已连接网络的 IP，子网掩码，网关，DNS（未连接时 IP 为 '0.0.0.0'）

        Returns:
            Tuple[str]
        """
        return self.wlan.ifconfig()

    def isconnected(self) -> bool:
        """
        网络是否已连接

        Returns:
            True: 已连接
            False: 未连接
        """
        return self.wlan.isconnected()

    def disconnect(self):
        """
        断开连接的网络
        """
        if self.wlan.active():
            self.wlan.disconnect()
            self.wlan.active(False)  # 关闭wifi接口
            self.ssid = None
            self.password = None