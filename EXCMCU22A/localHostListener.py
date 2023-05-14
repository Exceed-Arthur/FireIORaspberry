import fileIO
from WebFunctions import *
from template_content import *
import NetworkStation
import config
import UserProfile
import access_point_exc
from microdot import Microdot, Response, redirect
from microdot_session import set_session_secret_key
app = Microdot()

def runLocalServer():
    access_point_exc.connectAccessPoint()
    app.run(debug=True)

RELATIVE_BACK_END_SUCCESS_PATH = '/config/network/success2'
RELATIVE_FRONT_END_SUCCESS_PATH = '/config/network/success1'
set_session_secret_key('top-secret')
Response.default_content_type = 'text/html'

@app.route('/')
def home(req):
    return "I love niggers"

@app.get('/login')
@app.post('/login')
def login(req):
    if req.method == 'POST':
        username = req.form.get('username')
        password = req.form.get('password')
        UserProfile.DEVICE_USER.username = username
        UserProfile.DEVICE_USER.password = password  # Hash the password
        fileIO.replaceFileFromString('config.py', fileIO.replaceVariableInPYFileString('config.py', var='username', val=username))
        fileIO.replaceFileFromString('config.py', fileIO.replaceVariableInPYFileString('config.py', var='password', val=password))
        print("Received post request and modified user credentials")
        return redirect('/config/network')  # Try to get real outgoing WIFI from home network, obtain cred
    if config.username is None:
        return BASE_TEMPLATE.format(dashboardLocation=DASHBOARD_LOCATION_PATH,content=LOGGED_OUT)  # NO HARDCODED USERNAME, START OVER
    elif config.password is None:
        return BASE_TEMPLATE.format(dashboardLocation=DASHBOARD_LOCATION_PATH,content=LOGGED_OUT)  # NO HARDCODES PASSWORD, START OVER
    else:
        return redirect('/config/network')  # Try to get real outgoing WIFI from home network, obtain cred


@app.get('/config/network')
@app.post('/config/network')
def configNetwork(req):
    ssid_, wpa_ = None, None
    if req.method == 'POST':
        ssid_ = req.form.get('ssid')
        wpa_ = req.form.get('wpa')
        if not NetworkStation.STATION_INTERFACE.isconnected():
            print("STATION NOT CONNECTED YET...INSERTING NEW CREDENTIALS")
            access_point_exc.modifyCredentials(ssid_, wpa_)
            return redirect('/config/network')  # Run again with credentials this time
        else:
            print("REDIRECTING TO SERVER HOSTED DASHBOARD FOR EXC SENSORS...")
            LightControl.lightShow([LED.CONNECT], 10)
            LightControl.light(LED_PIN=LED_PINS.CONNECT)
            return redirect('/config/network/success1')
    if NetworkStation.STATION_INTERFACE.isconnected():
        print("STATION INTERFACE IS CONNECTED DETECTED FROM GET REQUEST")
        return BASE_TEMPLATE.format(dashboardLocation=DASHBOARD_LOCATION_PATH,content=SUCCESSFUL_WIFI_SETUP.format(
            username=DEVICE_USER.username))
    if config.WIFI_SSID and config.WIFI_PASSWORD:
        ssid_ = config.WIFI_SSID
        wpa_ = config.WIFI_PASSWORD
        print(f"CONFIG NETWORK: {ssid_, wpa_}")
        NetworkStation.connect_WIFI()
        if NetworkStation.STATION_INTERFACE.isconnected():
            LightControl.lightShow([LED.CONNECT], 10)
            LightControl.light(LED_PIN=LED_PINS.CONNECT)
            monitorSensors()
            print("Network configured through re-check! Monitoring Sensors now.")
    if ssid_ is None:
        return BASE_TEMPLATE.format(dashboardLocation=DASHBOARD_LOCATION_PATH,content=withAlert(NETWORK_CONFIG_PG, alertText="Please enter your network name in the box."))
    elif wpa_ is None:
        return BASE_TEMPLATE.format(dashboardLocation=DASHBOARD_LOCATION_PATH,
            content=withAlert(NETWORK_CONFIG_PG, alertText="Please enter your network passkey in the box."))
    else:
        return redirect(RELATIVE_FRONT_END_SUCCESS_PATH)



@app.route('/logout')
def logout():
    DEVICE_USER.username = None
    DEVICE_USER.password = None
    fileIO.replaceFileFromString('config.py', fileIO.replaceFileFromString('config.py', fileIO.replaceVariableInPYFileString('config.py', var='username', val=None)))
    fileIO.replaceFileFromString('config.py', fileIO.replaceFileFromString('config.py', fileIO.replaceVariableInPYFileString('config.py', var='password', val=None)))
    return redirect('/login')


@app.get('/config/network/success1')
@app.post('/config/network/success1')
def success_frontEnd():
    print("Serving front end success page for wifi setup.")
    return BASE_TEMPLATE.format(dashboardLocation=DASHBOARD_LOCATION_PATH,content=withRedirect(SUCCESSFUL_WIFI_SETUP, RELATIVE_BACK_END_SUCCESS_PATH))


@app.get('/config/network/success2')
@app.post('/config/network/success2')
def success_backEnd():
    access_point_exc.disconnectAccessPoint()
    print("ATTEMPTING TO START SERVICE PICKER FROM BACKEND")
    main.servicePicker()  # Starting service picker
    return True


if __name__ == '__main__':
    app.run()
