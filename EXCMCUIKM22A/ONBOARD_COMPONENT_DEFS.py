from Sensors import *
from RFReceiver433 import RFReceiver433
from PIN_DEFS import *


FlammableGasS = FlammableGasSensor()  # ANALOG FLAMMABLE GAS SENSOR
TempHumidityS = AHT20()  # ADAFRUIT AHT20
ProximityS = ProximitySensor()  # MICROWAVE DOPPLER PROX SENSOR
ONBOARD_SENSORS = set(list([FlammableGasS, TempHumidityS, ProximityS]))
rfReceiver = RFReceiver433(PIN_NUMBER=RFReceiver)  # HI LET GO RF RECEIVER 433 mhz
for sensor in ONBOARD_SENSORS:  # UNIFY BASED ON ADDRESSING SCHEME
    sensor.ID = MAIN_UNIT_ID  # ALL ONBOARD SENSORS PART OF MAIN UNIT
    sensor.TYPE = MAIN_UNIT_TYPE  # ALL ONBOARD SENSORS PART OF MAIN UNIT