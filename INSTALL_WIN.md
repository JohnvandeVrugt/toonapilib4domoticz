# Installation on a windows (10) target
This python plugin depends on the toonapilib created by Costas Tyfoxylos.<br>
The toonapilib source can be found at https://github.com/costastf/toonapilib

This plugin requires a Toon consumer api key and secret.<br>
Further reading: https://developer.toon.eu.

### Install Python
* Download the latest !! 32-bit !! 3.x Python version from http://python.org
* Install the Python software
* During installation check that pip is installed and that the python path is added to the environment PATH of windows.

### Install toonapilib
* Open a command prompt (with admin rights)
* Install the toonapilib: `pip install toonapilib -U` The -U flag updates toonapilib to the latest version.

### Add the toonapi4domoticz plugin
* Create a subfolder named 'plugins' in the installation folder of Domoticz, e.g. c:\program files(x86)\domoticz\plugins.
* Create a subfolder in the domoticz plugins folder, eg. c:\program files(x86)\domoticz\plugins\toonapilib4domoticz.
* Copy the plugin.py file and the devices folder of this repository into the subfolder.
* Restart the domoticz service.

### Setup the plugin within Domoticz
* Navigate to the hardware section of Domoticz.
* Select ToonApiLib4Domoticz from the type selection box and press add.

* Fill in the required fields:
  - Username: Eneco/Toon user name
  - Password: Eneco/Toon password
  - Consumer key: api key obtained from developer.toon.eu
  - Consumer secret: api secret obtained from developer.toon.eu

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
