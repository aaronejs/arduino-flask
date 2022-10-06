import requests
import csv

def sendDataFromCSV(fileName : str, url : str):
    with open(fileName, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['sent_time'] = row.pop('time')      #format for server
            row['sent_temp'] = row.pop('temperature')
            row['sent_humidity'] = row.pop('humidity')
            row['sent_light'] = row.pop('light')
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