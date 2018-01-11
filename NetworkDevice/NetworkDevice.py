from PyTango import AttrQuality, AttrWriteType, DevState, DispLevel, AttrWriteType
from PyTango.server import Device, DeviceMeta, command, attribute, device_property, run


import platform
import os
from socket import socket, AF_INET, SOCK_STREAM, setdefaulttimeout

setdefaulttimeout(.5)

class NetworkDevice(Device, metaclass=DeviceMeta):
    online = attribute(label="Online", dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ,
            unit="",
            doc="Device responds to ICMP ping")

    host = device_property(dtype=str, default_value="192.168.0.1")

    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.STANDBY)
        self.__online = False

    def read_online(self):
        res = ping(self.host)
        self.__online = res
        return self.__online

    @command
    def TurnOn(self):
        self.set_state(DevState.ON)
    @command
    def TurnOff(self):
        self.set_state(DevState.OFF)

def ping(host):
    """
    Returns True if host responds to a ping request
    """

    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"

    # Ping
    return os.system("ping " + ping_str + " " + host) == 0

def test_port(host, port):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect( (host, port))
        return True
    except Exception as exc:
        return False


if __name__ == "__main__":
    run([NetworkDevice,])
