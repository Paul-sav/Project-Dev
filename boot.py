# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import network
import machine
import urequests
import time
import config  # Ensure that you have a config.py file with WIFI_SSID and WIFI_PASS

# region Pin initialization
# Actuator initialization
afwd = machine.Pin(4, machine.Pin.OUT); afwd.value(0)
arev = machine.Pin(15, machine.Pin.OUT); arev.value(0)

# PWM for motor wheels
wheel_PWM_B = machine.PWM(machine.Pin(25))
wheel_PWM_B.freq(10000)
wheel_PWM_B.duty(0)
wheel_PWM_A = machine.PWM(machine.Pin(26))
wheel_PWM_A.freq(10000)
wheel_PWM_A.duty(0)

# Wheel initialization
wheel_B1 = machine.Pin(12, machine.Pin.OUT); wheel_B1.value(0)
wheel_B2 = machine.Pin(27, machine.Pin.OUT); wheel_B2.value(0)
wheel_A1 = machine.Pin(13, machine.Pin.OUT); wheel_A1.value(0)
wheel_A2 = machine.Pin(14, machine.Pin.OUT); wheel_A2.value(0)
wheel_stby = machine.Pin(33, machine.Pin.OUT); wheel_stby.value(0)
# endregion

# region Github and Wi-Fi info
# GitHub repository information
GITHUB_USER = "Paul-sav"
GITHUB_REPO = "Project-Dev"
GITHUB_FILE = "main.py"

# Connect to Wi-Fi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(config.WIFI_SSID, config.WIFI_PASS)
# endregion

# region Connecting to Wi-Fi and parsing GitHub repo
# Wait for Wi-Fi connection (5 sec timeout)
timeout = 5
while not sta_if.isconnected() and timeout > 0:
    time.sleep(1)
    timeout -= 1

if sta_if.isconnected():
    print("Connected to Wi-Fi")

    # Function to download code from GitHub
    def download_code(url):
        try:
            response = urequests.get(url)
            if response.status_code == 200:
                code = response.text
                return code
            else:
                print("Failed to download code. HTTP Status Code:", response.status_code)
        except Exception as e:
            print("An error occurred:", str(e))
        return None

    # Read the local version (if available)
    try:
        with open("version.txt", "r") as version_file:
            local_version = version_file.read()
    except OSError:
        local_version = "0.0.0"

    # Check the latest version on GitHub
    github_version_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.txt"
    latest_version = download_code(github_version_url)

    if latest_version is not None and latest_version != local_version:
        # New version available
        print("New version available:", latest_version)

        # Construct the URL to download the main.py file
        github_main_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/{GITHUB_FILE}"
        
        # Download and save the main.py file
        new_code = download_code(github_main_url)

        if new_code is not None:
            with open("main.py", "w") as main_file:
                main_file.write(new_code)
                print("Downloaded and saved main.py")

else:
    print("Failed to connect to Wi-Fi")
# endregion
