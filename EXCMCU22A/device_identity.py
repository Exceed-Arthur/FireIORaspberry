import random


def randomID():
    device_id = ""
    for i in range(8):
        if random.randint(1) > 0:
            device_id += "1"
        else:
            device_id += "0"

