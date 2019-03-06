# ToonApiLib for Domoticz
# https://github.com/JohnvandeVrugt/toonapilib4domoticz
# by John van de Vrugt
#
# A domoticz plugin based on the toonapilib by Costas Tyfoxylos
# https://github.com/costastf/toonapilib/
"""
<plugin key="ToonApiLib" name="ToonApiLib" author="John van de Vrugt" version="1.0.13" wikilink="https://github.com/JohnvandeVrugt/toonapilib4domoticz">
    <description>
    </description>
    <params>
        <param field="Username" label="Eneco user" required="true"/>
        <param field="Password" label="Eneco pass" required="true" password="true"/>
        <param field="Mode1" label="Consumer key" required="true"/>
        <param field="Mode2" label="Consumer secret" required="true" password="true"/>
        <param field="Mode3" label="Update rate" required="true">
            <options>
                <option label="1 minute" value="1"/>
                <option label="2 minutes" value="2" default="true" />
                <option label="5 minutes" value="5"/>
                <option label="10 minutes" value="10"/>
                <option label="20 minutes" value="20"/>
                <option label="30 minutes" value="30"/>
                <option label="60 minutes" value="60"/>
            </options>
        </param>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import toonapilib

UNIT_POWER = 1
UNIT_GAS = 2
UNIT_TEMPERATURE = 3
UNIT_SET_POINT = 4
UNIT_HEATING_ACTIVE = 5
UNIT_HOT_WATER_ACTIVE = 6
UNIT_PREHEAT_ACTIVE = 7
UNIT_SCENE = 8
UNIT_PROGRAM_STATE = 9
UNIT_MODULATION_LEVEL = 10

HEARTBEATS_PER_MIN = 6


class ToonApiLibPlugin:
    my_toon = None
    heart_beat = 0
    print_debug_log = True
    heart_bead_mod = 1

    prv_str_power = ""
    prv_str_gas = ""
    prv_str_temp = ""
    prv_str_set_point = ""
    prv_str_burner_state = ""
    prv_str_thermostat_state = ""
    prv_program_state = -1
    prv_modulation_level = -1

    def __init__(self):
        return

    def on_start(self):
        Domoticz.Log("Using toonapilib version " + toonapilib.__version__ + " by " + toonapilib.__author__)

        self.print_debug_log = Parameters["Mode6"] == "Debug"
        if self.print_debug_log:
            Domoticz.Log("Debug logging is active")

        updates_per_min = 1
        if Parameters["Mode3"] != "":
            updates_per_min = int(Parameters["Mode3"])
        self.heart_bead_mod = HEARTBEATS_PER_MIN * updates_per_min

        if self.my_toon is None:
            self._create_toon_object()

        self._check_and_create_devices()
        self._update_devices()

    def on_command(self, Unit, Command, Level, Hue):
        if self.print_debug_log:
            Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" +
                         str(Command) + "', Level: " + str(Level))

        try:
            if Unit == UNIT_SET_POINT:
                self.my_toon.thermostat = Level
                Domoticz.Log("set set point " + str(Level))
                Devices[UNIT_SET_POINT].Update(0, str(Level))
        except:
            Domoticz.Log("An error occurred setting thermostat")

        try:
            if Unit == UNIT_SCENE:
                str_scene = self.get_scene_name(Level)
                self.my_toon.thermostat_state = str_scene
                Domoticz.Log("set scene " + str(Level) + " - " + str_scene)
                Devices[UNIT_SCENE].Update(2, str(Level))
        except:
            Domoticz.Log("An error occurred setting scene")

        try:
            if Unit == UNIT_PROGRAM_STATE:
                str_program_state = str(Command).lower()
                self.my_toon.program_state = str_program_state
                program_state = 0
                if str_program_state != "off":
                    program_state = 1
                Domoticz.Log("set program state " + str_program_state + " - " + str(program_state))
                Devices[UNIT_PROGRAM_STATE].Update(program_state, str(program_state))
        except:
            Domoticz.Log("An error occurred setting program state")

    def on_heartbeat(self):
        self.heart_beat = self.heart_beat + 1
        if self.my_toon is not None and self.heart_beat == self.heart_bead_mod:
            self.heart_beat = 0
            self._update_devices()

    def _create_toon_object(self):
        try:
            myname = Parameters["Username"]
            mypass = Parameters["Password"]
            mykey = Parameters["Mode1"]
            mysecret = Parameters["Mode2"]

            if self.print_debug_log:
                Domoticz.Log("Creating toonapilib object")

            self.my_toon = toonapilib.Toon(myname, mypass, mykey, mysecret)
        except Exception:
            self.my_toon = None
            Domoticz.Log("Could not create a toonapilib object")
            Domoticz.Log("Possible solution:")
            Domoticz.Log("* Check your credentials")
            Domoticz.Log("* Restart Domoticz")

    def _check_and_create_devices(self):
        Domoticz.Log("Check and create Toon devices")

        if UNIT_POWER not in Devices:
            try:
                Domoticz.Log("Creating Power usage device")
                Domoticz.Device(Name="Power usage", Unit=UNIT_POWER, Type=250, Subtype=1).Create()
            except:
                Domoticz.Log("An error occurred creating Power usage device")

        if UNIT_GAS not in Devices:
            try:
                Domoticz.Log("Creating Gas usage device")
                Domoticz.Device(Name="Gas usage", Unit=UNIT_GAS, Type=251, Subtype=2).Create()
            except:
                Domoticz.Log("An error occurred creating Gas usage device")

        if UNIT_TEMPERATURE not in Devices:
            try:
                Domoticz.Log("Creating Room temperature device")
                Domoticz.Device(Name="Room temperature", Unit=UNIT_TEMPERATURE, Type=80, Subtype=5).Create()
            except:
                Domoticz.Log("An error occurred creating Room temperature device")

        if UNIT_SET_POINT not in Devices:
            try:
                Domoticz.Log("Creating Set point device")
                Domoticz.Device(Name="Set point", Unit=UNIT_SET_POINT, Type=242, Subtype=1).Create()
            except:
                Domoticz.Log("An error occurred creating Set point device")

        if UNIT_HEATING_ACTIVE not in Devices:
            try:
                Domoticz.Log("Creating Heating active device")
                Domoticz.Device(Name="Heating active", Unit=UNIT_HEATING_ACTIVE, Type=244, Subtype=62, Switchtype=0, Image=9).Create()
            except:
                Domoticz.Log("An error occurred creating Heating active device")

        if UNIT_HOT_WATER_ACTIVE not in Devices:
            try:
                Domoticz.Log("Creating Hot water active device")
                Domoticz.Device(Name="Hot water active", Unit=UNIT_HOT_WATER_ACTIVE, Type=244, Subtype=62, Switchtype=0, Image=9).Create()
            except:
                Domoticz.Log("An error occurred creating Hot water active device")

        if UNIT_PREHEAT_ACTIVE not in Devices:
            try:
                Domoticz.Log("Creating Preheat active device")
                Domoticz.Device(Name="Preheat active", Unit=UNIT_PREHEAT_ACTIVE, Type=244, Subtype=62, Switchtype=0, Image=9).Create()
            except:
                Domoticz.Log("An error occurred creating Preheat active device")

        if UNIT_SCENE not in Devices:
            try:
                Domoticz.Log("Creating Scene device")
                options = {
                    "LevelNames": "Unknown|Away|Sleep|Home|Comfort|Holiday",
                    "LevelOffHidden": "true", "SelectorStyle": "0"}
                Domoticz.Device(Name="Scene", Unit=UNIT_SCENE, TypeName="Selector Switch", Options=options).Create()
            except:
                Domoticz.Log("An error occurred creating Scene device")

        if UNIT_PROGRAM_STATE not in Devices:
            try:
                Domoticz.Log("Creating Program state device")
                Domoticz.Device(Name="Program state", Unit=UNIT_PROGRAM_STATE, Type=244, Subtype=62, Switchtype=0, Image=9).Create()
            except:
                Domoticz.Log("An error occurred creating Program state device")

        if UNIT_MODULATION_LEVEL not in Devices:
            try:
                Domoticz.Log("Creating Modulation level device")
                Domoticz.Device(Name="Modulation level", Unit=UNIT_MODULATION_LEVEL, Type=243, Subtype=6, Switchtype=0).Create()
            except:
                Domoticz.Log("An error occurred creating Modulation level device")

    def _update_devices(self):
        if self.my_toon is not None:
            self._update_power()
            self._update_gas()
            self._update_temperature()
            self._update_set_point()
            self._update_burner_state()
            self._update_thermostat_state()
            self._update_program_active()
            self._update_modulation_level()

    def _update_power(self):
        try:
            str_power = str(self.my_toon.power.meter_reading_low) + ";" + \
                        str(self.my_toon.power.meter_reading) + ";" + \
                        str(self.my_toon.solar.meter_reading_low_produced) + ";" + \
                        str(self.my_toon.solar.meter_reading_produced) + ";" + \
                        str(self.my_toon.power.value) + ";" + str(self.my_toon.solar.value)

            if str_power != self.prv_str_power:
                if self.print_debug_log:
                    Domoticz.Log("Update power/solar usage: " + str_power)
                Devices[UNIT_POWER].Update(0, str_power)

            self.prv_str_power = str_power
        except:
            Domoticz.Log("An error occurred updating power usage")

    def _update_gas(self):
        try:
            str_gas = str(self.my_toon.gas.daily_usage)

            if str_gas != self.prv_str_gas:
                if self.print_debug_log:
                    Domoticz.Log("Update gas usage: " + str_gas)
                Devices[UNIT_GAS].Update(0, str_gas)

            self.prv_str_gas = str_gas
        except:
            Domoticz.Log("An error occurred updating gas usage")

    def _update_temperature(self):
        try:
            str_temp = str(self.my_toon.temperature)

            if str_temp != self.prv_str_temp:
                if self.print_debug_log:
                    Domoticz.Log("Update temperature: " + str_temp)
                Devices[UNIT_TEMPERATURE].Update(0, str_temp)

            self.prv_str_temp = str_temp
        except:
            Domoticz.Log("An error occurred updating temperature")

    def _update_set_point(self):
        try:
            str_set_point = str(self.my_toon.thermostat)

            if str_set_point != self.prv_str_set_point:
                if self.print_debug_log:
                    Domoticz.Log("Update set point: " + str_set_point)
                Devices[UNIT_SET_POINT].Update(0, str_set_point)

            self.prv_str_set_point = str_set_point
        except:
            Domoticz.Log("An error occurred updating thermostat set point")

    def _update_burner_state(self):
        try:
            str_burner_state = ""
            hot_water_on = 0
            heating_on = 0
            preheating_on = 0

            try:
                str_burner_state = self.my_toon.burner_state
            except:
                Domoticz.Log("An error occurred updating burner state")

            if str_burner_state != "":

                if str_burner_state == "on":
                    heating_on = 1
                elif str_burner_state == "water_heating":
                    hot_water_on = 1
                elif str_burner_state == "pre_heating":
                    preheating_on = 1

                if str_burner_state != self.prv_str_burner_state:
                    if self.print_debug_log:
                        Domoticz.Log("Update state: " + str_burner_state)
                    Devices[UNIT_HEATING_ACTIVE].Update(heating_on, str(heating_on))
                    Devices[UNIT_HOT_WATER_ACTIVE].Update(hot_water_on, str(hot_water_on))
                    Devices[UNIT_PREHEAT_ACTIVE].Update(preheating_on, str(preheating_on))

                self.prv_str_burner_state = str_burner_state
        except:
            Domoticz.Log("An error occurred updating burner state")

    def _update_thermostat_state(self):
        try:
            str_thermostat_state = ""
            if not self.my_toon.thermostat_state:
                str_thermostat_state = "Unknown"
                if self.print_debug_log:
                    Domoticz.Log("Update state: Manual set point - no thermostat state chosen")
            else:
                str_thermostat_state = str(self.my_toon.thermostat_state.name)

            if str_thermostat_state != "":
                if str_thermostat_state != self.prv_str_thermostat_state:
                    if self.print_debug_log:
                        Domoticz.Log("Update state: " + str_thermostat_state + " - " +
                                     str(self.get_scene_value(str_thermostat_state)))
                    Devices[UNIT_SCENE].Update(2, str(self.get_scene_value(str_thermostat_state)))

                self.prv_str_thermostat_state = str_thermostat_state
        except:
            Domoticz.Log("An error occurred updating thermostat state")

    def _update_program_active(self):
        try:
            program_state = 0
            if self.my_toon.program_state != "off":
                program_state = 1

            if program_state != self.prv_program_state:
                if self.print_debug_log:
                    Domoticz.Log("Update program state: " + str(program_state))
                Devices[UNIT_PROGRAM_STATE].Update(program_state, str(program_state))

            self.prv_program_state = program_state
        except:
            Domoticz.Log("An error occurred updating program state")

    def _update_modulation_level(self):
        try:
            modulation_level = self.my_toon.thermostat_info.current_modulation_level

            if modulation_level != self.prv_modulation_level:
                if self.print_debug_log:
                    Domoticz.Log("Update modulation level: " + str(modulation_level))
                Devices[UNIT_MODULATION_LEVEL].Update(modulation_level, str(modulation_level))

            self.prv_modulation_level = modulation_level
        except:
            Domoticz.Log("An error occurred updating modulation level")

    @staticmethod
    def get_scene_value(x):
        return {
            'Unknown': 0,
            'Away': 10,
            'Sleep': 20,
            'Home': 30,
            'Comfort': 40,
            'Holiday': 50
        }[x]

    @staticmethod
    def get_scene_name(i):
        str_return_string = "Unknown"

        if i == 10:
            str_return_string = "Away"
        elif i == 20:
            str_return_string = "Sleep"
        elif i == 30:
            str_return_string = "Home"
        elif i == 40:
            str_return_string = "Comfort"
        elif i == 50:
            str_return_string = "Holiday"

        return str_return_string

global _plugin
_plugin = ToonApiLibPlugin()


def onStart():
    global _plugin
    _plugin.on_start()


def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.on_command(Unit, Command, Level, Hue)


def onHeartbeat():
    global _plugin
    _plugin.on_heartbeat()
