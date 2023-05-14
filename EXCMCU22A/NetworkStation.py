import config
import network
from LightControl import *
from PIN_DEFS import *
import access_point_exc
import ValidateCredentials

STATION_INTERFACE = network.WLAN(network.STA_IF)


def connect_WIFI():
    print("ENTERED CONNECT WIFI FUNC")
    global STATION_INTERFACE
    access_point_exc.ap_if.active(False)  # Turn off local access point
    if not STATION_INTERFACE.isconnected():
        print("Connecting to WIFI...")
        STATION_INTERFACE.active(True)
        if config.WIFI_SSID and config.WIFI_PASSWORD:
            STATION_INTERFACE.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
            timeoutLimit = 30
            while not STATION_INTERFACE.isconnected() and timeoutLimit:
                time.sleep(1)
                timeoutLimit -= 1
                lightShow([DISCONNECT, CONNECT], 1)
            if not timeoutLimit:
                print("Failed to connect within timeout period")
                return False
            else:
                print("Connected to wifi.")
                print('Network config:', STATION_INTERFACE.ifconfig())
                if ValidateCredentials.secondaryAuthentication():  # Ensure saved credentials match server credentials
                    return True
    else:
        return True

def disconnect_WIFI():
    global STATION_INTERFACE
    if STATION_INTERFACE.isconnected():
        print("Disconnecting from outgoing WIFI...")
        STATION_INTERFACE.active(False)
        timeoutLimit = 30
        while STATION_INTERFACE.isconnected() and timeoutLimit:
            time.sleep(1)
            timeoutLimit -= 1
            lightShow([DISCONNECT, RESET], 1)
        if not timeoutLimit:
            print("Failed to disconnect within timeout period")
            return False
        else:
            print("Disconnected to wifi.")
            return True
    access_point_exc.ap_if.active(True)  # Turn on local access point
    return True


# MUST MODIFY CREDENTIALS FIRST IF ON FIRST RUN
def isConnected():
    global STATION_INTERFACE
    return STATION_INTERFACE.isconnected()