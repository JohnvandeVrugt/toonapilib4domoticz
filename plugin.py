# ToonApiLib for Domoticz
# by John van de Vrugt
#
"""
<plugin key="ToonApiLib" name="ToonApiLib" author="John van de Vrugt" version="1.0.7" wikilink="https://github.com/JohnvandeVrugt/toonapilib4domoticz">
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
from toonapilib import Toon

MyToon = None
Heartbeat = 0
DebugPrint = True

class BasePlugin:
    enabled = False
    def __init__(self):
        return

    def onStart(self):
        global MyToon
        global DebugPrint

        DebugPrint = Parameters["Mode6"] == "Debug"
        if DebugPrint:
            Domoticz.Log("Starting toonapilib4domoticz with debug logging")

        CreateToonObject()

        if MyToon != None:
            #check for devices
            if (len(Devices) == 0):
                Domoticz.Log("Creating Toon devices")

                try:
                    Domoticz.Device(Name="Power usage", Unit=1, Type=250, Subtype=1).Create()
                    Domoticz.Device(Name="Gas usage", Unit=2, Type=251, Subtype=2).Create()
                    Domoticz.Device(Name="Room temperature", Unit=3, Type=80, Subtype=5).Create()
                    Domoticz.Device(Name="Setpoint", Unit=4, Type=242, Subtype=1).Create()
                    Domoticz.Device(Name="Heating active", Unit=5, Type=244, Subtype=62, Switchtype=0).Create()
                    Domoticz.Device(Name="Hot water active", Unit=6, Type=244, Subtype=62, Switchtype=0).Create()
                    Domoticz.Device(Name="Preheat active", Unit=7, Type=244, Subtype=62, Switchtype=0).Create()
                except:
                    Domoticz.Log("An error occured while creating Toon devices")

                #add scenes
                Options = {"LevelNames": "Unknown|Away|Sleep|Home|Comfort", "LevelOffHidden": "true", "SelectorStyle": "0"}
                Domoticz.Device(Name="Scene", Unit=8, TypeName="Selector Switch", Options=Options).Create()
            else:
                UpdateDevices()

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        global myToon
        if DebugPrint:
            Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

        try:
            if Unit == 4:
                MyToon.thermostat = Level
                Domoticz.Log("set level " +  str(Level))
                szSetpoint = str(MyToon.thermostat)
                Devices[4].Update(0, szSetpoint)
        except:
            Domoticz.Log("An error occured setting thermostat")

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        global Heartbeat
        Heartbeat = Heartbeat + 1
        if Heartbeat == 12:
            Heartbeat = 0
            UpdateDevices()

def CreateToonObject():
    global MyToon
    try:
        myname = Parameters["Username"]
        mypass = Parameters["Password"]
        mykey = Parameters["Mode1"]
        mysecret = Parameters["Mode2"]

        if DebugPrint:
            Domoticz.Log("Creating Toon object")

        MyToon = Toon(myname, mypass, mykey, mysecret)
    except:
        MyToon = None
        Domoticz.Log("Could not create a toon object")
        Domoticz.Log("Possible solution:")
        Domoticz.Log("* Check your credentials")
        Domoticz.Log("* Restart domoticz")

def UpdateDevices():
    global MyToon

    if MyToon != None:
        try: 
            szPower = str(MyToon.power.meter_reading_low) + ";" + str(MyToon.power.meter_reading) + ";0;0;" + str(MyToon.power.value) + ";0"
            if DebugPrint:
                Domoticz.Log("Update power usage: " + szPower)
            Devices[1].Update(0, szPower)
        except:
            Domoticz.Log("An error occured updating power usage")

        try:
            szGas = str(MyToon.gas.daily_usage)
            if DebugPrint:
                Domoticz.Log("Update gas usage: " + szGas)
            Devices[2].Update(0, szGas)
        except:
            Domoticz.Log("An error occured updating gas usage")

        try:
            szTemp = str(MyToon.temperature)
            if DebugPrint:
                Domoticz.Log("Update temperature: " + szTemp)
            Devices[3].Update(0, szTemp)
        except:
            Domoticz.Log("An error occured updating temperature")

        try:
            szSetpoint = str(MyToon.thermostat)
            if DebugPrint:
                Domoticz.Log("Update setpoint: " + szSetpoint)
            Devices[4].Update(0, szSetpoint)
        except:
            Domoticz.Log("An error occured updating thermostat")

        try:
            szThermostatState = ""

            if MyToon.thermostat_info.program_state == 0:
                #program is off
                szThermostatState = "Unknown"
            else:
                try:
                    szThermostatState = str(MyToon.thermostat_state.name)
                except:
                    Domoticz.Log("An error occured updating thermostat state")

            if szThermostatState != "":
                if DebugPrint:
                    Domoticz.Log("Update state: " + szThermostatState + " - " + str(getSceneValue(szThermostatState))) 
                Devices[8].Update(2, str(getSceneValue(szThermostatState)))
        except:
            Domoticz.Log("An error occured updating thermostat state")

        try:
            szBurnerState = ""
            hotwater_on = 0
            heating_on = 0
            preheating_on = 0

            try:
                szBurnerState = MyToon.burner_state
            except:
                Domoticz.Log("An error occured updating burner state")

            if szBurnerState != "":
                if DebugPrint:
                    Domoticz.Log("Update state: " + szBurnerState)
 
                if szBurnerState == "on":
                    heating_on = 1
                elif szBurnerState == "water_heating":
                    hotwater_on = 1
                elif szBurnerState == "pre_heating":
                    preheating_on = 1

                Devices[5].Update(heating_on, str(heating_on))
                Devices[6].Update(hotwater_on, str(hotwater_on))
                Devices[7].Update(preheating_on, str(preheating_on))

        except:
            Domoticz.Log("An error occured updating burner state")

def getSceneValue(x):
    return {
        'Unknown': 0,
        'Away': 10,
        'Sleep': 20,
        'Home': 30,
        'Comfort': 40
    }[x]

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()
