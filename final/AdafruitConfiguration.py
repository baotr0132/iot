import serial.tools.list_ports
import random
import time
import sys
from Adafruit_IO import  MQTTClient

AIO_FEED_ID = ["relay1","relay2","relay3"]
AIO_USERNAME = "bao23mse23109"
AIO_KEY = "aio_LtkR56mUw0sjKGZGXZuOJiH2OkmP"

def connected(client):
    print("Ket noi thanh cong ...")
    for item in AIO_FEED_ID:
        client.subscribe(item)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

c1 = True
count = 5
while True:
    if count <= 0:
        count = 5
        value = random.randint(30, 60)
        value2 = random.randint(100, 500)
        value3 = random.randint(40, 100)

        if c1 == True:
            print("cap temperature", value)
            client.publish("temperature", value)
            c1 = False
        else:
            print("moisture", value3)
            client.publish("moisture", value3)
            c1 = True
    count -= 1
    print("check 1s")
    time.sleep(1)