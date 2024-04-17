from flask import Flask, jsonify, request
import json
import http.client
import threading
import time
import sys
from Adafruit_IO import  MQTTClient

#app = Flask(__name__)
AIO_FEED_ID = ["schedule"]
AIO_USERNAME = "bao23mse23109"
AIO_KEY = "aio_LtkR56mUw0sjKGZGXZuOJiH2OkmP"
schedule = None
#with open('lichhen.json', 'r') as file:
#    schedule = json.load(file)

def check_schedule():
    while True:
        current_time = time.strftime('%H:%M')  # Sử dụng hệ thống 24 giờ
        for switch, events in schedule.items():
            for event in events:
                if event['time'] == current_time:
                    action = event['action']
                    print(f"Executing {action} action for {switch} at {current_time}")
                    if action == "on":
                        value = "1"
                    else:
                        value = "0"
                    client.publish(switch, value)
        time.sleep(60)



def getData(feed_key,limit):
    conn = http.client.HTTPSConnection("io.adafruit.com")

    url = "/api/v2/" + AIO_USERNAME + "/feeds/" + feed_key + "/data?limit="+limit
    #print(url)
    payload = ''
    headers = {'X-AIO-Key': AIO_KEY}
    conn.request("GET",url,payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(feed_key)
    #print(data.decode("utf-8"))
    return data.decode("utf-8")

def setJson():
    global schedule
    data = getData(feed_key="schedule",limit="1")
    print(data)
    data_as_list = json.loads(data)

    # Lấy giá trị từ trường 'value' của dữ liệu
    value = data_as_list[0]['value']

    # Chuyển đổi chuỗi JSON thành đối tượng Python
    schedule_data = json.loads(value)

    schedule = schedule_data

    # Lưu đối tượng Python vào tệp tin JSON
    with open('lichhen.json', 'w') as f:
        json.dump(schedule_data, f, indent=4)

    print("lưu thong tin thanh cong")

# @app.route('/schedule', methods=['GET'])
# def get_schedule():
#     return jsonify(schedule)
#
# if __name__ == '__main__':
#     app.run(debug=True)

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
    global schedule
    if feed_id == "schedule":
        schedule_data = json.loads(payload)
        schedule = schedule_data
        # Lưu đối tượng Python vào tệp tin JSON
        with open('lichhen.json', 'w') as f:
            json.dump(schedule_data, f, indent=4)
        print("lưu thong tin thanh cong")

setJson()
# Khởi tạo luồng kiểm tra lịch trình
schedule_thread = threading.Thread(target=check_schedule)
schedule_thread.daemon = True
schedule_thread.start()

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True:
    a = 1