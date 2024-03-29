import time

def customCallback(client,userdata,message):
    print("callback came...")
    print(message.payload)

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

myMQTTClient = AWSIoTMQTTClient("alexLaptopThing")
myMQTTClient.configureEndpoint("a2x5w8hvbskv9v-ats.iot.ap-southeast-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("./AmazonRootCA1.pem","./b968e7d1c8b37361594b4318a3a2fcc34cd48588259c8dc1ebf11ac6acac0b93-private.pem.key", "./b968e7d1c8b37361594b4318a3a2fcc34cd48588259c8dc1ebf11ac6acac0b93-certificate.pem.crt")

myMQTTClient.connect()
print("Client Connected")

myMQTTClient.subscribe("general/outbound", 1, customCallback)
print('waiting for the callback. Click to continue...')
x = input()

myMQTTClient.unsubscribe("general/outbound")
print("Client unsubscribed") 


myMQTTClient.disconnect()
print("Client Disconnected")