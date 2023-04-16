import network
import time
ap_if = network.WLAN(network.AP_IF)
credentialFile = "config.py"
exc_ssid = 'ExceedIO HomeSense WIFI'
exc_wpa = 'safe'


def connectAccessPoint(ssid1=exc_ssid, password1=exc_wpa):  # VOID
	global ap_if
	ap_if.config(ssid=ssid1, password=password1)
	ap_if.active(True)
	time.sleep(5)
	if ap_if.active():
		print(f"ACCESS POINT {ssid1} ACTIVATED [connect with pw: {password1}]")
		return True
	else:
		print(f"ACCESS POINT {ssid1} FAILED TO ACTIVATE")
		return False


def disconnectAccessPoint(ssid=exc_ssid):
	global ap_if
	ap_if.active(False)
	time.sleep(5)
	if ap_if.active():
		print(f"ACCESS POINT {ssid} DISCONNECTED")
		return True
	else:
		return False


def modifyCredentials(SSID_, PASS_):
	import fileIO
	for credential in [SSID_, PASS_]:
		fileIO.replaceFileFromString(credentialFile, fileIO.replaceVariableInPYFileString(credential))
	print(f"Modified {credentialFile} with new SSID and PASS {[SSID_, PASS_]}")


"""
SERVER WILL PERFORM THE "modifyCredentials" function upon receiving the proper credentials from the web-application.
Then, the Station will be free to connect (station_exc)
"""
