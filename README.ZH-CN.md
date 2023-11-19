[English (英语)](./README.md)
# micropython-easynetwork
更简单地接入和管理 `micropython` 的 `WLAN` 网络

![EasyNetwork](./EasyNetwork_256px.png)
### 说明
基于原版 `network` 简化了部分繁琐的操作，比如：
- 查询原版文档有些不方便，不过，这些文档都被整理到了代码注释
- 部分功能使用前需要 `active(True)`，但是现在只需要直接执行即可，程序会自动判断
- 作为 `Client`：在已经连接 `WLAN` 的情况下，如果直接连接其他的 `WLAN` 会报错，现在，你只需要直接 `connect('ssid','password')`切换网络即可
- 作为 `AP`：使用加密 `ssid`，则必须先设置 `key` 再设置 `security`。现在，你只需要直接设置 `ssid` 和 `key`。

### 固件版本要求
- `micropython 1.20 +`

### 使用示例
```python
# 示例：创建 AP #
from libs.easynetwork import AP

# 创建AP
ap = AP()
ap.config(ssid='ssid', key='password')  # SSID 为 WIFI 名称，key 为密码，不填写密码则为开放网络，填写自动设置为加密网络
ap.config(key='password2')  # 修改密码
ap.config(key='')  # 禁用密码
ap.active(False)  # 关闭AP

# 示例：连接网络 #
from libs.easynetwork import Client
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
```
