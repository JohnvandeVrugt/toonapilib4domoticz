# ToonApiLib for Domoticz
# https://github.com/JohnvandeVrugt/toonapilib4domoticz
# by John van de Vrugt
#
# A domoticz plugin based on the toonapilib by Costas Tyfoxylos
# https://github.com/costastf/toonapilib/
"""
<plugin key="ToonApiLib" name="ToonApiLib" author="John van de Vrugt" version="1.0.14" wikilink="https://github.com/JohnvandeVrugt/toonapilib4domoticz">
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
from devices.configuration import config
from devices.device_factory import DeviceFactory

HEARTBEATS_PER_MIN = 6


class ToonApiLibPlugin:
    _heart_beat = 0
    _heart_bead_mod = 1
    _my_toon = None
    _toon_devices = None

    def __init__(self):
        return

    def on_start(self):
        Domoticz.Log("Using toonapilib version " + toonapilib.__version__ + " by " + toonapilib.__author__)
        config.set_debug(Parameters["Mode6"] == "Debug")

        updates_per_min = 1
        if Parameters["Mode3"] != "":
            updates_per_min = int(Parameters["Mode3"])
        self._heart_bead_mod = HEARTBEATS_PER_MIN * updates_per_min

        if self._my_toon is None:
            self._create_toon_object()

        self._toon_devices = DeviceFactory.create_devices(self._my_toon, Devices)
        self._update_devices()

    def on_command(self, Unit, Command, Level, Hue):
        if config.debug:
            Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" +
                         str(Command) + "', Level: " + str(Level))
        self._toon_devices.on_command(Unit, Command, Level, Hue)

    def on_heartbeat(self):
        self._heart_beat = self._heart_beat + 1
        if self._my_toon is not None and self._heart_beat == self._heart_bead_mod:
            self._heart_beat = 0
            self._update_devices()

    def _create_toon_object(self):
        try:
            myname = Parameters["Username"]
            mypass = Parameters["Password"]
            mykey = Parameters["Mode1"]
            mysecret = Parameters["Mode2"]

            if config.debug:
                Domoticz.Log("Creating toonapilib object")

            self._my_toon = toonapilib.Toon(myname, mypass, mykey, mysecret)

        except Exception:
            self._my_toon = None
            Domoticz.Log("Could not create a toonapilib object")
            Domoticz.Log("Possible solution:")
            Domoticz.Log("* Check your credentials")
            Domoticz.Log("* Restart Domoticz")

    def _update_devices(self):
        if self._my_toon is not None:
            self._toon_devices.update()


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
