#encoding:utf-8
import time
import numpy

from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from PyTango.server import Device, DeviceMeta, attribute, command, run
from PyTango.server import device_property

from pyModbusTCP.client import ModbusClient
import logging

logger = logging.getLogger(__name__)
host = "192.168.0.23"
port = 502
unit_id = 101

U_WORD=1
S_WORD=1
UD_WORD=2
SD_WORD=2

def get_UD_WORDs(data):
    """gets a two elements array/list and returns bitwise sum [12,23]"""
    result = []
    while(data):
        result.append(data.pop(0) << 16 | data.pop(0))
    return result

class NEMOD4Le(Device, metaclass=DeviceMeta):

    L1 = attribute(label="L1", dtype = float,
                   display_level=DispLevel.OPERATOR,
                   access=AttrWriteType.READ,
                   unit="V", format="4,2f",
                   doc="L1 Voltage")
    L2 = attribute(label="L2", dtype = float,
                   display_level=DispLevel.OPERATOR,
                   access=AttrWriteType.READ,
                   unit="V", format="4,2f",
                   doc="L2 Voltage")
    L3 = attribute(label="L3", dtype = float,
                   display_level=DispLevel.OPERATOR,
                   access=AttrWriteType.READ,
                   unit="V", format="4,2f",
                   doc="L3 Voltage")
    I1 = attribute(label="I1", dtype = float,
                   display_level=DispLevel.OPERATOR,
                   access=AttrWriteType.READ,
                   unit="A", format="4,2f",
                   doc="I1 Current")
    I2 = attribute(label="I2", dtype = float,
                   display_level=DispLevel.OPERATOR,
                   access=AttrWriteType.READ,
                   unit="A", format="4,2f",
                   doc="I2 Current")
    I3 = attribute(label="I3", dtype = float,
                   display_level=DispLevel.OPERATOR,
                   access=AttrWriteType.READ,
                   unit="A", format="4,2f",
                   doc="I3 Current")



    host = device_property(dtype=str, default_value="192.168.0.23")
    port = device_property(dtype=int, default_value = 502)
    id = device_property(dtype=int, default_value = 100)

    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.STANDBY)

    def modbus_register(self, register, size):
        print("checking state")
        if self.get_state() == DevState.ON:
            print("devstate on")
            try:
                c = ModbusClient(host=self.host, port=self.port, unit_id=self.id)
                c.open()
                print("c is open")
                if c.is_open():
                    regs = c.read_holding_registers(register, size)
                    #regs = c.read_holding_registers(0x1000, UD_WORD*6)
                else:
                    self.error_stream("Connection not open")
                #return regs[0], time.time(), AttrQuality.ATTR_WARNING
                print(regs)
                a = get_UD_WORDs(regs)
                print(a)
                return int(a[0])#, time.time(), AttrQuality.ATTR_WARNING
            except Exception as exc:
                self.error_stream("Exception reading registe4r {} {}".format(register, exc))

    def read_L1(self):
        return self.modbus_register(0x1000, UD_WORD*2)
    def read_L2(self):
        return self.modbus_register(0x1002, UD_WORD*2)
    def read_L3(self):
        return self.modbus_register(0x1004, UD_WORD*2)
    def read_I1(self):
        return self.modbus_register(0x1006, UD_WORD*2)
    def read_I2(self):
        return self.modbus_register(0x1008, UD_WORD*2)
    def read_I3(self):
        return self.modbus_register(0x100a, UD_WORD*2)

    def read_all(self):
        if self.state == DevState.ON:
            pass
    @command
    def TurnOn(self):
        self.set_state(DevState.ON)
    @command
    def TurnOff(self):
        self.set_state(DevState.OFF)


if __name__ == "__main__":
    run([NEMOD4Le,])

