import random as r
from flask import Flask
from flask import render_template
from datetime import datetime as dt
from fhict_cb_01.CustomPymata4 import CustomPymata4
import time

LDRPIN = 2
DHTPIN = 12
light = humidity = temperature = 0
statistics = []
statistics_calc = [
    {"max_temp" : 0, "avg_temp" : 0, "min_temp" : 0},
    {"max_humidity" : 0, "avg_humidity" : 0, "min_humidity" : 0},
    {"max_light" : 0, "avg_light" : 0, "min_light" : 0}
]

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

def CalcMax(type : str):
    max = 0

    for i in statistics:
        for key, value in i.items():
            if type == key:
                if value > max:
                    max = value

    return max

def CalcAverage(type : str):
    counter = 0
    avg = 0
    for i in statistics:
        for key, value in i.items():
            if type == key:
                avg += value
                counter += 1

    if counter < 1:
        return 0.0
    return avg/counter

def CalcMin(type : str):
    min = 10000
    for i in statistics:
        for key, value in i.items():
            if type == key:
                if value < min:
                    min = value
    
    return min

@app.route("/")
def main():
    rows = 3
    now = dt.now().strftime('%H:%M:%S')
    board.set_pin_mode_analog_input(LDRPIN, differential = 10, callback = LDRMeasure)
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback = Measure)

    if len(statistics) < rows+1:
        if temperature > 0 and humidity > 0 and light > 0:

            statistics.append({ "time" : now, "temperature" : temperature, "humidity" : humidity, "light" : light})
        
            statistics_calc[0] = {"max_temp" : round(CalcMax("temperature"), 2), "avg_temp" : round(CalcAverage("temperature"), 2), "min_temp" : round(CalcMin("temperature"), 2)}
            statistics_calc[1] = {"max_humidity" : round(CalcMax("humidity"), 2), "avg_humidity" : round(CalcAverage("humidity"), 2), "min_humidity" : round(CalcMin("humidity"), 2)}
            statistics_calc[2] = {"max_light" : round(CalcMax("light"), 2), "avg_light" : round(CalcAverage("light"), 2), "min_light" : round(CalcMin("light"), 2)}
            if len(statistics) > rows:
                del statistics[0]

    return render_template('time.html', statistics = statistics, statistics_calc = statistics_calc)