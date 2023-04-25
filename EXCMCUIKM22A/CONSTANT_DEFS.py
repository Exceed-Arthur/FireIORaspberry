EXC_SESSION_INDEX_URL = "https://homi.herokuapp.com/ActiveSessionIndex"
EXC_DEVICE_LISTENER_URL = "https://homi.herokuapp.com/DeviceRequestListener"
USER_AUTHENTICATION_URL = "https://homi.herokuapp.com/token/auth/homi"
EXC_SESSION_MODIFICATION_URL = "https://homi.herokuapp.com/ModifySessionIndex"
DASHBOARD_LOCATION_PATH = "https://homi.herokuapp.com/Dashboard"
DEVICE_REQUEST_LISTENER_URL = "https://homi.herokuapp.com/DeviceRequestListener"
HomeSenseModelNameDict = {"000000": "Homi Hub", "000001": "HomeSense Hub + Kitchen Monitor", "100000": "CandleGuard",
                          "110000": "FridgeSense", "110011": "GasWizard: Hydrogen", "110010": "GasWizard: Carbon Monoxide", "110001": "GasWizard: Methane", "110101": "GasWizard: Smoke"}
FLAME_GUARD_SERIAL_PREFIX = "EXCFRSADAT2"
FRIDGE_SENSE_SERIAL_TYPE = "110000"
GASWIZARD_SMOKE_SERIAL_TYPE = "110101"
GASWIZARD_METHANE_SERIAL_TYPE = "110001"
GASWIZARD_HYDROGEN_SERIAL_TYPE = "110011"
GASWIZARD_CARBON_SERIAL_TYPE = "110010"
FLAME_GUARD_SERIAL_TYPE = "100000"
DEVICE_PAYLOAD_IDENTIFIER = "device_payload"
FRIDGE_SENSE_SERIAL_PREFIX = "EXCFLS22A1"

HomeSenseSerialPrefixDict = {"110001": "EXCGASFMET", "110010": "EXCGASFCO","110011":"EXCGASFHYS", "110101": "EXCGASFSMK", "100000": "EXCFLS22A", "110000": "EXCFRSADA22A", "000000": "EXCMCU22A", "000001": "EXCMCUIKM22A"}
gas_type_serial_prefixes = [GASWIZARD_SMOKE_SERIAL_TYPE, GASWIZARD_METHANE_SERIAL_TYPE, GASWIZARD_HYDROGEN_SERIAL_TYPE, GASWIZARD_CARBON_SERIAL_TYPE]

LONG_TERM_DEVICE_FILE = 'device_file.txt'
SENSOR_READ_LIMIT = 60  # NUMBER OF READS PER INTERVAL
MAX_VAL_8_BIT = 255  # Easily Represented In Binary
ABSOLUTE_MINIMUM_TEMP = -40  # AHT20 TEMP DETECT RANGE MIN  # ADD TO ACTUAL TEMPERATURE TO TRANSMIT THE DIFFERENCE
ABSOLUTE_MAXIMUM_TEMP = 85  # CELSIUS AHT20 MAXIMUM
DIGITAL_MAX_VALUE = 1  # 0 and 1 for Digital Signal Read Possibilities
AHT20_ID = 0  # I2C ID
RF_READ_LIMIT = 25  # Reads before giving up on RF Receive
PROXIMITY_THRESHOLD = 3  # 3 Reads per interval is considered a human presence
BASIC_THRESHOLD = 3  # UnCalibrated Threshold Value
ANALOG_MAXIMUM_READ = 65535  # Highest Possible Value In MicroPy for ANALOG Reads
ANALOG_SENSOR_8BIT_DIVISOR = 257  # 65535 IS MAX ANALOG READING, MAX VALUE ADJUSTED TO 255
GENERIC_SENSOR_NAME = f"Unassigned Homi Sensor"
DIGITAL_SIGNAL_THRESHOLD = 3  # Number of reads considered to be significant during read interval
EIGHT_BIT_FILLER = "00000000"
SIX_BIT_FILLER = "000000"
TRUE = HIGH = ON = LIT = PRESENT = 1
NOT = LOW = OFF = 0
MAIN_UNIT_ID = "00001010"  # 10 IN BINARY 8 BIT
MAIN_UNIT_TYPE = "001010"  # 10 IN BINARY 6 BIT
FLAME_ADC_MINIMUM = 750
FLAME_THRESHOLD = 3  # Number of reads considered to be significant during read interval
FLAMMABLE_GAS_THRESHOLD = 3  # Number of reads considered to be significant during read interval
DASHBOARD_NAMESERVER = "https://homi.herokuapp.com/"
DASHBOARD_PATH = "/homi/dashboard"
DASHBOARD_LOCATION = DASHBOARD_NAMESERVER + DASHBOARD_PATH
TEMPERATURE_STABILITY_DEAD_ZONE = 7  # Amount of negligible temperature fluctuations in a single interval
HUMIDITY_STABILITY_DEAD_ZONE = 7  # Amount of negligible temperature fluctuations in a single interval
device_name = "Exceed IO Homi/HomeSense Homi Hub + Integrated Kitchen Monitoring"
device_category = "000000" # STATIC FOR ALL VERSIONS OF THIS DEVICE
READING_RF = True  # Toggle this when you start various sensor monitoring procedures