import time
import numpy

from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from PyTango.server import Device, DeviceMeta, attribute, command, run
from PyTango.server import device_property

from pyModbusTCP.client import ModbusClient

port = 502


class MRDIO(Device, metaclass=DeviceMeta):
    host = device_property(dtype=str, default_value="192.168.0.11")
    port = device_property(dtype=int, default_value = 502)
    modbus_id = device_property(dtype=int, default_value = 70)
    min_polling_time = device_property(dtype=float, devault_value = 1)
    last_input_read = 0

    IN_1 = attribute(label="IN_1",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ,
            docs="Input number 1 on pin D1")
    IN_2 = attribute(label="IN_2",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ,
            docs="Input number 2 on pin D2")
    IN_3 = attribute(label="IN_3",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ,
            docs="Input number 3 on pin D3")
    IN_4 = attribute(label="IN_4",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ,
            docs="Input number 4 on pin D4")
    IN_5 = attribute(label="IN_5",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ,
            docs="Input number 5 on pin D5")
    IN_6 = attribute(label="IN_6",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ,
            docs="Input number 6 on pin D6")
    OUT_1 = attribute(label="OUT_1",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ_WRITE,
            docs="Output number 1 on pin D1")
    OUT_2 = attribute(label="OUT_2",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ_WRITE,
            docs="Output number 2 on pin D2")
    OUT_3 = attribute(label="OUT_3",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ_WRITE,
            docs="Output number 3 on pin D3")
    OUT_4 = attribute(label="OUT_4",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ_WRITE,
            docs="Output number 4 on pin D4")
    OUT_5 = attribute(label="OUT_5",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ_WRITE,
            docs="Output number 5 on pin D5")
    OUT_6 = attribute(label="OUT_6",
            dtype=bool,
            display_level=DispLevel.OPERATOR,
            access=AttrWriteType.READ_WRITE,
            docs="Output number 6 on pin D6")

    self.init_device(self):
        Device.init_device(self)
        self.debug_stream("In init_device()")
        self.cl = ModbusClient(self.host, self.port, self.modbus_id)
        self.cl.timeout(.5)
        self.last_read_time=time.time()

    @command
    self.TurnON(self):
        self.set_state(DevState.ON)

    @command
    self.TurnOFF(self):
        self.set_state(DevState.OFF)

    self.read_ALL(self):
        if (time.time()>last_read_time+min_polling_time):
            last_read_time = time.time() 
            if self.get_state() == DevState.ON:
                self.cl.open()
                if self.cl.isopen():
                    try:
                        IN_1, IN_2, IN_3, IN_4, IN_5, IN_6 = cl.read_discrete_inputs(4000, 6)
                    except Exception as exc:
                        self.error_stream("Exception trying to connect {}".format(exc))
                        return None
                else:
                    self.error_stream("Error trying to connect")
                    return None
                self.cl.close()
        else:
            # is not necessary to make a read as data is updated
            pass
    self.read_IN_1(self):
        return IN_2

    self.read_IN_2(self):
        return IN_2

    self.read_IN_3(self):
        return IN_3

    self.read_IN_4(self):
        return IN_4

    self._write_modbus(self, index, value):
        self.cl.open()
        if self.cl.isopen():
            try:
                cl.write_single_coil(4000+index, [value])
            except Exception as exc:
                self.error_stream("Exception trying to connect {}".format(exc))
                return None
        else:
            self.error_stream("Error trying to connect")
            return None
        self.cl.close()

    self.set_OUT_1(self, value):
        return self._write_modbus(0, value)










    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.STANDBY)
    def 
