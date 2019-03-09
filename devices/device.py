import Domoticz
import toonapilib


class Device:
    _previous_value = ""

    def __init__(self, name, unit, devices, toon, debug):
        self._name = name
        self._unit = unit
        self._devices = devices
        self._toon = toon
        self._debug = debug
        self._previous_value = ""

    @property
    def debug(self):
        return self._debug

    @property
    def devices(self):
        return self._devices

    @property
    def exists(self):
        Domoticz.Log("Check existence of " + self._name)
        return self._unit in self._devices

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

    def on_command(self, Unit, Command, Level, Hue):
        return

    def update(self):
        return


class DeviceCommandException(Exception):
    """An error occurred while issuing a command"""


class DeviceCreateException(Exception):
    """An error occurred while creating the device"""


class DeviceUpdateException(Exception):
    """An error occurred while updating the device"""
