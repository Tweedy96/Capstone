import json
import subprocess
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


# Function to scan for WiFi networks and return a list of SSIDs
def scan_wifi_networks(interface='wlan0'):
    scan_output = subprocess.check_output(['iwlist', interface, 'scan'])
    scan_text = scan_output.decode('utf-8')
    # This is a simplistic parser; consider using more robust parsing depending on your needs
    ssids = [line.split(':')[1].strip() for line in scan_text.split('\n') if "ESSID" in line]
    return ssids

# Configure your MQTT client as before
myMQTTClient = AWSIoTMQTTClient("raspberryPiThing")
myMQTTClient.configureEndpoint("a2x5w8hvbskv9v-ats.iot.ap-southeast-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("./AmazonRootCA1.pem", "./ef0c0ecdba3f5dcee71d2c5ba8f5cd3d328a520d0d272d9b4fa5efc7ed8e014a-private.pem.key", "./ef0c0ecdba3f5dcee71d2c5ba8f5cd3d328a520d0d272d9b4fa5efc7ed8e014a-certificate.pem.crt")

print("Endpoint Configured")

myMQTTClient.connect()
print("Client Connected")

wifi_data = scan_wifi_networks()

for i, ssid in enumerate(wifi_data):
    jsonmsg = json.dumps({
        "timestamp": time.time(),
        "ssid": ssid,
        "device_id": "raspberryPi",
        "message_count": i
    }, indent=2)
    print(jsonmsg)
    topic = "wifi/inbound"
    myMQTTClient.publish(topic, jsonmsg, 0)
    print(f"Message Sent for SSID: {ssid}")
    time.sleep(1)

myMQTTClient.disconnect()
print("Client Disconnected")
