from datetime import datetime as dt
from fhict_cb_01.CustomPymata4 import CustomPymata4
import requests
import random as r
import csv

fieldnames = ['time', 'temperature','humidity','light']
board = CustomPymata4(com_port = "COM8")
DHTPIN = 12
LDRPIN = 2
temperature = humidity = light = 0

def setup():
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback = Measure)
    board.set_pin_mode_analog_input(LDRPIN, differential = 10, callback = LDRMeasure)

def LDRMeasure(data):
    global light
    light = data[2]

def Measure(data):
    global humidity, temperature
    # [report_type, pin, dht_type, error_value, humidity, temperature, timestamp]
    if (data[3] == 0):
        humidity = data[4]
        temperature = data[5]

def getCurTime():
    return dt.now().strftime('%H:%M:%S')

def writeCSV(maxLines : int):
    if temperature == 0:
        writeCSV(maxLines)
    else:
        data = {'time':getCurTime(), 'temperature':temperature, 'humidity':humidity, 'light':light}

        with open('data.csv') as f:
            rows = sum(1 for line in f)
        if rows < maxLines+1:
            with open('data.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(data)

    return data

def sendData():
    result = writeCSV(32)
    data = { 'sent_time': result['time'], 'sent_temp': result['temperature'],
             'sent_humidity':result['humidity'], 'sent_light':result['light'] }
    response = requests.post('http://localhost:5000/post_data', json = data)

def getAvg():
    response = requests.get('http://localhost:5000/average')
    data = response.json()

    if data == {}:
        print("No data available")
        return

    temp = data['temperature']

    print("Average received from server: " + str(temp) + " degrees")

setup()
while True:
    inpt = input('S-send data, G-get average, Q-quit\n')

    if inpt in 'sS':
        sendData()
    elif inpt in 'gG':
        getAvg()
    else:
        break