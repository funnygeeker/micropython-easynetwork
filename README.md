[简体中文 (Chinese)](./README.ZH-CN.md)
# micropython-easynetwork

Simplified access and management of WLAN networks in Micropython.

![EasyNetwork](./EasyNetwork_256px.png)

### Description

Based on the original `network` module, this library simplifies some of the cumbersome operations, such as:

- Documentation for the original module can be inconvenient to access, but with this library, the documentation is included as code comments.
- Prior to using certain features, the original module requires calling `active(True)`. Now, with this library, it's not necessary as the program will automatically handle it.
- As a client: Previously, when connected to a WLAN network, attempting to connect to another network would result in an error. The library simplifies this process by allowing direct switching of networks using `connect('ssid', 'password')`.
- As an access point (AP): When using an encrypted SSID, the original module required setting the `key` before setting the `security`. However, with this library, it's possible to directly set the `ssid` and `key`.

### Firmware Version Requirement

- Micropython 1.20 or higher

### Usage Example

```python
# Example: Creating an access point (AP) #
from libs.easynetwork import AP

# Create an AP
ap = AP()
ap.config(ssid='ssid', key='password')  # SSID is the network name, key is the password. If no password is provided, the network is open. If password is specified, it is automatically set as an encrypted network.
ap.config(key='password2')  # Change the password
ap.config(key='')  # Disable the password
ap.active(False)  # Disable the AP

# Example: Connecting to a network #
from libs.easynetwork import Client

# Scan for wireless networks (example)
print(client.scan())

# [(b'QWERTY', b'\xfc\xa0Z\x03\r\xf6', 6, -29, 4, False), (b'UIOP_2G', b'\x94\x83\xc4"(\xf5', 6, -30, 3, False)
client.connect('ssid', 'password')  # For an open network, no password parameter is required or password can be left empty.

# Check if the network is connected
print(client.isconnected())
# True

# Disconnect from the network
client.disconnect()
```