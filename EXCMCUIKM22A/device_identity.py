import random
def randomID():
    device_id = ""
    for i in range(8):
        if random.random() > 0.5:
            device_id += "1"
        else:
            device_id += "0"

