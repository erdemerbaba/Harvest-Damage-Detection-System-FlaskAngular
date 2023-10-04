# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 14:53:58 2022

@author: Akes
"""

import serial
import time

ser = serial.Serial('COM7', 9600) 
time.sleep(2) 
ser.write(b'1') 
ser.write(b'1')
ser.write(b'1') 
time.sleep(2) 
ser.write(b'0') 
ser.write(b'0') 
ser.write(b'0') 

ser.close()