import config
from config import username
from CONSTANT_DEFS import *

def getDashboardLocation():
    return f"{DASHBOARD_LOCATION_PATH}?username={username}"


stylesheet = '<link rel="stylesheet" href="https://itoven-ai.co/homi/css/main.css">'

BASE_TEMPLATE = '''<!doctype html>
<html>
  <head>

    <link rel="stylesheet" href="https://itoven-ai.co/homi/css/main.css">
  </head>
  <body>
        <div style="display:inline-flex; min-width: 550px;" id="navigationWithLogo">
          <div style="background-color: #0d7963; height:60px;">
            <ul class="nav" style="font-size: 1.3rem; padding-top: 1rem; height: 60px; width: 550px;">
              <li>
                <a href="/config/network">Network Settings</a>
              </li>
              <li>
                <a href="/logout">Logout</a>
              </li>
              <li>
                <a href="{dashboardLocation}">Dashboard</a>
              </li>
              <li>
                <a href="#">Help</a>
              </li>
            </ul>
          </div>
          <div style="background-color: #0d7963; height:60px; padding: 1rem; padding-bottom: 1rem; vertical-align: center;">
            <img src="https://itoven-ai.co/images/logo-white.png" height=38; width=120px;>
          </div>
        </div>
    {content}
  </body>
</html>'''


SUCCESSFUL_WIFI_SETUP = f'''

     <div style="display:inline-flex; min-width: 550px;" id="navigationWithLogo">
       <div style="background-color: #0d7963; height:60px;">
         <ul class="nav" style="font-size: 1.3rem; padding-top: 1rem; height: 60px; width: 550px;">
           <li>
             <a href="/config/network">Network Settings</a>
           </li>
           <li>
             <a href="/logout">Logout</a>
           </li>
           <li>
             <a href="{getDashboardLocation()}">Dashboard</a>
           </li>
           <li>
             <a href="#">Help</a>
           </li>
         </ul>
       </div>
       <div style="background-color: #0d7963; height:60px; padding: 1rem; padding-bottom: 1rem; vertical-align: center; min-width: 100rem;">
         <img src="https://itoven-ai.co/images/logo-white.png" height=38; width=120px;>
       </div>
     </div>
     <div style="top: 1rem; position: relative; text-align: center;">
       <h1 style="color: gold; padding-bottom: 2rem;">Next Steps</h1>
       <div style="max-width: 50%; left: 25%; position: relative;box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px, rgba(17, 17, 26, 0.05) 0px 8px 32px; border-radius: 1rem; padding: 1rem;">
         <p>Great! Your HomeSense is now connected to the internet. Now, just make sure your phone/computer is connected back to your normal WIFI/LTE and visit your dashboard.</p>
       </div>
       <div style="max-width: 42%; display: inline-flex; position: relative; border-radius: 1rem; padding: 3rem; box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px; top: 1rem;">
         <p>Note: If your login credentials are correct, this button will take you to your devices. If not, it will take you back to the login screen.</p>
       </div>
       <div id="buttonDiv" style="max-width: 50%; min-height: 15rem;left: 25%; position: relative; border-radius: 1rem; padding: 1rem;">
         <button class="button-15" style="top: 1rem;;min-width: 50%; left: 25%; position: relative;box-shadow: rgba(0, 0, 0, 0.4) 0px 13px 30px;; border-radius: 1rem; padding: 1rem;"> My Dashboard <a href="{DASHBOARD_LOCATION}"></a>
         </button>
       </div>
     </div>

'''

SUCCESSFUL_LOGIN = f'''


     <div style="display:inline-flex; min-width: 550px;" id="navigationWithLogo">
       <div style="background-color: #0d7963; height:60px;">
         <ul class="nav" style="font-size: 1.3rem; padding-top: 1rem; height: 60px; width: 550px;">
           <li>
             <a href="/config/network">Network Settings</a>
           </li>
           <li>
             <a href="/logout">Logout</a>
           </li>
           <li>
             <a href="{getDashboardLocation()}">Dashboard</a>
           </li>
           <li>
             <a href="#">Help</a>
           </li>
         </ul>
       </div>
       <div style="background-color: #0d7963; height:60px; padding: 1rem; padding-bottom: 1rem; vertical-align: center; min-width: 100rem;">
         <img src="https://itoven-ai.co/images/logo-white.png" height=38; width=120px;>
       </div>
     </div>
     <div style="top: 1rem; position: relative; text-align: center;">
       <h1 style="color: gold; padding-bottom: 2rem;">Next Steps</h1>
       <div style="max-width: 50%; left: 25%; position: relative;box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px, rgba(17, 17, 26, 0.05) 0px 8px 32px; border-radius: 1rem; padding: 1rem;">
         <p>Great! Your HomeSense is now connected to the internet. Now, just make sure your phone/computer is connected back to your normal WIFI/LTE and visit your dashboard.</p>
       </div>
       <div style="max-width: 42%; display: inline-flex; position: relative; border-radius: 1rem; padding: 3rem; box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px; top: 1rem;">
         <p>Note: If your login credentials are correct, this button will take you to your devices. If not, it will take you back to the login screen.</p>
       </div>
       <div id="buttonDiv" style="max-width: 50%; min-height: 15rem;left: 25%; position: relative; border-radius: 1rem; padding: 1rem;">
         <button class="button-15" style="top: 1rem;;min-width: 50%; left: 25%; position: relative;box-shadow: rgba(0, 0, 0, 0.4) 0px 13px 30px;; border-radius: 1rem; padding: 1rem;"> My Dashboard <a href="{DASHBOARD_LOCATION}"></a>
         </button>
       </div>
     </div>

'''


LOGGED_OUT = f'''
  
  <div style="padding-top: 5rem">
    <p style="text-align: center;">You are not logged in. New users must create an account at <a href="https://homi.itoven-ai.co" style="color: gold; font-weight: bold;">Homi</a> with a valid internet connection. Your username must be a valid email address. </p>
    <div style="display: flex; justify-content: center;position: ; min-width: 50%; padding-top: 2rem;">
      <form method="POST">
        <p> Username: <input style="background-color: beige;" type="text" name="username" autofocus />
        </p>
        <p style="padding-bottom: 2rem;"> Password: <input type="text" style="background-color: beige;" name="password" autofocus />
        </p>
        <div>
          <div style="display: inline-flex;">
            <input type="submit" class="button-15" value="Login" />
            <a href="https://homi.itoven-ai.co/forgot">
              <button class="button-15" value="Create an Account"> Forgot </button>
            </a>
            <a href="https://homi.itoven-ai.co/register">
              <button class="button-15" value="Sign Up"> Sign Up </button>
            </a>
          </div>
        </div>
      </form>
    </div>
  </div>
  
  '''

NETWORK_CONFIG_PG = f''' 

  <div>
    <p style="padding-bottom: 2rem; padding-top: 2rem; text-align: center;">Let's get connected to your home network.</p>
    <form method="POST">
      <p> Home WiFi Name (SSID): <input style="background-color: beige;" type="text" name="ssid" autofocus />
      </p>
      <p style="padding-bottom: 2rem;"> Home WiFi Passkey (WPA/WPA2): <input style="background-color: beige;" type="text" name="wpa" autofocus />
      </p>
      <input style="" type="submit" class="button-15" value="Submit" />
    </form>
  </div>
'''