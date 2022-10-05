from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
app = Flask(__name__)
dataList = []

def calcAvg(type : str):
    counter = 0
    avg = 0
    for i in dataList:
        for key, value in i.items():
            if type == key:
                avg += value
                counter += 1

    if counter < 1:
        return 0.0
    return avg/counter

@app.route("/")
def main():
    return render_template('index.html', data = dataList)

@app.route('/post_data', methods = ['POST'])
def add_data():
    data = request.get_json()
    time = data['sent_time']
    temperature = data['sent_temp']
    humidity = data['sent_humidity']
    light = data['sent_light']

    newData = { "time" : time, "temperature" : temperature, "humidity" : humidity, "light" : light}
    dataList.append(newData)

    return redirect('/', code=302)

@app.route('/average', methods = ['GET'])
def sendAverage():

    if len(dataList) == 0:
        return

    temperature = calcAvg('temperature')
    humidity = calcAvg('humidity')
    light = calcAvg('light')
    return { 'temperature':temperature, 'humidity':humidity, 'light':light }

if __name__ == '__main__':
    app.run(debug=True)