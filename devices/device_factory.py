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
from devices.smartplug import DeviceSmartPlugState
from devices.smartplug import DeviceSmartPlugUsage
from devices.smartplug import DeviceSmartPlugkWh
from devices.lights import DeviceLightState


class DeviceFactory:
    def __init__(self):
        return

    @staticmethod
    def create_devices(toon, plugin_devices):
        Domoticz.Log("Check and create Toon devices")

        """Adding standard devices"""
        container.add_device(DevicePower(plugin_devices, toon).create())
        container.add_device(DeviceGas(plugin_devices, toon).create())
        container.add_device(DeviceTemperature(plugin_devices, toon).create())
        container.add_device(DeviceSetPoint(plugin_devices, toon).create())
        container.add_device(DeviceHeatingActive(plugin_devices, toon).create())
        container.add_device(DeviceHotWaterActive(plugin_devices, toon).create())
        container.add_device(DevicePreHeatActive(plugin_devices, toon).create())
        container.add_device(DeviceThermostatState(plugin_devices, toon).create())
        container.add_device(DeviceProgramState(plugin_devices, toon).create())
        container.add_device(DeviceModulationLevel(plugin_devices, toon).create())

        # Smart Plugs
        for plug in toon.smartplugs:
            container.add_device(DeviceSmartPlugState(plugin_devices, toon, plug).create(plug))
            container.add_device(DeviceSmartPlugUsage(plugin_devices, toon, plug).create(plug))
            container.add_device(DeviceSmartPlugkWh(plugin_devices, toon, plug).create(plug))

        # Lights
        for light in toon.lights:
            container.add_device(DeviceLightState(plugin_devices, toon, light).create(light))

        return container
