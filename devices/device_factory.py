import Domoticz
import toonapilib
from devices.device_container import container
from devices.gas import DeviceGas
from devices.heating_active import DeviceHeatingActive
from devices.hotwater_active import DeviceHotWaterActive
from devices.modulation_level import DeviceModulationLevel
from devices.power import DevicePower
from devices.preheat_active import DevicePreHeatActive
from devices.program_state import DeviceProgramState
from devices.set_point import DeviceSetPoint
from devices.temperature import DeviceTemperature
from devices.thermostat_state import DeviceThermostatState

STD_UNIT_POWER = 1
STD_UNIT_GAS = 2
STD_UNIT_TEMPERATURE = 3
STD_UNIT_SET_POINT = 4
STD_UNIT_HEATING_ACTIVE = 5
STD_UNIT_HOT_WATER_ACTIVE = 6
STD_UNIT_PREHEAT_ACTIVE = 7
STD_UNIT_SCENE = 8
STD_UNIT_PROGRAM_STATE = 9
STD_UNIT_MODULATION_LEVEL = 10


class DeviceFactory:
    def __init__(self):
        return

    @staticmethod
    def create_devices(toon, plugin_devices, debug):
        Domoticz.Log("Check and create Toon devices")
        container.set_debug(debug)

        """Adding standard devices"""
        container.add_device(DevicePower("Power usage", STD_UNIT_POWER, plugin_devices, toon, debug).create())
        container.add_device(DeviceGas("Gas usage", STD_UNIT_GAS, plugin_devices, toon, debug).create())
        container.add_device(DeviceTemperature("Room temperature", STD_UNIT_TEMPERATURE, plugin_devices, toon, debug).create())
        container.add_device(DeviceSetPoint("Set point", STD_UNIT_SET_POINT, plugin_devices, toon, debug).create())
        container.add_device(DeviceHeatingActive("Heating active", STD_UNIT_HEATING_ACTIVE, plugin_devices, toon, debug).create())
        container.add_device(DeviceHotWaterActive("Hot water active", STD_UNIT_HOT_WATER_ACTIVE, plugin_devices, toon, debug).create())
        container.add_device(DevicePreHeatActive("Preheat active", STD_UNIT_PREHEAT_ACTIVE, plugin_devices, toon, debug).create())
        container.add_device(DeviceThermostatState("Scene", STD_UNIT_SCENE, plugin_devices, toon, debug).create())
        container.add_device(DeviceProgramState("Program state", STD_UNIT_PROGRAM_STATE, plugin_devices, toon, debug).create())
        container.add_device(DeviceModulationLevel("Modulation level", STD_UNIT_MODULATION_LEVEL, plugin_devices, toon, debug).create())

        return container
