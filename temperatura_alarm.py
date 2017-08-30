#!/usr/bin/python

import os
import time

PATH = '/tmp/timestamp'

def main():

	tempfile = open("/sys/bus/w1/devices/28-04146f491dff/w1_slave")
	thetext = tempfile.read()
	tempfile.close()
	tempdata = thetext.split("\n")[1].split(" ")[9]
	temperature = int(tempdata[2:])

	if temperature > 30000:
		if call_permit():
			make_call(3, 'wszyscy')
#			make_call(1, 'janix')

	print temperature

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
