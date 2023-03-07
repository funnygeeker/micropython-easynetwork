# EasyNetwork https://github.com/funnygeeker/micropython-easynetwork
# 参考资料：https://docs.micropython.org/en/v1.9.3/esp8266/library/network.html

import time
import network


class AP:
    def __init__(self):
        self.wlan = network.WLAN(network.AP_IF)  # 指定用ap模式

    def create(self, essid: str,
               password: str = '',
               authmode: int = None,
               hidden: int = 0,
               channel: int = 0,
               dhcp_hostname: str = 'EasyNetwork'):
        """
        创建一个 AP

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
                authmode = 4
            else:
                authmode = 0
        self.wlan.active(True)  # 启用wifi前需要先激活接口
        self.wlan.config(essid=essid, password=password, authmode=authmode, hidden=hidden, channel=channel,
                         dhcp_hostname=dhcp_hostname)  # 设置热点

    def close(self):
        """
        关闭 AP
        """
        self.wlan.active(False)


class Client:
    def __init__(self, delay: int = 1000, retry: int = 10):
        self.wlan = network.WLAN(network.STA_IF)
        self.delay = delay
        self.retry = retry

    def scan(self) -> list:
        """
        扫描无线网络

        Returns:
            List[Tuple[Union[bytes, int, bool]]]
            [(ssid, bssid, channel, RSSI, authmode, hidden), ...]
        """
        if not self.wlan.active():
            self.wlan.active(True)
            result = self.wlan.scan()
            self.wlan.active(False)
            return result
        else:
            return self.wlan.scan()

    def connect(self, ssid: str, password: str = None):
        """
        连接无线网络

        Args:
            ssid: 无线网络名称
            password: 无线网络密码

        Returns:
            Tuple[str]: 连接成功或已连接，网络连接信息
            None: 连接失败
        """
        if not self.wlan.isconnected():
            self.wlan.active(True)  # 开启wifi接口
            self.wlan.connect(ssid, password)
            for i in range(self.retry):
                if self.wlan.isconnected():  # 网络是否已连接
                    return self.wlan.ifconfig()  # 输出当前 wifi 网络给自己分配的网络参数
                    # ('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')
                else:
                    print("[WARN] Wireless network connection failed, Trying again({}/{})".format(
                        i + 1, self.retry)
                    )
                    time.sleep_ms(self.delay)
            self.wlan.disconnect()
            self.wlan.active(False)  # 关闭wifi接口
            print("[ERROR] Wireless network connection failed, please check the network configuration!")
            return False
        else:
            return self.wlan.ifconfig()

    def disconnect(self) -> bool:
        """
        断开连接的网络

        Returns:
            True: 操作成功
            False: 未连接网络
        """
        if self.wlan.isconnected():  # 如果连接了网络则断开连接
            self.wlan.disconnect()
            self.wlan.active(False)  # 关闭wifi接口
            return True
        else:
            return False
