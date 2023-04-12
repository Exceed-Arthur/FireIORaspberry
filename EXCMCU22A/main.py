import LightControl
from FireIORaspb import localServer, LED_PINS, DEVICE_USER, monitorSensors
import NetworkStation
import WebFunctions


def servicePicker():
    LightControl.lightShow([LED_PINS.RESET, LED_PINS.TALK], 6)
    if not NetworkStation.isConnected(): # Check if connected
        NetworkStation.connect_WIFI() # Connect to WIFI
        localServer()  # Ready local network socket to enable set-up web-app
    else: # Good WIFI Connection
        local_ip = WebFunctions.getOwnIP()  # Get basic IP address of new WIFI connection (home network)
        if local_ip not in DEVICE_USER.ip_addresses:  # Link multiple IP addresses for this user
            DEVICE_USER.ip_addresses.append(local_ip) 
        monitorSensors()


servicePicker()