# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()
import network
import machine
import urequests
import time
import config  # Ensure that you have a config.py file with WIFI_SSID and WIFI_PASS

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
    esp_config = sta_if.ifconfig()
    print("ESP IP address:", esp_config)
    print("Connected to Wi-Fi\n")

    ip_address, netmask, _, _ = sta_if.ifconfig()
    config.IP_ADDRESS = ip_address  # Store the IP address in the config module
    config.NETMASK = netmask  # Store the netmask in the config module

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
    print("Failed to obtain ESP IP address")
    print("Failed to connect to Wi-Fi")
# endregion
