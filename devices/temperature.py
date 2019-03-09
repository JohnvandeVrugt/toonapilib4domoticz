import Domoticz
from devices.device import Device
from devices.device import DeviceCreateException
from devices.device import DeviceUpdateException


class DeviceTemperature(Device):
    domoticz_device_type = 80
    domoticz_subtype = 5

    def __init__(self, name, unit, devices, toon, debug):
        super().__init__(name, unit, devices, toon, debug)

    def create(self):
        if not super().exists:
            try:
                Domoticz.Log("Creating temperature device " + super().name)
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
            str_value = str(self.toon.temperature)

            if str_value != self.previous_value:
                if self.debug:
                    Domoticz.Log("Update temperature: " + str_value)
                self.devices[self.unit].Update(0, str_value)

        except DeviceUpdateException as ex:
            Domoticz.Log("An error occurred updating " + self.name)
            Domoticz.Log("Exception: " + str(ex))

        self.set_previous_value(str_value)
