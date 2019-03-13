import Domoticz
from devices.configuration import config
from devices.device import Device
from devices.device import DeviceCreateException
from devices.device import DeviceCommandException
from devices.device import DeviceUpdateException


class DeviceSetPoint(Device):
    domoticz_device_type = 242
    domoticz_subtype = 1

    def __init__(self, plugin_devices, toon, debug):
        super().__init__(config.STR_UNIT_SET_POINT,
                         config.STD_UNIT_SET_POINT,
                         plugin_devices,
                         toon,
                         debug)

    def create(self):
        if not self.exists:
            try:
                Domoticz.Log("Creating set point device " + self.name)
                Domoticz.Device(Name=self.name, Unit=self.unit, Type=self.domoticz_device_type,
                                Subtype=self.domoticz_subtype).Create()

            except DeviceCreateException as ex:
                Domoticz.Log("An error occurred creating " + self.name)
                Domoticz.Log("Exception: " + str(ex))
        elif self.debug:
            Domoticz.Log("Unit " + str(self.unit) + " exists - nothing to do")
        return self

    def on_command(self, unit, command, level, hue):
        try:
            self.toon.thermostat = level
            if self.debug:
                Domoticz.Log("set set point " + str(level))
            self.plugin_devices[unit].Update(0, str(level))

        except DeviceCommandException as ex:
            Domoticz.Log("An error occurred setting " + self.name)
            Domoticz.Log("Exception: " + str(ex))

    def update(self):
        super().update()
        str_value = ""

        try:
            str_value = str(self.toon.thermostat)

            if str_value != self.previous_value:
                if self.debug:
                    Domoticz.Log("Update set point: " + str_value)
                self.plugin_devices[self.unit].Update(0, str_value)

        except DeviceUpdateException as ex:
            Domoticz.Log("An error occurred updating " + self.name)
            Domoticz.Log("Exception: " + str(ex))

        self.set_previous_value(str_value)
