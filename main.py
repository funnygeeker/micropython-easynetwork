# 示例：创建 AP #
from lib.easynetwork import AP

# 创建AP
ap = AP()
ap.config(ssid='ssid', key='password')  # SSID 为 WIFI 名称，key 为密码，不填写密码则为开放网络，填写自动设置为加密网络
ap.config(key='password2')  # 修改密码
ap.config(key='')  # 禁用密码
ap.active(True)  # 启用AP
ap.active(False)  # 关闭AP

# 示例：连接网络 #
from lib.easynetwork import Client
client = Client()

# 扫描无线网络（此处为示例，实际连接时按需使用）
print(client.scan())

# [(b'QWERTY', b'\xfc\xa0Z\x03\r\xf6', 6, -29, 4, False), (b'UIOP_2G', b'\x94\x83\xc4"(\xf5', 6, -30, 3, False)]
client.connect('ssid', 'password')  # 开放网络无需填写密码参数，或者密码为空

# 检查网络是否已连接
print(client.isconnected())
# True

# 断开网络
client.disconnect()