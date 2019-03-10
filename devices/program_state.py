import Domoticz
from devices.device import Device
from devices.device import DeviceCreateException
from devices.device import DeviceCommandException
from devices.device import DeviceUpdateException


class DeviceProgramState(Device):
    domoticz_device_type = 244,
    domoticz_subtype = 62,
    domoticz_switch_type = 0,
    domoticz_image = 9

    def __init__(self, name, unit, devices, toon, debug):
        super().__init__(name, unit, devices, toon, debug)

    def create(self):
        if not self.exists:
            try:
                Domoticz.Log("Creating program state device " + self.name)
                Domoticz.Device(Name=super().name, Unit=super().unit, Type=self.domoticz_device_type,
                                Subtype=self.domoticz_subtype, Switchtype=self.domoticz_switch_type,
                                Image=self.domoticz_image).Create()

            except DeviceCreateException as ex:
                Domoticz.Log("An error occurred creating " + self.name)
                Domoticz.Log("Exception: " + str(ex))
        elif self.debug:
            Domoticz.Log("Unit " + str(self.unit) + " exists - nothing to do")
        return self

    def on_command(self, unit, command, level, hue):
        try:
            str_program_state = str(command).lower()
            super().toon.program_state = str_program_state

            program_state = 0
            if str_program_state != "off":
                program_state = 1

            if self.debug:
                Domoticz.Log("set program state " + str_program_state + " - " + str(program_state))

            super().devices[super().unit].Update(program_state, str(program_state))

        except DeviceCommandException as ex:
            Domoticz.Log("An error occurred setting " + self.name)
            Domoticz.Log("Exception: " + str(ex))

    def update(self):
        super().update()
        str_value = ""

        try:
            program_state = 0
            if super().toon.program_state != "off":
                program_state = 1

            str_value = str(program_state)

            if str_value != super().previous_value:
                if self.debug:
                    Domoticz.Log("Update program state: " + str_value)
                super().devices[super().unit].Update(program_state, str_value)

        except DeviceUpdateException as ex:
            Domoticz.Log("An error occurred updating " + super().name)
            Domoticz.Log("Exception: " + str(ex))

        super().set_previous_value(str_value)
