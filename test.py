import serial
import time

ser = serial.Serial('COM5', 9600, timeout=1)
def get_joystick():
    result = ser.readline()
    result = result[:-2]
    result = result.decode()
    out = result.split(";")
 

    if len(out) < 3:
        return [0 , 0 , 0]

    else:
        out[0] = int(out[0])
        out[1] = int(out[1])
        out[2] = int(out[2])
        out[2] ^= 1
        return out


while True:
    print(get_joystick())

