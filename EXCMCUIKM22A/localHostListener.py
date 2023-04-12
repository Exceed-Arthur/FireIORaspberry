import fileIO
import main
from WebFunctions import *
from template_content import *
from microdot import Microdot, Response, redirect
from microdot_session import set_session_secret_key
RELATIVE_BACK_END_SUCCESS_PATH = '/config/network/success2'
RELATIVE_FRONT_END_SUCCESS_PATH = '/config/network/success1'
app = Microdot()
set_session_secret_key('top-secret')
Response.default_content_type = 'text/html'


@app.get('/login')
@app.post('/login')
def login(req):
    if config.username and config.password:
        return redirect(f'/config/network')
    if req.method == 'POST':
        username = req.form.get('username')
        password = req.form.get('password')
        DEVICE_USER.username = username
        DEVICE_USER.password = bricker.hashBrick(password)  # Hash the password
        fileIO.replaceVariableInPYFileString('config.py', var='username', val=DEVICE_USER.username)
        fileIO.replaceVariableInPYFileString('config.py', var='password', val=DEVICE_USER.password)
        print("Received post request and modified user credentials")
    elif req.method == 'GET':
        username = req.args.get('username')
        password = req.args.get('username')
        DEVICE_USER.username = username
        DEVICE_USER.password = bricker.hashBrick(password)  # Hash the password
        fileIO.replaceFileFromString('config.py', fileIO.replaceVariableInPYFileString('config.py', var='username',
                                                                                       val=DEVICE_USER.username))
        fileIO.replaceVariableInPYFileString('config.py', var='password', val=DEVICE_USER.password)
        print("Received get request and modified user credentials")
        return dict(completed=True, username=username, password=DEVICE_USER.password)

    if config.username is None:
        return BASE_TEMPLATE.format(content=LOGGED_OUT)  # NO HARDCODED USERNAME, START OVER
    elif config.password is None:
        return BASE_TEMPLATE.format(content=LOGGED_OUT)  # NO HARDCODES PASSWORD, START OVER
    else:
        return redirect('/config/network/')  # Try to get real outgoing WIFI from home network, obtain cred


@app.get('/config/network')
@app.post('/config/network')
def configNetwork(req):
    ssid_, wpa_ = None, None
    if NetworkStation.isConnected():
        return BASE_TEMPLATE.format(content=SUCCESSFUL_WIFI_SETUP.format(
            username=DEVICE_USER.username))
    if config.WIFI_SSID and config.WIFI_PASSWORD:
        ssid_ = config.WIFI_SSID
        wpa_ = config.WIFI_PASSWORD
        NetworkStation.connect_WIFI()
        if NetworkStation.isConnected():
            LightControl.lightShow([LED.CONNECT], 10)
            access_point_exc.disconnectAccessPoint()
            LightControl.light(LED_PIN=LED_PINS.CONNECT)
            monitorSensors()
            print("Network configured through re-check! Monitoring Sensors now.")

    if req.method == 'POST':
        if not NetworkStation.isConnected():
            print("STATION NOT CONNECTED YET...INSERTING NEW CREDENTIALS")
            access_point_exc.modifyCredentials(ssid_, wpa_)
            return redirect('/config/network') # Run again with credentials this time
        else:
            print("REDIRECTING TO SERVER HOSTED DASHBOARD FOR EXC SENSORS...")
            LightControl.lightShow([LED.CONNECT], 10)
            access_point_exc.disconnectAccessPoint()
            LightControl.light(LED_PIN=LED_PINS.CONNECT)
            monitorSensors()
            return redirect('/success')
    if req.method == 'GET':
        if not NetworkStation.isConnected():
          #  print("STATION NOT CONNECTED YET...INSERTING NEW CREDENTIALS")
            access_point_exc.modifyCredentials(req.args.get('ssid'), req.args.get('wpa'))
            return redirect('/config/network')
        else:
           # print("REDIRECTING TO SERVER HOSTED DASHBOARD FOR EXC SENSORS...")
            LightControl.lightShow([LED.CONNECT], 10)
            LightControl.light(LED_PIN=LED_PINS.CONNECT)
            return redirect(RELATIVE_FRONT_END_SUCCESS_PATH)

    if ssid_ is None:
        return BASE_TEMPLATE.format(content=withAlert(NETWORK_CONFIG_PG, alertText="Please enter your network name in the box."))
    elif wpa_ is None:
        return BASE_TEMPLATE.format(
            content=withAlert(NETWORK_CONFIG_PG, alertText="Please enter your network passkey in the box."))
    else:
        if NetworkStation.isConnected():
            return redirect(RELATIVE_FRONT_END_SUCCESS_PATH)
        else:
            return redirect('/config/network')


@app.post('/logout')
def logout():
    DEVICE_USER.username = None
    DEVICE_USER.password = None
    fileIO.replaceVariableInPYFileString('config.py', var='username', val=None)
    fileIO.replaceVariableInPYFileString('config.py', var='password', val=None)
    return redirect('/login')


@app.get('/config/network/success1')
@app.post('/config/network/success1')
def success_frontEnd():
    print("Serving front end success page for wifi setup.")
    return BASE_TEMPLATE.format(content=withRedirect(SUCCESSFUL_WIFI_SETUP, RELATIVE_BACK_END_SUCCESS_PATH))


@app.get('/config/network/success2')
@app.post('/config/network/success2')
def success_backEnd():
    access_point_exc.disconnectAccessPoint()
    print("ATTEMPTING TO START SERVICE PICKER FROM BACKEND")
    main.servicePicker()  # Starting service picker
    return True


if __name__ == '__main__':
    app.run()
