import random as r
from flask import Flask
from flask import render_template
from datetime import datetime as dt
from fhict_cb_01.CustomPymata4 import CustomPymata4

LDRPIN = 2
DHTPIN = 12
statistics = [{"sensor_id" : 0, "average_temperature" : 0.0, "average_humidity" : 0.0, "average_light" : 0}]
app = Flask(__name__)
board = CustomPymata4(com_port = "COM8")

def Measure(data):
    global humidity, temperature
    # [report_type, pin, dht_type, error_value, humidity, temperature, timestamp]
    if (data[3] == 0):
        humidity = data[4]
        temperature = data[5]

def LDRMeasure(data):
    global light
    light = data[2]

def CalcAverage(type : str):
    counter = 0
    avg = 0
    for i in statistics:
        if i != statistics[0]:
            for key, value in i.items():
                if type == key:
                    avg += value
                    counter += 1

    return avg/counter

@app.route("/")
def main():
    now = dt.now().strftime('%H:%M:%S')
    board.set_pin_mode_analog_input(LDRPIN, differential = 10, callback = LDRMeasure)
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback = Measure)

    if len(statistics) < 15:
        statistics.append({ "time" : now, "temperature" : temperature, "humidity" : humidity, "light" : light})
        statistics[0] = {"sensor_id" : 0, "average_temperature" : round(CalcAverage("temperature"), 2), 
                        "average_humidity" : round(CalcAverage("humidity"), 2), "average_light" : round(CalcAverage("light"), 2)} 
    
    return render_template('time.html', statistics = statistics)