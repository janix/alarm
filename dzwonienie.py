#!/usr/bin/python

#author: Janusz Janik

import serial
import time
import sys

ser = serial.Serial(
	port='/dev/ttyUSB0'
)

group = sys.argv[1]

def dialup(phone_number):
	ser.write("atdt+48{0};\r".format(phone_number))
	while True:
		data = ser.readline().rstrip()
		print data
        
		if ('ERROR' in data):
			time.sleep(5)
			ser.write("atdt+48{0};\r".format(phone_number))
			continue

		elif ('^CONF:1' in data):
			time.sleep(30)
			ser.write("at+chup\r")
		elif ('^CEND' in data):
			time.sleep(2)
			print "Ending call"
			break	
			

numbersList = [xxxxxxxxx,yyyyyyyyy,zzzzzzzzz]

for number in numbersList:
	dialup(number)
