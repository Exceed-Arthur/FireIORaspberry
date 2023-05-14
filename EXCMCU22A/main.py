import WebFunctions
import localHostListener
import access_point_exc
import config
from DEFINITIONS import *
from UserProfile import *
from CONSTANT_DEFS import *
import NetworkStation
import access_point_exc
import LightControl
import os
import time
from microdot import Microdot
import device_identity
from VOLATILE_DEVICE_FILE import *
import os
import device_id



if not device_id.identifier:   
    with open("device_id.py", "w+") as f:
        f.write(f"identifier = {device_identity.randomID()}")
        f.close()


device_sequence = device_id.identifier


def localServer():
    localHostListener.runLocalServer()
    
    
def writeCodesToFile(filename=LONG_TERM_DEVICE_FILE, codes=None):  # Data segment in part 2,  prefix in part 1 (index 0)
    OF_STR = ""
    if os.stat(LONG_TERM_DEVICE_FILE)[6] > 1000000:
        try:
            os.remove(LONG_TERM_DEVICE_FILE)
        except:
            print(f"UNABLE TO REMOVE {LONG_TERM_DEVICE_FILE}")
   # except:
   #     print(f"Unable to retrieve file size for {LONG_TERM_DEVICE_FILE}")
    for code in codes:
        OF_STR += f"{code[0:14]} {code[14:24]} {time.time()} \n"
    with open(filename, 'a') as OF:
        OF.write(OF_STR)
        OF.close()


def ReplaceDeviceFile(filename=LONG_TERM_DEVICE_FILE, lines=None):  # Data segment in part 2, prefix in part 1 (index 0)
    OF_STR = ""
    for code in lines:
        OF_STR += f"{code[0]} {code[1]} {time.time()} \n"
    with open(filename, 'w+') as OF:
        OF.write(OF_STR)
        OF.close()


def extractDevicesFromFile(
        filename=LONG_TERM_DEVICE_FILE) -> set:  # Retrieve Most Recent Non-Duplicate Devices and data
    lines = []
    devices = set()  # Each device is a dict
    prefixes = set()  # track any devices already added
    with open(filename, 'r') as IF:
        IF.readlines()
    lines.reverse()  # Reverse to get most recent entries first
    real_lines = []
    for line in lines:
        prefix = line.split(" ")[0]  # Device prefix Type + ID
        data_seg = line.split(f"{prefix} ")[1].split(" ")[0]
        time_ = line.split(f"{data_seg} ")[1]
        if prefix not in prefixes:
            prefixes.add(prefix)
            devices.add({"device": prefix, "data": data_seg, "time": time_, "type": prefix[0:6]})
            real_lines.append(prefix + data_seg)
    ReplaceDeviceFile(lines=real_lines)
    return devices


def ConvertedFlameSensorData(RawFlameGuardData: str) -> dict:  # Convert 10 bit data into multi-state information
    if RawFlameGuardData[0:10] == "0000000010":
        print("Retrieved device initialization for FlameGuard")
        return {"status": "Connecting or getting ready"}
    else:
        intensity = int(RawFlameGuardData[0:8], 2)
        print(f"Relative intensity of Flame Sensor: {intensity}")
        RISING = RawFlameGuardData[8: 10]
        if not RISING:
            flame = OFF
        else:
            flame = ON
        return {"intensity": intensity, "flame": flame}


def ConvertedGasSensorData(RawGasData: str, Sensor_Type) -> dict:  # Convert 10 bit data into multi-state information
    if not isBinary(RawGasData):
        print(f"Invalid binary representation: {RawGasData} // Raw Gas Data")
        return False
    if RawGasData[0:10] == "0000000010":
        print("Retrieved device initialization for Gas Sensor")
        return {"status": "Connecting or getting ready"}
    else:
        intensity = int(RawGasData[0:8], 2)
        print(f"Relative intensity of Gas Sensor: {intensity/255*100}")  # Get Percentage because 255 is max intensity
        RISING = RawGasData[8: 10]
        if not RISING:
            flame = OFF
        else:
            flame = ON
        gasIndex = {"110001": "Methane", "110010": "Carbon Monoxide", "110011": "Hydrogen Sulfide", "110101": "Smoke"}
        dictionary_representation = {"intensity": intensity, "Gas Detected": flame, "Gas Name:": gasIndex[Sensor_Type]}
        print(f"Converted {RawGasData}, {Sensor_Type} to {dictionary_representation}")
        return dictionary_representation


def ConvertedFridgeSensorData(RawFridgeSenseData: str) -> dict:
    if not isBinary(RawFridgeSenseData):
        print(f"Invalid binary representation: {RawFridgeSenseData} for ConvertedFridgeSensorData")
        return False
    Fridge_Temperature_Data = RawFridgeSenseData[0:8]
    if RawFridgeSenseData[0:10] == "0000000010":
        print("Retrieved device initialization for FridgeSense")
        return {"status": "Connecting or getting ready"}
    else:
        Temperature = int(Fridge_Temperature_Data, 2) + ABSOLUTE_MINIMUM_TEMP
        FLUCTUATION = int(RawFridgeSenseData[9])  # if the 10th bit is positive, the temperature changed significantly
        NEGATIVE_SIGN_BIT = int(RawFridgeSenseData[8])  # if 9th bit is 1 then it shifted in negative direction (cooled)
        if NEGATIVE_SIGN_BIT and FLUCTUATION:
            FLUCTUATION *= -1  # Invert Sign
        print(f"Retrieved Fluctuation {FLUCTUATION} at {Temperature} Degrees Celsius")
        return {"fluctuation": FLUCTUATION}

