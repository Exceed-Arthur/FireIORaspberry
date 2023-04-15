import NetworkStation
import access_point_exc
import WebFunctions
import config
import fileIO
from EXCMCU22A import localServer


def secondaryAuthentication():
    if not NetworkStation.isConnected():
        NetworkStation.connect_WIFI()  # Reconnect to WI-FI to make outgoing auth request
    if not (config.username and config.password):
        print("User never entered their login information.")
        NetworkStation.disconnect_WIFI()
        access_point_exc.connectAccessPoint()
        localServer()
    else:
        if not NetworkStation.isConnected():
            NetworkStation.disconnect_WIFI()
            access_point_exc.connectAccessPoint()
            localServer()
        else:
            print("Positive network connection. Attempting to validate User profile...")
            if not WebFunctions.userAuthenticated(USERNAME=config.username, PASSWORD=config.password):
                print("INVALID CREDENTIALS. TRY AGAIN. REDIRECTING.")
                fileIO.replaceFileFromString('config.py', fileIO.replaceVariableInPYFileString(fileName='config.py',
                                                                                               var='username', val='None'))
                fileIO.replaceFileFromString('config.py', fileIO.replaceVariableInPYFileString(fileName='config.py',
                                                                                               var='password', val='None'))
                localServer()
            else:
                return True
