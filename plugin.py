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


class ToonApiLibPlugin:
    my_toon = None
    heart_beat = 0
    print_debug_log = True

    def __init__(self):
        return

    def on_start(self):
        self.print_debug_log = Parameters["Mode6"] == "Debug"

        if self.print_debug_log:
            Domoticz.Log("Starting toonapilib4domoticz with debug logging")

        Domoticz.Log("Using toonapilib version " + toonapilib.__version__ + " by " + toonapilib.__author__)

        self.create_toon_object()

        if self.my_toon is not None:
            if len(Devices) == 0:
                Domoticz.Log("Creating Toon devices")
                self._create_devices()
            else:
                self._update_devices()

    def on_command(self, Unit, Command, Level, Hue):
        if self.print_debug_log:
            Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" +
                         str(Command) + "', Level: " + str(Level))

        try:
            if Unit == 4:
                self.my_toon.thermostat = Level
                Domoticz.Log("set level " + str(Level))
                Devices[4].Update(0, str(Level))
        except:
            Domoticz.Log("An error occurred setting thermostat")

        try:
            if Unit == 8:
                str_scene = self.get_scene_name(Level)
                self.my_toon.thermostat_state = str_scene
                Domoticz.Log("set scene " + str(Level) + " - " + str_scene)
                Devices[8].Update(2, str(Level))
        except:
            Domoticz.Log("An error occurred setting scene")

    def on_heartbeat(self):
        self.heart_beat = self.heart_beat + 1
        if self.my_toon is not None and self.heart_beat == 12:
            self.heart_beat = 0
            self._update_devices()

    def create_toon_object(self):
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

    def _create_devices(self):
        try:
            Domoticz.Device(Name="Power usage", Unit=1, Type=250, Subtype=1).Create()
            Domoticz.Device(Name="Gas usage", Unit=2, Type=251, Subtype=2).Create()
            Domoticz.Device(Name="Room temperature", Unit=3, Type=80, Subtype=5).Create()
            Domoticz.Device(Name="Set point", Unit=4, Type=242, Subtype=1).Create()
            Domoticz.Device(Name="Heating active", Unit=5, Type=244, Subtype=62, Switchtype=0).Create()
            Domoticz.Device(Name="Hot water active", Unit=6, Type=244, Subtype=62, Switchtype=0).Create()
            Domoticz.Device(Name="Preheat active", Unit=7, Type=244, Subtype=62, Switchtype=0).Create()

            options = {
                "LevelNames": "Unknown|Away|Sleep|Home|Comfort|Holiday",
                "LevelOffHidden": "true", "SelectorStyle": "0"}
            Domoticz.Device(Name="Scene", Unit=8, TypeName="Selector Switch", Options=options).Create()
        except:
            Domoticz.Log("An error occurred while creating Toon devices")

    def _update_devices(self):
        if self.my_toon is not None:
            self._update_power()
            self._update_gas()
            self._update_temperature()
            self._update_set_point()
            self._update_burner_state()
            self._update_thermostat_state()

    def _update_power(self):
        try:
            str_power = str(self.my_toon.power.meter_reading_low) + ";" + \
                        str(self.my_toon.power.meter_reading) + ";" + \
                        str(self.my_toon.solar.meter_reading_low_produced) + ";" + \
                        str(self.my_toon.solar.meter_reading_produced) + ";" + \
                        str(self.my_toon.power.value) + ";" + str(self.my_toon.solar.value)
            if self.print_debug_log:
                Domoticz.Log("Update power/solar usage: " + str_power)
            Devices[1].Update(0, str_power)
        except:
            Domoticz.Log("An error occurred updating power usage")

    def _update_gas(self):
        try:
            str_gas = str(self.my_toon.gas.daily_usage)
            if self.print_debug_log:
                Domoticz.Log("Update gas usage: " + str_gas)
            Devices[2].Update(0, str_gas)
        except:
            Domoticz.Log("An error occurred updating gas usage")

    def _update_temperature(self):
        try:
            str_temp = str(self.my_toon.temperature)
            if self.print_debug_log:
                Domoticz.Log("Update temperature: " + str_temp)
            Devices[3].Update(0, str_temp)
        except:
            Domoticz.Log("An error occurred updating temperature")

    def _update_set_point(self):
        try:
            str_set_point = str(self.my_toon.thermostat)
            if self.print_debug_log:
                Domoticz.Log("Update set point: " + str_set_point)
            Devices[4].Update(0, str_set_point)
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
                if self.print_debug_log:
                    Domoticz.Log("Update state: " + str_burner_state)

                if str_burner_state == "on":
                    heating_on = 1
                elif str_burner_state == "water_heating":
                    hot_water_on = 1
                elif str_burner_state == "pre_heating":
                    preheating_on = 1

                Devices[5].Update(heating_on, str(heating_on))
                Devices[6].Update(hot_water_on, str(hot_water_on))
                Devices[7].Update(preheating_on, str(preheating_on))

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
                if self.print_debug_log:
                    Domoticz.Log("Update state: " + str_thermostat_state + " - " +
                                 str(self.get_scene_value(str_thermostat_state)))
                Devices[8].Update(2, str(self.get_scene_value(str_thermostat_state)))
        except:
            Domoticz.Log("An error occurred updating thermostat state")

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
