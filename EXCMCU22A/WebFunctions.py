from CONSTANT_DEFS import *
import CONSTANT_DEFS
import urequests
import UserProfile
from UserProfile import DEVICE_USER
import config
import json

def withAlert(content, alertText):
    return f'<script>alert("{alertText}");</script>{content}'


def withRedirect(content, redirect):
    return r"<script>setTimeout(function(){ window.location = redirect; },5000);</script>{content}"


def getJSON(url):
    r = urequests.get(url)
    if r.status_code >= 300 or r.status_code < 200:
        print("There was an error with your request to send a message. \n" +
              "Response Status: " + str(r.status_code))
        return False
    else:
        print("Successful Request...")
        return json.loads(r.content.decode('utf-8'))


def ActivateUserSession():
    SessionModificationResponse = getJSON(f"{EXC_SESSION_MODIFICATION_URL}?username={config.username}")
    if SessionModificationResponse['complete'] == 1:
        print("Modification Request Failed. Device User Activity failed to update.")
        return False
    else:
        print("Modification Request Succeeded. Device User Activity updated.")
        return True


def RefreshDeviceUserActivity():
    activeSessionIndex = getJSON(f"{EXC_SESSION_INDEX_URL}?username={config.username}")
    if activeSessionIndex['active']:  # 0 if inactive and 1 if active
        UserProfile.DEVICE_USER.isActive = True
        print(f"DEVICE USER {config.username} ACTIVE")
    else:
        DEVICE_USER.isActive = False
        print(f"DEVICE USER {DEVICE_USER} IN-ACTIVE")


def getOwnIP():  # Obtain IP of this device
    r = urequests.get('http://icanhazip.com')
    if "200" in str(r.status_code):
        return r.text.replace("\n", "")
    return False


def setToJSON(JSON_SET):
    JSON = {}
    JSON_SET = list(JSON_SET)
    for Obj in JSON_SET:
        JSON.update({f"response_{JSON_SET.index(Obj)}": {DEVICE_PAYLOAD_IDENTIFIER: Obj, "timestamp": time.time()}})
    return JSON


def UpdateDashboard(Data, USERNAME=UserProfile.DEVICE_USER.username):
    JSON = setToJSON(Data)
    return urequests.post(url=CONSTANT_DEFS.DEVICE_REQUEST_LISTENER_URL, data={USERNAME:JSON})


def sendPriorityAlert(json):
    JSON = setToJSON(json)
    JSON.update(timestamp=time.time())
    return urequests.post(url=CONSTANT_DEFS.DEVICE_REQUEST_LISTENER_URL, data={config.username: JSON})


def userAuthenticated():
    r = getJSON(f"{CONSTANT_DEFS.USER_AUTHENTICATION_URL}?username={config.username}&password={config.password}")
    print(str(r))
    if "true" in str(r):
            print(f"USER AUTHENTICATED {DEVICE_USER.username} {DEVICE_USER.password}")
            return True
    print(f"FAILED TO AUTHENTICATE {DEVICE_USER.username} {DEVICE_USER.password}")
    return False
