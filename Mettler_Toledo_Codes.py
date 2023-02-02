import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from serial_interface import SerialInterface,SerialInterfaces,find_serial_interface_ports

serial_device=serial.Serial(port='COM4',
                                baudrate=9600,
                                timeout=0.05)
serial_device.write(b'SIR\r\n')
i=0
s=time.time()
while i<20:
    a=serial_device.readline().decode()
    print(a.split())
    time.sleep(0.01)
    i+=1
print(time.time()-s)
serial_device.close()
