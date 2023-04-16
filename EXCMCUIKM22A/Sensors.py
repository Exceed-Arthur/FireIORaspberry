import miscFuncs
from CONSTANT_DEFS import *
from PIN_DEFS import *
import ahtx0
from machine import Pin, I2C, ADC


class HomeSenseUnit:
    def __init__(self, TYPE_=SIX_BIT_FILLER, ID_=EIGHT_BIT_FILLER, NAME=GENERIC_SENSOR_NAME):
        self.TYPE = TYPE_
        self.ID = ID_
        self.NAME = NAME
        self.DEVICE_PREFIX = self.TYPE + self.ID

    def getDevicePrefix(self):
        self.DEVICE_PREFIX = self.TYPE + self.ID
        return self.DEVICE_PREFIX

    def HomeSenseIOID(self):
        return f"{self.NAME} #{self.ID} -> "

    def DEVICE_COMPOSITE_KEY(self):
        print(f"Generated composite key: {self.TYPE + self.ID}")
        return str(self.TYPE + self.ID)

    def EXC_PRINT(self, text):
        print(f"{self.HomeSenseIOID()}{text}")

    def isSameDevice(self, HomeSU):
        if (HomeSU.TYPE == self.TYPE) and (HomeSU.ID == self.ID):
            print(f"{HomeSU} is the same as {self}")
            return True
        return False

    def isSameDeviceFamily(self, HomeSU):
        if HomeSU.TYPE == self.TYPE:
            print(f"{HomeSU} is the same model of sensor as {self}, but not the same sensor itself.")
            return True
        return False


class BasicSensor(HomeSenseUnit):
    def __init__(self, SIGNAL_THRESHOLD=BASIC_THRESHOLD, IS_ANALOG=False):
        super().__init__()  # Get Unique Addressing Scheme for HomeSense
        self.READ_COUNT = SENSOR_READ_LIMIT  # Number of measurements
        self.HIGH_SIGNALS = 0  # Increment on every high read
        self.SIGNAL_THRESHOLD = SIGNAL_THRESHOLD
        self.IS_ANALOG = IS_ANALOG
        self.JSON = dict(name=self.NAME, type=self.TYPE, id=self.ID, device=self.getDevicePrefix())  # Standard addressing scheme

    def getIntensity(self):
        return float(float(self.HIGH_SIGNALS) / float(self.READ_COUNT))

    def get8BitIntensity(self):
        return miscFuncs.get_bin(self.getIntensity() * 100)  # Convert Percentile to Binary Representation in 8 bits


class I2CSensor(HomeSenseUnit):
    def __int__(self, SDA_PIN=SDA1, SCL_PIN=SCL1):
        self.SDA_PIN = SDA_PIN
        self.SCL_PIN = SCL_PIN


class AnalogSensor(BasicSensor):
    def __int__(self, SIGNAL_PIN, MAX_VALUE=MAX_VAL_8_BIT, READ_COUNT=SENSOR_READ_LIMIT, IS_ANALOG=True):
        super().__init__(IS_ANALOG=True)  # Get Unique Addressing Scheme for HomeSense
        self.SIGNAL_PIN = SIGNAL_PIN
        self.MAX_VALUE = MAX_VALUE  # 0-255
        self.HIGH_SIGNAL_VALUE = ANALOG_MAXIMUM_READ  # 65535
        self.ADC_Converter = ADC(SIGNAL_PIN)  # Create usable ADC object for the pin
        print(f"Instantiated {self.HomeSenseIOID()}")

    def basicSensorRead(self):
        analog_raw = self.ADC_Converter.read_u16() - FLAME_ADC_MINIMUM  # Raw range 0-65535
        if analog_raw < 0:
            analog_raw = 0
        adjusted_signal = round(analog_raw / ANALOG_SENSOR_8BIT_DIVISOR)  # Creates range from 0-255
        self.EXC_PRINT(f"Raw Analog Sig: {analog_raw}\nAdjusted Signal: {adjusted_signal}")
        return adjusted_signal  # 0-255




class FlammableGasSensor(AnalogSensor):
    def __init__(self, SIGNAL_PIN=FLAMMABLE_GAS_SENSOR):
        # call parent constructor to set MAX_VALUE and READ_COUNT
        super().__init__(SIGNAL_THRESHOLD=FLAMMABLE_GAS_THRESHOLD)  # Basic Sensor
        self.SIGNAL_PIN = SIGNAL_PIN

    def flammableGasDetected(self):
        return self.HIGH_SIGNALS >= self.SIGNAL_THRESHOLD  # Adjustable sensitivity to flame-like light

    def getJSONComponent(self):
        specific_dict = self.JSON  # BASIC ADDRESSING INFO
        specific_dict.update(dict(flammableGas=self.flammableGasDetected(), intensity=self.getIntensity()))
        return specific_dict

    def advancedSensorRead(self, RequestData: dict, SIGNAL_ACCUMULATOR: int):
        if self.basicSensorRead():
            RequestData.update({"priority": HIGH, "device": self.DEVICE_COMPOSITE_KEY(), "flammableGas": PRESENT,
                                "intensity": self.get8BitIntensity()})
            SIGNAL_ACCUMULATOR += 1
        return RequestData, SIGNAL_ACCUMULATOR

    @staticmethod
    def RFJSONComponent(RFCode):  # Radio frequency of
        device_type = RFCode[0:6]
        device_id = RFCode[6:14]
        device_data = RFCode[14:24]
        device_intensity = device_data[0:8]
        flame = device_data[-1]  # Negative bit is state[0], state[1]
        name = f"{HomeSenseModelNameDict[device_type]} {int(device_id, 2)}"
        return dict(name=name, flammableGas=int(flame), intensity=device_intensity)


