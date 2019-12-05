import Domoticz
from devices.configuration import config
from devices.device import Device
from devices.device import DeviceCreateException
from devices.device import DeviceCommandException
from devices.device import DeviceUpdateException




class DeviceLightState(Device):
    domoticz_device_type = 244
    domoticz_subtype = 73
    domoticz_switch_type = 0
    domoticz_image = 0
    _huelight = None

    def __init__(self, plugin_devices, toon, light):
        self._huelight = light
        super().__init__(self._huelight.name,
                         config.STD_UNIT_LIGHT_START_STATE + self._huelight.zwave_index,
                         plugin_devices,
                         toon)

    def create(self, light):
        if not self.exists:
            try:
                Domoticz.Log("Creating HueLight '" + self.name + "'")
                Domoticz.Device(Name=self.name, Unit=self.unit, Type=self.domoticz_device_type,
                                Subtype=self.domoticz_subtype, Switchtype=self.domoticz_switch_type,
                                Image=self.domoticz_image).Create()

            except DeviceCreateException as ex:
                Domoticz.Log("An error occurred creating HueLight '" + self.name + "'")
                Domoticz.Log("Exception: " + str(ex))
        elif config.debug:
            Domoticz.Log("Unit " + str(self.unit) + " exists - nothing to do")
        return self

    def on_command(self, unit, command, level, hue):
        try:
            str_program_state = str(command).lower()

            # Only of HueLight is Unlocked (Configured in Toon) we can switch it On/Off
            if not self._huelight.is_locked:
                if str_program_state == "on":
                    # Turn HueLight On
                    self._huelight.turn_on()
                    program_state = 1
                else:
                    # Turn HueLight Off
                    self._huelight.turn_off()
                    program_state = 0

                if config.debug:
                    Domoticz.Log("Set HueLight '" + self.name + "' State :" + str_program_state)

                # Call Update
                self.plugin_devices[self.unit].Update(program_state, str(program_state))

            else:
                Domoticz.Log("Can't switch state of HueLight '" + self.name + "'. It is Locked in Toon")

        except DeviceCommandException as ex:
            Domoticz.Log("An error occurred Setting HueLight '" + self.name + "'")
            Domoticz.Log("Exception: " + str(ex))

    def update(self):
        super().update()
        str_value = ""

        try:
            program_state = 1 if (self._huelight.status.lower() == "on") else 0
            str_value = str(program_state)

            if str_value != self.previous_value:
                if config.debug:
                    Domoticz.Log("HueLight '" + self.name + "' state changed, update: " + str_value)
                self.plugin_devices[self.unit].Update(program_state, str_value)

        except DeviceUpdateException as ex:
            Domoticz.Log("An error occurred Updating HueLight '" + self.name + "'")
            Domoticz.Log("Exception: " + str(ex))

        self.set_previous_value(str_value)
        