HomeSenseTypeDict = {"001010": "Control Hub + Integrated Kitchen Monitoring",
                     "100000": "Wifi Enabled Flame Sensor", "100100": "Wifi Enabled Fridge Monitor"}


def normalizeID(binaryRep: str):
    return int(binaryRep, 2)  # Get base two integer from binary representation of number