class DigitalSensor(BasicSensor):
    def __int__(self, SIGNAL_PIN, MAX_VALUE=DIGITAL_MAX_VALUE, READ_COUNT=SENSOR_READ_LIMIT,
                SIGNAL_THRESHOLD=BASIC_THRESHOLD):
        super().__init__()
        self.SIGNAL_PIN = SIGNAL_PIN
        self.SIGNAL_THRESHOLD = DIGITAL_SIGNAL_THRESHOLD
        self.PIN_INTERFACE = Pin(SIGNAL_PIN, Pin.OUT)  # Create Pin Object to Read as Output

    def basicSensorRead(self):
        digital_raw = self.PIN_INTERFACE.value()  # 0-1
        print(f"Raw Digital Sig: {digital_raw}")
        return digital_raw


class ProximitySensor(DigitalSensor):  # High if someone present during read
    def __init__(self, SIGNAL_PIN=PROXIMITY_SENSOR, HIGH_SIGNALS=0, SIGNAL_THRESHOLD=PROXIMITY_THRESHOLD):
        # call parent constructor to set MAX_VALUE and READ_COUNT
        super().__init__(SIGNAL_PIN)
        self.SIGNAL_THRESHOLD = SIGNAL_THRESHOLD  # Number of reads considered to be significant during read interval
        self.HIGH_SIGNALS = HIGH_SIGNALS  # Increment This Every Time Someone is Detected
        self.ACTIVITY_DETECTED = False

    def presenceDetected(self):
        return self.HIGH_SIGNALS >= self.SIGNAL_THRESHOLD  # Adjustable sensitivity to proximal people/objects

    def getJSONComponent(self):
        specific_dict = self.JSON  # BASIC ADDRESSING INFO
        intensity = self.getIntensity()
        if intensity > float(1):
            intensity = float(1)
            print(f"{self.HomeSenseIOID()}MAX INTENSITY DETECTED")
        specific_dict.update(dict(populated=self.presenceDetected(), intensity=intensity))
        return specific_dict

    @staticmethod
    def RFJSONComponent(RFCode):  # Radio frequency of
        device_type = RFCode[0:6]
        device_id = RFCode[6:14]
        device_data = RFCode[14:24]
        device_intensity = device_data[0:8]
        flame = device_data[-1]  # Negative bit is state[0], state[1]
        name = f"{HomeSenseModelNameDict[device_type]} {int(device_id, 2)}"
        return dict(name=name, populated=int(flame), intensity=device_intensity)


class AHT20(I2CSensor):
    def __init__(self):
        super().__init__()  # Get Unique Addressing Scheme for HomeSense
        i2c = I2C(id=1, scl=Pin(SCL1), sda=Pin(SDA1))
        self.sensor = ahtx0.AHT20(i2c)
        self.warmingEvents = 0  # Number of independent temperature increases within interval
        self.temperatureFluctuation = 0  # Magnitude of temperature fluctuations weighed against each other (+/-)
        self.READ_COUNT = 0  # Reads during interval
        self.JSON = dict(name=self.NAME, type=self.TYPE, id=self.ID)  # Standard addressing scheme

    def temperatureDirection(self) -> int:
        if self.warmingEvents >= ((SENSOR_READ_LIMIT / 2) + TEMPERATURE_STABILITY_DEAD_ZONE):
            return 1  # Environment warming (open) if increasing half the time
        elif self.warmingEvents <= ((SENSOR_READ_LIMIT / 2) + (TEMPERATURE_STABILITY_DEAD_ZONE * 2)):
            return -1  # Cooling Down Environment Detected
        else:
            return 0  # Stable Temperature Detected

    def isWarming(self):
        return self.warmingEvents >= (SENSOR_READ_LIMIT / 2)  # Environment warming (open) if increasing half the time

    def getTemperatureChange(self):
        tempFlux = self.temperatureFluctuation
        self.temperatureFluctuation = 0
        print(f"{self.HomeSenseIOID()}Temperature Fluctuation: {tempFlux}\n...Resetting to 0.")
        return tempFlux

    def getTemperature(self):
        print("\nTemperature: %0.2f C" % self.sensor.temperature)
        return self.sensor.temperature

    def getHumidity(self):
        print("Humidity: %0.2f %%" % self.sensor.relative_humidity)
        return self.sensor.temperature

    def getJSONComponent(self):
        specific_dict = self.JSON  # BASIC ADDRESSING INFO
        specific_dict.update(dict(state=self.getTemperatureChange(), temperature=self.getTemperature(),
                                  humidity=self.getHumidity(),
                                  temperatureChange=self.getTemperatureChange()))
        return specific_dict
