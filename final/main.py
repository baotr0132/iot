from flask import Flask, render_template, jsonify, request
import json
import http.client
from datetime import datetime, timedelta

app = Flask(__name__)
AIO_USERNAME = "bao23mse23109"
AIO_KEY = "aio_LtkR56mUw0sjKGZGXZuOJiH2OkmP"
# Route để hiển thị dashboard
@app.route('/')
def index():
    return render_template('dashboard.html')


# Route API để trả về dữ liệu từ IoT
@app.route('/temperature')
def temperature():
    # Dữ liệu mẫu từ IoT
    #with open('data.json') as json_file:
    #    data = json.load(json_file)

    data_from_api = getData(feed_key="temperature",limit="10")
    data = json.loads(data_from_api)

    sorted_data = sorted(data, key=lambda x: x['created_at'])

    # Format lại created_at chỉ lấy thời gian và cộng thêm 7 tiếng
    for item in sorted_data:
        created_at = datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=7)
        item['created_at'] = created_at.strftime('%H:%M:%S')
        #item['value'] = int( item['value']) * 0.01
    return jsonify(sorted_data)

@app.route('/moisture')
def moisture():
    # Dữ liệu mẫu từ IoT
#    with open('data_moisture.json') as json_file:
#        data = json.load(json_file)

    data_from_api = getData(feed_key="moisture",limit="10")
    data = json.loads(data_from_api)

    sorted_data = sorted(data, key=lambda x: x['created_at'])

    # Format lại created_at chỉ lấy thời gian và cộng thêm 7 tiếng
    for item in sorted_data:
        created_at = datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=7)
        item['created_at'] = created_at.strftime('%H:%M:%S')
        #item['value'] = int( item['value']) * 0.01
    return jsonify(sorted_data)

@app.route('/relay')
def relay():
    key = request.args.get('key')
    data_from_api = getData(feed_key=key,limit="1")
    #data_from_api = getData(feed_key="relay1",limit="1")
    data = json.loads(data_from_api)

    return jsonify(data)

# Hàm để lấy thời gian bắt đầu của ngày hiện tại
def get_start_time():
    today = datetime.today()
    start_time = today.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_time.isoformat() + 'Z'

# Hàm để lấy thời gian kết thúc của ngày hiện tại
def get_end_time():
    today = datetime.today()
    end_time = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    return end_time.isoformat() + 'Z'

def getData(feed_key,limit):
    conn = http.client.HTTPSConnection("io.adafruit.com")
    start_time = get_start_time()
    end_time = get_end_time()

    url = "/api/v2/" + AIO_USERNAME + "/feeds/" + feed_key + "/data?limit="+limit+"&start_time=" + start_time + "&end_time=" + end_time
    #print(url)
    payload = ''
    headers = {'X-AIO-Key': AIO_KEY}
    conn.request("GET",url,payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(feed_key)
    #print(data.decode("utf-8"))
    return data.decode("utf-8")

@app.route('/relay/change')
def setRelay():
    feed_key = request.args.get('key')
    data = request.args.get('data')

    conn = http.client.HTTPSConnection("io.adafruit.com")
    payload = json.dumps({
        "value": data
    })

    url = "/api/v2/" + AIO_USERNAME + "/feeds/" + feed_key + "/data"
    print(payload)
    headers = {'X-AIO-Key': AIO_KEY,'Content-Type': 'application/json'}
    conn.request("POST",url,payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
