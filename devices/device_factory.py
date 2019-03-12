import Domoticz
import toonapilib
from devices.configuration import config
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


class DeviceFactory:
    def __init__(self):
        return

    @staticmethod
    def create_devices(toon, plugin_devices, debug):
        Domoticz.Log("Check and create Toon devices")
        container.set_debug(debug)

        """Adding standard devices"""
        container.add_device(DevicePower(config.STR_UNIT_POWER, config.STD_UNIT_POWER, plugin_devices, toon, debug).create())
        container.add_device(DeviceGas(config.STR_UNIT_GAS, config.STD_UNIT_GAS, plugin_devices, toon, debug).create())
        container.add_device(DeviceTemperature(config.STR_UNIT_TEMPERATURE, config.STD_UNIT_TEMPERATURE, plugin_devices, toon, debug).create())
        container.add_device(DeviceSetPoint(config.STR_UNIT_SET_POINT, config.STD_UNIT_SET_POINT, plugin_devices, toon, debug).create())
        container.add_device(DeviceHeatingActive(config.STR_UNIT_HEATING_ACTIVE, config.STD_UNIT_HEATING_ACTIVE, plugin_devices, toon, debug).create())
        container.add_device(DeviceHotWaterActive(config.STR_UNIT_HOT_WATER_ACTIVE, config.STD_UNIT_HOT_WATER_ACTIVE, plugin_devices, toon, debug).create())
        container.add_device(DevicePreHeatActive(config.STR_UNIT_PREHEAT_ACTIVE, config.STD_UNIT_PREHEAT_ACTIVE, plugin_devices, toon, debug).create())
        container.add_device(DeviceThermostatState(config.STR_UNIT_SCENE, config.STD_UNIT_SCENE, plugin_devices, toon, debug).create())
        container.add_device(DeviceProgramState(config.STR_UNIT_PROGRAM_STATE, config.STD_UNIT_PROGRAM_STATE, plugin_devices, toon, debug).create())
        container.add_device(DeviceModulationLevel(config.STR_UNIT_MODULATION_LEVEL, config.STD_UNIT_MODULATION_LEVEL, plugin_devices, toon, debug).create())

        return container
