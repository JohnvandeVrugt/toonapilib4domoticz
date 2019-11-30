import Domoticz
from devices.configuration import config
from devices.device import Device
from devices.device import DeviceCreateException
from devices.device import DeviceCommandException
from devices.device import DeviceUpdateException


class DeviceSmartPlugUsage(Device):
    domoticz_device_type = 248
    domoticz_subtype = 1
    _smartplug = None

    def __init__(self, plugin_devices, toon, plug):
        self._smartplug = plug
        super().__init__(self._smartplug.name,
                         config.STD_UNIT_SMARTPLUG_START_USAGE + self._smartplug.zwave_index,
                         plugin_devices,
                         toon)

    def create(self, plug):
        if not self.exists:
            try:
                Domoticz.Log("Creating SmartPlug Usage '" + self.name + "'")
                Domoticz.Device(Name=self.name, Unit=self.unit, Type=self.domoticz_device_type,
                                Subtype=self.domoticz_subtype).Create()

            except DeviceCreateException as ex:
                Domoticz.Log("An error occurred creating SmartPlug Usage '" + self.name + "'")
                Domoticz.Log("Exception: " + str(ex))
        elif config.debug:
            Domoticz.Log("Unit " + str(self.unit) + " exists - nothing to do")
        return self

    def update(self):
        super().update()
        str_value = ""

        try:
            str_value = str(self._smartplug.current_usage)

            if str_value != self.previous_value:
                if config.debug:
                    Domoticz.Log("Update SmartPlug '" + self.name + "' ,Usage: " + str_value)
                self.plugin_devices[self.unit].Update(0, str_value)

        except DeviceUpdateException as ex:
            Domoticz.Log("An error occurred Updating Smartplug Usage '" + self.name + "'")
            Domoticz.Log("Exception: " + str(ex))

        self.set_previous_value(str_value)


class DeviceSmartPlugState(Device):
    domoticz_device_type = 244
    domoticz_subtype = 73
    domoticz_switch_type = 0
    domoticz_image = 1
    _smartplug = None

    def __init__(self, plugin_devices, toon, plug):
        self._smartplug = plug
        super().__init__(self._smartplug.name,
                         config.STD_UNIT_SMARTPLUG_START_STATE + self._smartplug.zwave_index,
                         plugin_devices,
                         toon)

    def create(self, plug):
        if not self.exists:
            try:
                Domoticz.Log("Creating SmartPlug Switch '" + self.name + "'")
                Domoticz.Device(Name=self.name, Unit=self.unit, Type=self.domoticz_device_type,
                                Subtype=self.domoticz_subtype, Switchtype=self.domoticz_switch_type,
                                Image=self.domoticz_image).Create()

            except DeviceCreateException as ex:
                Domoticz.Log("An error occurred creating SmartPlug Switch '" + self.name + "'")
                Domoticz.Log("Exception: " + str(ex))
        elif config.debug:
            Domoticz.Log("Unit " + str(self.unit) + " exists - nothing to do")
        return self

    def on_command(self, unit, command, level, hue):
        try:
            str_program_state = str(command).lower()

            # Only of SmartPlug is Unlocked (Configured in Toon) we can switch it On/Off
            if not self._smartplug.is_locked:
                if str_program_state == "on":
                    # Turn SmartPlug On
                    self._smartplug.turn_on()
                    program_state = 1
                else:
                    # Turn SmartPlug Off
                    self._smartplug.turn_off()
                    program_state = 0

                if config.debug:
                    Domoticz.Log("Set SmartPlug Switch '" + self.name + "' State :" + str_program_state)

                # Call Update
                self.plugin_devices[self.unit].Update(program_state, str(program_state))

            else:
                Domoticz.Log("Can't switch state of SmartPlug Switch '" + self.name + "'. It is Locked in Toon")

        except DeviceCommandException as ex:
            Domoticz.Log("An error occurred Setting SmartPlug Switch '" + self.name + "'")
            Domoticz.Log("Exception: " + str(ex))

    def update(self):
        super().update()
        str_value = ""

        try:
            program_state = 1 if (self._smartplug.status.lower() == "on") else 0
            str_value = str(program_state)

            if str_value != self.previous_value:
                if config.debug:
                    Domoticz.Log("SmartPlug Switch '" + self.name + "' state changed, update: " + str_value)
                self.plugin_devices[self.unit].Update(program_state, str_value)

        except DeviceUpdateException as ex:
            Domoticz.Log("An error occurred Updating Smartplug Switch '" + self.name + "'")
            Domoticz.Log("Exception: " + str(ex))

        self.set_previous_value(str_value)


class DeviceSmartPlugkWh(Device):
    domoticz_device_type = 243
    domoticz_subtype = 29
    _smartplug = None

    def __init__(self, plugin_devices, toon, plug):
        self._smartplug = plug
        super().__init__(self._smartplug.name,
                         config.STD_UNIT_SMARTPLUG_START_KWH + self._smartplug.zwave_index,
                         plugin_devices,
                         toon)

    def create(self, plug):
        if not self.exists:
            try:
                Domoticz.Log("Creating SmartPlug kWh '" + self.name + "'")
                Domoticz.Device(Name=self.name, Unit=self.unit, Type=self.domoticz_device_type,
                                Subtype=self.domoticz_subtype).Create()

            except DeviceCreateException as ex:
                Domoticz.Log("An error occurred creating SmartPlug kWh '" + self.name + "'")
                Domoticz.Log("Exception: " + str(ex))
        elif config.debug:
            Domoticz.Log("Unit " + str(self.unit) + " exists - nothing to do")
        return self

    def update(self):
        super().update()
        str_value = ""

        try:
            str_value = "{0};{1}".format(self._smartplug.current_usage,
                                         self._smartplug.daily_usage)

            if str_value != self.previous_value:
                if config.debug:
                    Domoticz.Log("SmartPlug '" + self.name + "' [POWER];[ENERGY]: " + str_value)
                self.plugin_devices[self.unit].Update(0, str_value)

        except DeviceUpdateException as ex:
            Domoticz.Log("An error occurred Updating Smartplug kWh '" + self.name + "'")
            Domoticz.Log("Exception: " + str(ex))

        self.set_previous_value(str_value)
