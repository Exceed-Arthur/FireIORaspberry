import time
import bricker
from FireIORaspb import EXC_SESSION_MODIFICATION_URL, EXC_SESSION_INDEX_URL, \
    DEVICE_PAYLOAD_IDENTIFIER, DEVICE_REQUEST_LISTENER_URL, USER_AUTHENTICATION_URL, DEVICE_USER
import urequests


def withAlert(content, alertText):
    return f'<script>alert("{alertText}");</script>{content}'


def withRedirect(content, redirect):
    return f'<script>setTimeout(function(){ window.location = redirect; },5000);</script>{content}'


def getJSON(url):
    r = urequests.get(url)
    if r.status_code >= 300 or r.status_code < 200:
        print("There was an error with your request to send a message. \n" +
              "Response Status: " + str(r.status_code))
        r.close()
        return False
    else:
        print("Successful Request...")
        r.close()
        return r.text


def ActivateUserSession():
    SessionModificationResponse = getJSON(f"{EXC_SESSION_MODIFICATION_URL}?username={DEVICE_USER.username}")
    if SessionModificationResponse['complete'] == 1:
        print("Modification Request Failed. Device User Activity failed to update.")
        return False
    else:
        print("Modification Request Succeeded. Device User Activity updated.")
        return True


def RefreshDeviceUserActivity():
    activeSessionIndex = getJSON(f"{EXC_SESSION_INDEX_URL}?username={DEVICE_USER.username}")
    if activeSessionIndex['active']:  # 0 if inactive and 1 if active
        DEVICE_USER.isActive = True
        print(f"DEVICE USER {DEVICE_USER} ACTIVE")
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


def UpdateDashboard(Data, USERNAME=DEVICE_USER.username):
    JSON = setToJSON(Data)
    return urequests.post(url=DEVICE_REQUEST_LISTENER_URL, data={USERNAME:JSON})


def sendPriorityAlert(url=DEVICE_REQUEST_LISTENER_URL, USERNAME=DEVICE_USER.username, json):
    JSON = setToJSON(json)
    JSON.update(timestamp=time.time())
    return urequests.post(url=url, data={USERNAME: JSON})


def userAuthenticated(url=USER_AUTHENTICATION_URL, USERNAME=DEVICE_USER.username, PASSWORD=DEVICE_USER.password):
    r = urequests.get(url=url, data=dict(username=USERNAME, password=bricker.hashBrick(PASSWORD)))
    if "200" in str(r.status_code):
        if "true" in r.text.lower():
            print(f"USER AUTHENTICATED {DEVICE_USER.username} {DEVICE_USER.password}")
            return True
    print(f"FAILED TO AUTHENTICATE {DEVICE_USER.username} {DEVICE_USER.password}")
    return False
