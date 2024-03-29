import json
import re
import subprocess
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


def get_wifi_details(interface='wlan0'):
    # Get SSID and RSSI
    try:
        iwconfig_output = subprocess.check_output(['iwconfig', interface]).decode('utf-8')
        ssid_match = re.search(r'ESSID:"([^"]+)"', iwconfig_output)
        rssi_match = re.search(r'Signal level=(\S+ \S+)', iwconfig_output) # Adjust based on your iwconfig output
        ssid = ssid_match.group(1) if ssid_match else "Not Connected"
        rssi = rssi_match.group(1) if rssi_match else "N/A"
    except subprocess.CalledProcessError as e:
        print(f"Failed to get WiFi details: {e}")
        ssid, rssi = "Error", "Error"
    
    # Measure latency
    try:
        ping_output = subprocess.check_output(['ping', '-c', '1', '8.8.8.8']).decode('utf-8')
        latency_match = re.search(r'time=(\S+) ms', ping_output)
        latency = latency_match.group(1) if latency_match else "N/A"
    except subprocess.CalledProcessError:
        latency = "Ping failed"
    
    return ssid, rssi, latency

# Setup your AWS IoT MQTT Client
myMQTTClient = AWSIoTMQTTClient("raspberryPiThing")
# Assuming MQTT client configuration is done as in previous examples

def main():
    myMQTTClient.connect()
    print("Client Connected")
    
    for _ in range(30):  # Send data once per second for 60 seconds
        ssid, rssi, latency = get_wifi_details()
        
        # Construct the message
        jsonmsg = json.dumps({
            "timestamp": time.time(),
            "ssid": ssid,
            "rssi": rssi,
            "latency": latency,
            "device_id": "raspberryPi"
        }, indent=2)
        
        print(jsonmsg)
        topic = "wifi/metrics"
        myMQTTClient.publish(topic, jsonmsg, 0)
        print("Message Sent")
        
        time.sleep(0.5)
    
    myMQTTClient.disconnect()
    print("Client Disconnected")

if __name__ == "__main__":
    main()