def writeDeviceFileFromRF(RFCodes):  # Use RF Signals from satellite devices to update onboard device file
    if len(RFCodes) > 0:
        for code in RFCodes:
            DEVICE_TYPE = code[0:6]  # First 6 bits are the type of hardware unit
            DEVICE_PREFIX = code[0:14]  # First 14 bits = 6-bit type + 8-bit ID
            DATA_SEGMENT = code[14:24]  # Last 10 bits reserved for data segment
            DEVICE_FILE.update({DEVICE_PREFIX: {'data': DATA_SEGMENT, 'connected': TRUE, 'type': DEVICE_TYPE}})
        writeCodesToFile(codes=RFCodes)  # Save the time-stamp of all devices to file
        print(f"Wrote device codes to file {RFCodes}")
    print("NO CODES RECEIVED...SCAN CONTINUES...")
def collectOffBoardSensors():  # Use device file to build variable of device file
    import VOLATILE_DEVICE_FILE
    Devices = list(extractDevicesFromFile(VOLATILE_DEVICE_FILE.DEVICE_FILE))  # Dictionaries of Device data
    JSON_Devices = set()  # List of devices and their data
    for device in Devices:  # devices.add({"device": prefix, "data": data_seg, "time": time_, "type": prefix[0:6]})
        device_prefix = device["device"]
        device = Devices[device_prefix]
        data = device['data']
        device_type = device_prefix[0:6]
        device.update(dict(name=(HomeSenseModelNameDict[device_type])))
        if device_type == FRIDGE_SENSE_SERIAL_TYPE:
            device.update(ConvertedFridgeSensorData(data))
        elif device_type == FLAME_GUARD_SERIAL_TYPE:
            device.update(ConvertedFlameSensorData(data))
        elif device_type in gas_type_serial_prefixes:
            device.update(ConvertedGasSensorData(data, type_serial))
        JSON_Devices.add(device)
    return JSON_Devices


def monitorSensors():
    print("STARTING MONITOR SENSORS")
    MONITORING = True  # Keep monitoring if network enabled
    rfReceiver.activate()
    WebFunctions.RefreshDeviceUserActivity()  # Determine if user is active, and send non-priority requests if so
    while MONITORING:
        for i in range(SENSOR_READ_LIMIT):
            RF_CODES = rfReceiver.normalizeRFCodes(rfReceiver.scanRFCodes())  # Returns set of normalized binary codes
            writeDeviceFileFromRF(RF_CODES)  # Cache and update device file containing user's home devices
            PriorityNetworkRequestData = set()  # Save Network Capacity By Limiting Immediate Requests
            if PriorityNetworkRequestData:
                WebFunctions.sendPriorityAlert(url=EXC_DEVICE_LISTENER__URL, json=PriorityNetworkRequestData)
        NetworkRequestData = set()
        WebFunctions.RefreshDeviceUserActivity()  # Determine if user is active, and send non-priority requests if so
        HomeUnitDeviceSnapshot = {"device": HomeSenseModelNameDict['000001'], 'connected': True}
        for device in collectOffBoardSensors():  # Extract Devices and their data from RF Codes (translated):
            NetworkRequestData.add(device)
        if DEVICE_USER.isActive:
            NetworkRequestData.add(HomeUnitDeviceSnapshot)
    
            WebFunctions.UpdateDashboard(NetworkRequestData)  # Send post request to reflect user profile and device states
        if not NetworkStation.STATION_INTERFACE.isconnected():
            LightControl.blink(DISCONNECT, 2)
            LightControl.light(LED_PIN=DISCONNECT)
            MONITORING = NetworkStation.connect_WIFI()



def servicePicker():
    print("SERVICE PICKER")
    if (config.username is None or config.password is None) or (config.WIFI_SSID is None or config.password is None):
        print(f"SERVICE PICKER OBTAINED NO CREDENTIALS AND NEEDS TO START SERVER LOCALLY")
        NetworkStation.disconnect_WIFI()
        localServer()  # Ready local network socket to enable set-up web-app
        LightControl.lightShow([RESET, TALK], 6)
    if not NetworkStation.STATION_INTERFACE.isconnected(): # Check if connected
        print("SERVICE PICKER DETECTED NO CONNECTION YET")
        if NetworkStation.connect_WIFI() == False:
            localServer()  # Ready local network socket to enable set-up web-app
        else:
            print("SERVICE PICKER INTIATED AND CONNECTED A WIFI SIGNAL")
            servicePicker()
    else: # connected and has credentials
        print("SERVICE PICKER DETECTED EXISTING CONNECTION")
        print(config.username, config.password)
        print("SERVICE PICKER DETECTED A CONNECTION AND CREDENTIALS")
        monitorSensors()
        print("EXITED MONITORING FROM SERVICE PICKER")
            
            


servicePicker()