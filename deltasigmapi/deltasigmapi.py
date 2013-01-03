#!/usr/bin/env python3
#
# read AB Electronics Delta Sigma Pi inputs.
# www.abelectronics.co.uk
# uses quick2wire from http://quick2wire.com/ github: https://github.com/quick2wire/quick2wire-python-api
# Requries Python 3. 
# GPIO API depends on Quick2Wire GPIO Admin. To install Quick2Wire GPIO Admin, follow instructions at http://github.com/quick2wire/quick2wire-gpio-admin
# I2C API depends on I2C support in the kernel.
# auto I2C port selection code from http://elinux.org/RPi_ADC_I2C_Python by Andrew Scheller
#
# Version 1.2  - 03/01/2013
# Version History:
# 1.0 - Initial Release
# 1.1 bug fixes
# 1.2 bug fixes
#
# Usage: getadcreading(address, hexvalue) to return value in millivolts.
# see pdf file for hex numbers and divisor
#
# address = DSPi_address1 or DSPi_address2 - Hex address of I2C chips as configured by board header pins.


import quick2wire.i2c as i2c

import time
import re


DSPi_address1 = 0x68
DSPi_address2 = 0x69

# set for 18bit mode 1 gain
varDivisior = 64



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
	
	def getadcreading(address, adcConfig):
		# Select port to read
		bus.transaction(i2c.writing_bytes(address, adcConfig))
		
		time.sleep(0.2)
		
		# 18 bit mode
		h, m, l ,s = bus.transaction(i2c.reading(address,4))[0]
		time.sleep(0.1)
		h, m, l, s  = bus.transaction(i2c.reading(address,4))[0]
		# shift bits to product result
		t = ((h & 0b00000001) << 16) | (m << 8) | l
		
		# check if positive or negative number and invert if needed
		if (h > 128):
			t = ~(0x020000 - t)
		# return result 	
		return (t/varDivisior)
	
	while True:
		print ("Channel 1: %02f" % getadcreading(DSPi_address1, 0x9C))
		print ("Channel 2: %02f" % getadcreading(DSPi_address1, 0xBC))
		print ("Channel 3 :%02f" % getadcreading(DSPi_address1, 0xDC))
		print ("Channel 4: %02f" % getadcreading(DSPi_address1, 0xFC))
		print ("Channel 5: %02f" % getadcreading(DSPi_address2, 0x9C))
		print ("Channel 6: %02f" % getadcreading(DSPi_address2, 0xBC))
		print ("Channel 7 :%02f" % getadcreading(DSPi_address2, 0xDC))
		print ("Channel 8: %02f" % getadcreading(DSPi_address2, 0xFC))
		
		time.sleep(1)	
