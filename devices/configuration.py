import Domoticz


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Configuration(metaclass=Singleton):
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
    STD_UNIT_SMARTPLUG_START_STATE = 100  # Begin counting for SmartPlugs State
    STD_UNIT_SMARTPLUG_START_USAGE = 120  # Begin counting for SmartPlugs Usage
    STD_UNIT_SMARTPLUG_START_KWH = 140    # Begin counting for SmartPlugs kWh
    STD_UNIT_LIGHT_START_STATE = 200 # Begin counting for Light State

    STR_UNIT_POWER = "Power usage"
    STR_UNIT_GAS = "Gas usage"
    STR_UNIT_TEMPERATURE = "Room temperature"
    STR_UNIT_SET_POINT = "Set point"
    STR_UNIT_HEATING_ACTIVE = "Heating active"
    STR_UNIT_HOT_WATER_ACTIVE = "Hot water active"
    STR_UNIT_PREHEAT_ACTIVE = "Preheat active"
    STR_UNIT_SCENE = "Scene"
    STR_UNIT_PROGRAM_STATE = "Program state"
    STR_UNIT_MODULATION_LEVEL = "Modulation level"

    _debug = False

    @property
    def debug(self):
        return self._debug

    def set_debug(self, on_off):
        self._debug = on_off
        str_on_off = "on" if on_off else "off"
        Domoticz.Log("Debug logging is " + str_on_off)


config = Configuration()
