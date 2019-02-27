# Installation on a Raspberry Pi (3)
This python plugin depends on the toonapilib created by Costas Tyfoxylos.<br>
The toonapilib source can be found at https://github.com/costastf/toonapilib

This plugin requires a Toon consumer api key and secret.<br>
Further reading: https://developer.toon.eu.

### Install toonapilib
* `sudo pip3 install toonapilib`

### Add the toonapi4domoticz plugin (this also is the way to update to a newer version for now)
* change dir into the domoticz plugins folder, e.g. `cd /home/pi/dev-domoticz/plugins`.
* `git clone https://github.com/JohnvandeVrugt/toonapilib4domoticz`.<br>
Or alternatively
* Create a subfolder in the domoticz/plugins folder, eg. /home/pi/dev-domoticz/plugins/toonapilib4domoticz.
* Copy the plugin.py file of this repository into the subfolder.
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
