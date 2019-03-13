import Domoticz
import toonapilib


class Device:
    _previous_value = ""

    def __init__(self, name, unit, plugin_devices, toon):
        self._name = name
        self._unit = unit
        self._plugin_devices = plugin_devices
        self._toon = toon
        self._previous_value = ""

    @property
    def plugin_devices(self):
        return self._plugin_devices

    @property
    def exists(self):
        return self._unit in self._plugin_devices

    @property
    def name(self):
        return self._name

    @property
    def toon(self):
        return self._toon

    @property
    def unit(self):
        return self._unit

    @property
    def previous_value(self):
        return self._previous_value

    def set_previous_value(self, str_new_value):
        self._previous_value = str_new_value

    def create(self):
        Domoticz.Log("Creating " + self.name + " as unit " + self.unit)

    def on_command(self, unit, command, level, hue):
        return

    def update(self):
        return


class DeviceCommandException(Exception):
    """An error occurred while issuing a command"""


class DeviceCreateException(Exception):
    """An error occurred while creating the device"""


class DeviceUpdateException(Exception):
    """An error occurred while updating the device"""
