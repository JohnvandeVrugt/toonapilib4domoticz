import Domoticz
import toonapilib


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DeviceContainer(metaclass=Singleton):

    def __init__(self):
        self._debug = False
        self._devices = []

    @property
    def devices(self):
        return self._devices

    @property
    def debug(self):
        return self._debug

    def add_device(self, device):
        self._devices.append(device)

    def on_command(self, unit, command, level, hue):
        dev = next((device for device in self._devices
                    if device.unit == unit), None)
        if dev is not None:
            dev.on_command(unit, command, level, hue)

    def set_debug(self, on_off):
        self._debug = on_off

    def update(self):
        for my_device in self._devices:
            my_device.update()


container = DeviceContainer()
