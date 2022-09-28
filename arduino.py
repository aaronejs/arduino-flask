import time,sys
from fhict_cb_01.CustomPymata4 import CustomPymata4

#-----------
# Constants
#-----------
DHTPIN = 12
LDRPIN = 2
BUTTON1PIN = 8
BUTTON2PIN = 9

#------------------------------
# Initialized global variables
#------------------------------
humidity = 0
temperature = 0
LDRvalue = 0
buttonLevel1 = 0
buttonLevel2 = 0
prevLevel1 = 1
prevLevel2 = 1
mode = 0

#-----------
# functions
#-----------

def Button1Changed(data):
    global buttonLevel1
    buttonLevel1 = data[2]

def Button2Changed(data):
    global buttonLevel2
    buttonLevel2 = data[2]

def Measure(data):
    global humidity, temperature
    # [report_type, pin, dht_type, error_value, humidity, temperature, timestamp]
    if (data[3] == 0):
        humidity = data[4]
        temperature = data[5]

def LDRChanged(data):
    global LDRvalue
    LDRvalue = data[2]

def setup():
    global board
    board = CustomPymata4(com_port = "COM7")
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback = Measure)
    board.set_pin_mode_analog_input(LDRPIN, differential = 10, callback = LDRChanged)
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN, callback = Button1Changed) # set pin to input pullup
    board.set_pin_mode_digital_input_pullup(BUTTON2PIN, callback = Button2Changed) # set pin to input pullup
    

def loop():
    global prevLevel1, prevLevel2, mode
    prevMode= prevTemp= prevHumidity= prevLDR = 0
    if prevLevel1 != buttonLevel1:
        mode += 1
        prevLevel1 = buttonLevel1

    if prevLevel2 != buttonLevel2:
        mode -= 1
        prevLevel2 = buttonLevel2

    if mode > 7:
        mode = 0
    if mode < -1:
        mode = 6
    
    match mode:
        case 0:
            if prevMode != mode:
                board.displayShow(mode)
                prevMode = mode
        case 2:
            if prevTemp != temperature:
                board.displayShow(temperature)
                prevTemp = temperature
        case 4:
            if prevHumidity != humidity:
                board.displayShow(humidity)
                prevHumidity = humidity
        case 6:
            if prevLDR != LDRvalue:
                board.displayShow(LDRvalue)
                prevLDR = LDRvalue

    time.sleep(0.01) # Give Firmata some time to handle the protocol.

# Put your functions here.

#--------------
# main program
#--------------
setup()
while True:
    try:
        loop()
    except KeyboardInterrupt: # Shutdown Firmata on Crtl+C.
        print ('shutdown')
        board.shutdown()
        sys.exit(0)  