#!/usr/bin/python

#run as root
#author: Janusz Janik


import smbus
import time
import sys
import os

PATH = '/tmp/timestamp'

def main():

	read_value = read_sensor(0x39) + read_sensor(0x49)
	sensors_limit_value = 1000
	
#	print read_value

	if (read_value > 0 and read_value < sensors_limit_value):
		if call_permit():
			make_call(3, 'wszyscy')
#			make_call(1, 'janix')

	elif (read_value < 0):
		time.sleep(30)
		read_value2 = read_sensor(0x39) + read_sensor(0x49)
		if (read_value2 < sensors_limit_value):
			if call_permit():
				make_call(3, 'wszyscy')



def read_sensor(address):

	# Get I2C bus
	bus = smbus.SMBus(1)

	# Get address from script parameter (for example ./TSL2561.py 39)
#	addr = int(sys.argv[1], 16)

	# TSL2561 address, 0x39(57)
	# Select control register, 0x00(00) with command register, 0x80(128)
	#               0x03(03)        Power ON mode

	try:
		bus.write_byte_data(address, 0x00 | 0x80, 0x03)
		# TSL2561 address, 0x39(57)
		# Select timing register, 0x01(01) with command register, 0x80(128)
		#               0x02(02)        Nominal integration time = 402ms
		bus.write_byte_data(address, 0x01 | 0x80, 0x02)

		time.sleep(0.5)

		# Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
		# ch0 LSB, ch0 MSB
		data = bus.read_i2c_block_data(address, 0x0C | 0x80, 2)

		# Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
		# ch1 LSB, ch1 MSB
		data1 = bus.read_i2c_block_data(address, 0x0E | 0x80, 2)

		# Convert the data
		ch0 = data[1] * 256 + data[0]
		ch1 = data1[1] * 256 + data1[0]


		# Output data to screen
		print "sensor {0:02x}: Full Spectrum(IR + Visible) :{1} lux".format(address, ch0)
		print "sensor {0:02x}: Infrared Value :{1} lux".format(address, ch1)
		print "sensor {0:02x}: Visible Value :{1} lux".format(address, ch0-ch1)
		
		return ch0

	except IOError:
		print "IOError Sensor {0:02x}".format(address)
		return -1

def call_permit():
	set_timestamp = 900
	try:
		if check_timestamp() < 0:
			print "timestamp < 0"
			return True
		elif check_timestamp() > 0 and check_timestamp() <= set_timestamp:
			print "waiting for delay time"
			return False
		elif check_timestamp() > set_timestamp:
			print "delay time has passed, making call"
			return True

	except IOError:
		print "/tmp/timestamp is missing"
		return True
	except ValueError:
		print "/tmp/timestamp was modified by hand"
		return True

def create_file():
	f = open(PATH, 'w+')
	timestamp = time.time()
	f.write(str(timestamp))
	print timestamp
	f.close()

def check_timestamp():
	f = open(PATH, 'r')
	old_timestamp = float(f.read())
	new_timestamp = time.time()
	time_interval = new_timestamp - old_timestamp
	return time_interval

def make_call(repetitions_number, group):
	create_file()
	for n in range(repetitions_number):
		os.system("/var/scripts/alarmy/dzwonienie.py {0}".format(group))


main()
