# ToonApiLib for Domoticz
# by John van de Vrugt
#
"""
<plugin key="ToonApiLib" name="ToonApiLib" author="John van de Vrugt" version="1.0.0" wikilink="https://github.com/JohnvandeVrugt/toonapilib4domoticz">
    <description>
    </description>
    <params>
		<param field="Username" label="Username" required="true"/>
		<param field="Password" label="Password" required="true"/>
		<param field="Mode1" label="Consumer key" required="true"/>
		<param field="Mode2" label="Consumer secret" required="true"/>
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
        myname = Parameters["Username"]
        mypass = Parameters["Password"]
        mykey = Parameters["Mode1"]
        mysecret = Parameters["Mode2"]
        MyToon = Toon(myname, mypass, mykey, mysecret)
        szStates = ""

        if MyToon != None:
            #check for devices
            if (len(Devices) == 0):
                Domoticz.Log("Creating Toon devices")
                Domoticz.Device(Name="Power usage", Unit=1, Type=250, Subtype=1).Create()
                Domoticz.Device(Name="Gas usage", Unit=2, Type=251, Subtype=2).Create()
                Domoticz.Device(Name="Room temperature", Unit=3, Type=80, Subtype=5).Create()
                Domoticz.Device(Name="Setpoint", Unit=4, Type=242, Subtype=1).Create()
                Domoticz.Device(Name="Heating active", Unit=5, Type=244, Subtype=62, Switchtype=0).Create()
                Domoticz.Device(Name="Hot water active", Unit=6, Type=244, Subtype=62, Switchtype=0).Create()
                Domoticz.Device(Name="Preheat active", Unit=7, Type=244, Subtype=62, Switchtype=0).Create()

                #scenes
                for state in MyToon.thermostat_states:
                    if state.id != 0:
                        szStates += "|"
                    szStates += state.name
                if DebugPrint:
                    Domoticz.Log(szStates)

                Options = {"LevelNames": szStates, "LevelOffHidden": "false", "SelectorStyle": "1"}
                Domoticz.Device(Name="Source", Unit=8, TypeName="Selector Switch", Options=Options).Create()
            else:
                UpdateDevices()

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        if DebugPrint:
            Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        
        if Unit == 4:
            MyToon.thermostat=Level
            Domoticz.Log("set level " +  str(Level))
            szSetpoint = str(MyToon.thermostat)
            Devices[4].Update(0, szSetpoint);

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        #Domoticz.Log("heartbeat "+ str(Heartbeat));
        global Heartbeat
        Heartbeat = Heartbeat + 1
        if Heartbeat == 12:
            Heartbeat = 0
            UpdateDevices()

def UpdateDevices():
    if MyToon != None:
        szPower = str(MyToon.power.meter_reading_low) + ";" + str(MyToon.power.meter_reading) + ";0;0;" + str(MyToon.power.value) + ";0"
        if DebugPrint:
            Domoticz.Log("Update power usage: " + szPower)
        Devices[1].Update(0, szPower)

        szGas = str(MyToon.gas.daily_usage)
        if DebugPrint:
            Domoticz.Log("Update gas usage: " + szGas)
        Devices[2].Update(0, szGas)

        szTemp = str(MyToon.temperature)
        if DebugPrint:
            Domoticz.Log("Update temperature: " + szTemp)
        Devices[3].Update(0, szTemp)

        szSetpoint = str(MyToon.thermostat)
        if DebugPrint:
            Domoticz.Log("Update temperature: " + szSetpoint)
        Devices[4].Update(0, szSetpoint);

	#todo: add heating actice, hot water active, pre-heat active and update states


def getSelector(x):
    return {
        'Comfort': 0,
        'Home': 10,
        'Sleep': 20,
        'Away': 30,
        'Unknown': 40,
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
