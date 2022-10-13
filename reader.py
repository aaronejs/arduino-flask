import requests
import csv

def sendDataFromCSV(fileName : str, url : str):
    with open(fileName, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = {}
            for key, value in row.items():
                if key != 'sensor_id' and key != 'time':
                    value = float(value)
                data[key] = value
                

            data['sent_time'] = data.pop('time')      #format for server
            data['sent_temp'] = data.pop('temperature')
            data['sent_humidity'] = data.pop('humidity')
            data['sent_light'] = data.pop('light')
            print(data)
            response = requests.post(url, json = row)

while True:
    input_file = input('Please enter the file name: ')
    url = input("Please enter the IP address of the Flask server: ")
    inpt = input('S-send data, Q-quit\n')

    if not url:
        url = "http://localhost:5000/post_data"
    else: 
        url = url + ":5000/post_data"

    if inpt in 'sS':
        sendDataFromCSV(input_file, url)
    else:
        break