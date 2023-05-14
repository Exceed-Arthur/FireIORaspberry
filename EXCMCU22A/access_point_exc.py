import network
ap_if = network.WLAN(network.AP_IF)
credentialFile = "config.py"
exc_ssid = 'ExceedIO HomeSense WIFI'
exc_wpa = 'homesense'




def connectAccessPoint():  # VOID
    global ap_if
    ap_if.active(False)
    ap_if.config(ssid=exc_ssid, password=exc_wpa)
    ap_if.active(True)
    print(ap_if.ifconfig())
    if ap_if.active():
        print(f"ACCESS POINT {exc_ssid} ACTIVATED [connect with pw: {exc_wpa}]")
        return True
    else:
        print(f"ACCESS POINT {exc_ssid} FAILED TO ACTIVATE")
        return False


def disconnectAccessPoint(ssid=exc_ssid):
    global ap_if
    ap_if.active(False)
    if not ap_if.active():
        print(f"ACCESS POINT {ssid} DISCONNECTED")
        return True
    else:
        return False


def modifyCredentials(SSID_, PASS_):
    import fileIO
    fileIO.replaceFileFromString(credentialFile, fileIO.replaceVariableInPYFileString(credentialFile, 'WIFI_SSID', SSID_))
    fileIO.replaceFileFromString(credentialFile, fileIO.replaceVariableInPYFileString(credentialFile, 'WIFI_PASSWORD', PASS_))
    print(f"Modified {credentialFile} with new SSID and PASS {[SSID_, PASS_]}")


"""
SERVER WILL PERFORM THE "modifyCredentials" function upon receiving the proper credentials from the web-application.
Then, the Station will be free to connect (station_exc)
"""
