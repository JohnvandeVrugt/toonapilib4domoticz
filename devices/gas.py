import Domoticz
from devices.configuration import config
from devices.device import Device
from devices.device import DeviceCreateException
from devices.device import DeviceUpdateException


class DeviceGas(Device):
    domoticz_device_type = 251
    domoticz_subtype = 2

    def __init__(self, plugin_devices, toon, debug):
        super().__init__(config.STR_UNIT_GAS,
                         config.STD_UNIT_GAS,
                         plugin_devices,
                         toon,
                         debug)

    def create(self):
        if not self.exists:
            try:
                Domoticz.Log("Creating gas usage device " + self.name)
                Domoticz.Device(Name=self.name, Unit=self.unit, Type=self.domoticz_device_type,
                                Subtype=self.domoticz_subtype).Create()

            except DeviceCreateException as ex:
                Domoticz.Log("An error occurred creating " + self.name)
                Domoticz.Log("Exception: " + str(ex))
        elif self.debug:
            Domoticz.Log("Unit " + str(self.unit) + " exists - nothing to do")
        return self

    def update(self):
        super().update()
        str_value = ""

        try:
            str_value = str(self.toon.gas.daily_usage)

            if str_value != self.previous_value:
                if self.debug:
                    Domoticz.Log("Update gas usage: " + str_value)
                self.plugin_devices[self.unit].Update(0, str_value)

        except DeviceUpdateException as ex:
            Domoticz.Log("An error occurred updating " + self.name)
            Domoticz.Log("Exception: " + str(ex))

        self.set_previous_value(str_value)
