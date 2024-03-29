import json
import re
import subprocess
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


def get_wifi_details(interface='wlan0'):
    # Get SSIDs of available networks
    scan_output = subprocess.check_output(['iwlist', interface, 'scan']).decode('utf-8')
    ssids = [line.split(':')[1].strip() for line in scan_output.split('\n') if "ESSID" in line]

    # Get current connection details using 'iw'
    iw_result = subprocess.check_output(['iw', interface, 'link']).decode('utf-8')
    signal_match = re.search(r'signal: (-?\d+)', iw_result)
    frequency_match = re.search(r'freq: (\d+)', iw_result)
    signal_strength = signal_match.group(1) if signal_match else "N/A"
    frequency = frequency_match.group(1) if frequency_match else "N/A"

    # Measure latency
    try:
        ping_result = subprocess.check_output(['ping', '-c', '4', '8.8.8.8']).decode('utf-8')
        latency_match = re.search(r'rtt min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms', ping_result)
        latency = latency_match.group(1) if latency_match else "N/A"
    except subprocess.CalledProcessError:
        latency = "Ping failed"

    return ssids, signal_strength, frequency, latency

# Configure your MQTT client as before
myMQTTClient = AWSIoTMQTTClient("raspberryPiThing")
myMQTTClient.configureEndpoint("a2x5w8hvbskv9v-ats.iot.ap-southeast-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("./AmazonRootCA1.pem", "./ef0c0ecdba3f5dcee71d2c5ba8f5cd3d328a520d0d272d9b4fa5efc7ed8e014a-private.pem.key", "./ef0c0ecdba3f5dcee71d2c5ba8f5cd3d328a520d0d272d9b4fa5efc7ed8e014a-certificate.pem.crt")

print("Endpoint Configured")
myMQTTClient.connect()
print("Client Connected")

ssids, signal_strength, frequency, latency = get_wifi_details()

# Assuming you want to send a single message with all details
jsonmsg = json.dumps({
    "timestamp": time.time(),
    "ssids": ssids,
    "signal_strength": signal_strength,
    "frequency": frequency,
    "latency": latency,
    "device_id": "raspberryPi"
}, indent=2)

print(jsonmsg)
topic = "wifi/inbound"
myMQTTClient.publish(topic, jsonmsg, 0)
print("Message Sent")

myMQTTClient.disconnect()
print("Client Disconnected")
