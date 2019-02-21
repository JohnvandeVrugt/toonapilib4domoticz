# Installation
This python plugin depends on the toonapilib created by Costas Tyfoxylos.<br>
The toonapilib source can be found at https://github.com/costastf/toonapilib
<br>
<br>
This plugin requires a Toon consumer api key and secret.<br>
Further reading: https://developer.toon.eu.
<br>
<br>
First requirement, install toonapilib on your domoticz server device
* sudo pip3 install toonapilib
Note: successfully tested with v3.0.2.

Add the plugin to the domoticz project
* Create a subfolder in the domoticz/plugins folder, eg. /home/pi/dev-domoticz/plugins/toonapilib4domoticz
* Copy this plugin.py file into the subfolder

Restart the domoticz service
* sudo service domoticz restart

Setup the plugin within Domoticz
* Navigate to the hardware section of Domoticz
* Select ToonApiLib4Domoticz from the type selection box and press add

Fill in the required fields:
* Username: Eneco/Toon user name
* Password: Eneco/Toon password
* Consumer key: api key obtained from developer.toon.eu
* Consumer secret: api secret obtained from developer.toon.eu

The plugin will generate the following devices:
* P1 Smart meter Energy, "Power usage"
* P1 Smart meter Gas, "Gas usage"
* Temp LaCrosse TX3, "Setpoint"
* Thermostat, "Setpoint"
* Switch, "Heating active"
* Switch, "Hot water active"
* Switch, "Preheat active"
* Selector, "States"
