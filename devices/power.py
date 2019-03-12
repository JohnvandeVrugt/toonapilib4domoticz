import Domoticz
from devices.device import Device
from devices.device import DeviceCreateException
from devices.device import DeviceUpdateException


class DevicePower(Device):
    domoticz_device_type = 250
    domoticz_subtype = 1

    def __init__(self, name, unit, plugin_devices, toon, debug):
        super().__init__(name, unit, plugin_devices, toon, debug)

    def create(self):
        if not self.exists:
            try:
                Domoticz.Log("Creating power usage device " + self.name)
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
            str_value = "{0};{1};{2};{3};{4};{5}".format(self.toon.power.meter_reading_low,
                                                         self.toon.power.meter_reading,
                                                         self.toon.solar.meter_reading_low_produced,
                                                         self.toon.solar.meter_reading_produced,
                                                         self.toon.power.value, self.toon.solar.value)
            if str_value != self.previous_value:
                if self.debug:
                    Domoticz.Log("Update power/solar usage: " + str_value)
                self.plugin_devices[self.unit].Update(0, str_value)

        except DeviceUpdateException as ex:
            Domoticz.Log("An error occurred updating " + super().name)
            Domoticz.Log("Exception: " + str(ex))

        self.set_previous_value(str_value)
