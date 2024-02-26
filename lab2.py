from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import random
import time
import sys
from Adafruit_IO import MQTTClient

AIO_FEED_ID = ["nutnhan1","nutnhan2"]
AIO_USERNAME = "bao23mse23109"
AIO_KEY = "aio_vPGC60mcONRS5Ge7rrjrxW4NTvkv"

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
##############

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

count = 25
while True:

    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    if count <= 0:
        count = 25

        if class_name[2:] == "Khong khau trang":
            client.publish("cambien1", 50)
            print(50)
        elif class_name[2:] == "Deo khau trang":
            client.publish("cambien1", 70)
            print(70)
        elif class_name[2:] == "Khong nguoi":
            client.publish("cambien1", 90)
            print(90)
    print("count" + str(count))
    count -= 1
    #print("check 1s")
    time.sleep(0.01)
    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
