from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
app = Flask(__name__)
dataList = []
calc_list = [
    {"max_temp" : 0, "avg_temp" : 0, "min_temp" : 0},
    {"max_humidity" : 0, "avg_humidity" : 0, "min_humidity" : 0},
    {"max_light" : 0, "avg_light" : 0, "min_light" : 0}
]

def calcAvg(type : str, collection : list):
    counter = 0
    avg = 0
    for i in collection:
        for key, value in i.items():
            if key == type and key != 'sensor_id' and key != 'time':
                avg += value
                counter += 1

    if counter < 1:
        return 0.0
    return avg/counter

def calcMax(type : str, collection : list):
    max = 0

    for i in collection:
        for key, value in i.items():
            if key == type and key != 'sensor_id' and key != 'time':
                if value > max:
                    max = value

    return max

def calcMin(type : str, collection : list):
    min = 10000
    for i in collection:
        for key, value in i.items():
            if key == type and key != 'sensor_id' and key != 'time':
                if value < min:
                    min = value

    return min

@app.route("/")
def main():
    calc_list[0] = {'max_temp' : calcMax('temperature', dataList), 'avg_temp' : round(calcAvg('temperature', dataList), 2), 'min_temp' : calcMin('temperature', dataList)}
    calc_list[1] = {'max_humidity' : calcMax('humidity', dataList), 'avg_humidity' : round(calcAvg('humidity', dataList), 2), 'min_humidity' : calcMin('humidity', dataList)}
    calc_list[2] = {'max_light' : calcMax('light', dataList), 'avg_light' : round(calcAvg('light', dataList), 2), 'min_light' : calcMin('light', dataList)}

    return render_template('index.html', data = dataList, calculations = calc_list)

@app.route('/post_data', methods = ['POST'])
def add_data():
    data = request.get_json()
    sensor_id = data['sensor_id']
    time = data['sent_time']
    temperature = data['sent_temp']
    humidity = data['sent_humidity']
    light = data['sent_light']

    newData = { "sensor_id" : sensor_id, "time" : time, "temperature" : temperature, "humidity" : humidity, "light" : light}
    dataList.append(newData)

    return redirect('/', code=302)

@app.route('/average', methods = ['GET'])
def sendAverage():

    if len(dataList) == 0:
        return

    temperature = calcAvg('temperature', dataList)
    humidity = calcAvg('humidity', dataList)
    light = calcAvg('light', dataList)
    return { 'temperature': temperature, 'humidity': humidity, 'light': light }

if __name__ == '__main__':
    app.run(debug=True)