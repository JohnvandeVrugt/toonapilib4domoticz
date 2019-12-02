# This python test can be used to check toonapilib functionality along with your credentials
# As domoticz is running python 3.x one should test this script with python3.x.
# Usage: python3.x testtoonapilib.py

from toonapilib import Toon

# please fill in your credentials and api key and secret
token = ''

print("Starting toonapilib test")
print("On success the room temperature will be presented")

try:
    print("Trying to create a toon object")
    toon = Toon(token)
    print("Room temperature: ", toon.temperature)

except Exception:
    print("An error occurred creating the Toon object")
