import random
import time
import pywifi
from pywifi import const, PyWiFi, Profile

def scan_wifi():
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    results = iface.scan_results()

    wifi_list = []
    for network in results:
        security = "OPEN"
        if network.akm:
            if const.AKM_TYPE_WPA2 in network.akm:
                security = "WPA2"
            elif const.AKM_TYPE_WPA in network.akm:
                security = "WPA"
            elif const.AKM_TYPE_WPA3 in network.akm:
                security = "WPA3"

        wifi_list.append({
            "SSID": network.ssid,
            "BSSID": network.bssid,
            "Security": security
        })

    return wifi_list

def auto_guess(target):
    
    attempts = 0
    guess = "00000000"
    
    while guess != target:
        attempts += 1
        guess = str(random.randint(10**7, 10**8 - 1))
        if guess[6] == '0':
            continue
        
    print(f"找到目標數字: {target}，總共嘗試次數: {attempts}")

def connect_wifi(target_ssid, target_password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    while True:
        iface.disconnect()
        time.sleep(1)

        profile = pywifi.Profile()
        profile.ssid = target_ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = target_password

        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)

        iface.connect(tmp_profile)
        print(f"嘗試連接到 {target_ssid}...")
        time.sleep(5)

        if iface.status() == const.IFACE_CONNECTED:
            print(f"成功連接到 WiFi: {target_ssid}")
            break
        else:
            print(f"無法連接到 WiFi: {target_ssid}，1秒後重試...")

if __name__ == '__main__':
    ssid = "Your_WiFi_SSID"
    password = "Your_WiFi_Password"
    connect_wifi(ssid, password)
