import json
import sys
import time

import psutil
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

myMQTTClient = AWSIoTMQTTClient("alexLaptopThing")
myMQTTClient.configureEndpoint("a2x5w8hvbskv9v-ats.iot.ap-southeast-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("./AmazonRootCA1.pem","./b968e7d1c8b37361594b4318a3a2fcc34cd48588259c8dc1ebf11ac6acac0b93-private.pem.key", "./b968e7d1c8b37361594b4318a3a2fcc34cd48588259c8dc1ebf11ac6acac0b93-certificate.pem.crt")

print("Endpoint Configured")

myMQTTClient.connect()
print("Client Connected")

for i in range(10):
    msg = "Sample data from the device"
    jsonmsg = json.dumps({
        "sample_time": time.time(),
        "cpu": psutil.cpu_percent(),
        "mem": psutil.virtual_memory().percent,
        "device_id": "alexLaptop",
        "message_count": i
    }, indent=2)
    print(jsonmsg)
    topic = "general/inbound"
    myMQTTClient.publish(topic, jsonmsg, 0)
    print("Message Sent")
    time.sleep(1)

myMQTTClient.disconnect()
print("Client Disconnected")