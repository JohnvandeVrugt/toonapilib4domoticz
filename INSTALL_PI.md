# Installation on a Raspberry Pi (3)
This python plugin depends on the toonapilib created by Costas Tyfoxylos.<br>
The toonapilib source can be found at https://github.com/costastf/toonapilib

This plugin requires a Toon Access Token which can be created via "https://api.toon.eu/toonapi-accesstoken?tenant_id=eneco&client_id=<consumer_key>".<br>
Further reading: https://developer.toon.eu.

### Install / update toonapilib
* `sudo pip3 install toonapilib -U`
The -U flag updates toonapilib to the latest version.

### Install / update the toonapi4domoticz plugin
* change dir into the domoticz plugins folder, e.g. `cd /home/pi/dev-domoticz/plugins`.
* `git clone https://github.com/JohnvandeVrugt/toonapilib4domoticz`.<br>
Or alternatively
* Create a sub folder in the domoticz/plugins folder, eg. /home/pi/dev-domoticz/plugins/toonapilib4domoticz.
* Copy the plugin.py file and the devices folder of this repository into the sub folder.
* Restart the domoticz service `sudo service domoticz restart`.

### Setup the plugin within Domoticz
* Navigate to the hardware section of Domoticz.
* Select ToonApiLib4Domoticz from the type selection box and press add.
* Fill in the required fields:
  * Username: Eneco/Toon user name
  * Password: Eneco/Toon password
  * Consumer key: api key obtained from developer.toon.eu
  * Consumer secret: api secret obtained from developer.toon.eu

### Devices
The plugin will generate the following devices:
* P1 Smart meter Energy, "Power usage"
* P1 Smart meter Gas, "Gas usage"
* Temp LaCrosse TX3, "Setpoint"
* Thermostat, "Setpoint"
* Switch, "Heating active"
* Switch, "Hot water active"
* Switch, "Preheat active"
* Selector, "States"
* Switch, "Program state"
* Percentage, "Modulation level"
* SmartPlugs, devices with name of SmartPlug (Switch, Electric, kWh)

Domoticz allows to replace existing devices with the newly created ones.
See the Domoticz manual for instructions. http://www.domoticz.com/DomoticzManual.pdf
