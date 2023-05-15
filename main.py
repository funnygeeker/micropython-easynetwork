# 示例：创建 AP #
from libs.easynetwork import AP

# 创建AP
ap = AP()
ap.create('WIFI_SSID', 'password')  # SSID 为 WIFI 名，password 为密码，不填写密码则为开放网络

# 关闭AP
ap.close()

# 示例：连接网络 #
from libs.easynetwork import Client
client = Client()
client.connect('WIFI_SSID', 'password')  # SSID 为 WIFI 名，password 为密码，开放网络无需填写密码参数

# 扫描无线网络（此处为示例，实际连接时按需使用）
print(client.scan())
# [(b'QWERTY', b'\xfc\xa0Z\x03\r\xf6', 6, -29, 4, False), (b'UIOP_2G', b'\x94\x83\xc4"(\xf5', 6, -30, 3, False)]

# 检查网络是否已连接
print(client.isconnected())
# True

# 断开网络
client.disconnect()

# 其他详细参数详见源码，随便写的库，只是希望调用时方便一点（）
