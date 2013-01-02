#!/usr/bin/env python3
# abelectronics IO Pi Expander board output demo with light chaser and binary counter
# uses quick2wire from http://quick2wire.com/ github: https://github.com/quick2wire/quick2wire-python-api
# Requries Python 3 
# GPIO API depends on Quick2Wire GPIO Admin. To install Quick2Wire GPIO Admin, follow instructions at http://github.com/quick2wire/quick2wire-gpio-admin
# I2C API depends on I2C support in the kernel

# Version 1.0  - 16/12/2012
# Version History:
# 1.0 - Initial Release
# 

import quick2wire.i2c as i2c

import time
import re
import array



expander_address1 = 0x20
expander_address2 = 0x21
# IO pin address array
alloff = 0
pinarray  = array.array('i', [1,2, 4, 8, 16, 32, 64, 128])


for line in open('/proc/cpuinfo').readlines():
    m = re.match('(.*?)\s*:\s*(.*)', line)
    if m:
        (name, value) = (m.group(1), m.group(2))
        if name == "Revision":
            if value [-4:] in ('0002', '0003'):
                i2c_bus = 0
            else:
                i2c_bus = 1
            break
            
            
with i2c.I2CMaster(i2c_bus) as bus:
	#set both busses as outputs on both chips
	bus.transaction(i2c.writing_bytes(expander_address1, 0x00, 0x00))
	bus.transaction(i2c.writing_bytes(expander_address1, 0x01, 0x00))
	
	bus.transaction(i2c.writing_bytes(expander_address2, 0x00, 0x00))
	bus.transaction(i2c.writing_bytes(expander_address2, 0x01, 0x00))
	
	# code below will count in binary from 0 to 255 on bank b using outputs (9-16) for IC 1
	# uncomment to run this demo
	#for i in range(1,255):
	#	bus.transaction(i2c.writing_bytes(expander_address1, 0x13, i))
	#	time.sleep(0.1)
	#	bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0))
	#	time.sleep(0.1)
	
	# light chaser demo which switches all 32 outputs on and off in sequence
	bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x00))
	while True:
		
		# run code on IC 2
		
		for i in range(0,8):
			currentrow = pinarray[i]
			bus.transaction(i2c.writing_bytes(expander_address2, 0x13, currentrow))
			time.sleep(0.1)
		bus.transaction(i2c.writing_bytes(expander_address2, 0x13, alloff))	
		
		for i in range(0,8):
			currentrow = pinarray[i]
			bus.transaction(i2c.writing_bytes(expander_address2, 0x12, currentrow))
			time.sleep(0.1)
		bus.transaction(i2c.writing_bytes(expander_address2, 0x12, alloff))		
		
		# run code on IC 1
		#for i in range(0,8):
		#	currentrow = pinarray[i]
		#	bus.transaction(i2c.writing_bytes(expander_address1, 0x12, currentrow))
		#	time.sleep(0.1)
		#bus.transaction(i2c.writing_bytes(expander_address1, 0x12, alloff))	
		
		for i in range(0,8):
			currentrow = pinarray[i]
			bus.transaction(i2c.writing_bytes(expander_address1, 0x13, currentrow))
			time.sleep(0.1)
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, alloff))	
		
