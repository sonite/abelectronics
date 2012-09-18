#!/usr/bin/env python3
# read abelectronics ADC Pi board inputs
# uses quick2wire from http://quick2wire.com/ github: https://github.com/quick2wire/quick2wire-python-api
# Requries Python 3 
# GPIO API depends on Quick2Wire GPIO Admin. To install Quick2Wire GPIO Admin, follow instructions at http://github.com/quick2wire/quick2wire-gpio-admin
# I2C API depends on I2C support in the kernel

import quick2wire.i2c as i2c

import time


adc_address1 = 0x68
adc_address2 = 0x69

adc_channel1 = 0x98
adc_channel2 = 0xB8
adc_channel3 = 0xD8
adc_channel4 = 0xF8

with i2c.I2CMaster(1) as bus:
	

	def getadcreading(address, channel):
		bus.transaction(i2c.writing_bytes(address, channel))
		time.sleep(0.05)
		h, l, r = bus.transaction(i2c.reading(address,3))[0]
		time.sleep(0.05)
		h, l, r = bus.transaction(i2c.reading(address,3))[0]
		
		t = (h << 8 | l)
		if (t >= 32768):
			t = 655361 -t
		v = (t * 0.000154	)
		if (v < 5.5):
			return v
		return 0.00
	
	while True:
		
		print ("1: %02f" % getadcreading(adc_address1, adc_channel1))
		print ("2: %02f" % getadcreading(adc_address1, adc_channel2))
		print ("3: %02f" % getadcreading(adc_address1, adc_channel3))
		print ("4: %02f" % getadcreading(adc_address1, adc_channel4))
		
		print ("5: %02f" % getadcreading(adc_address2, adc_channel1))
		print ("6: %02f" % getadcreading(adc_address2, adc_channel2))
		print ("7: %02f" % getadcreading(adc_address2, adc_channel3))
		print ("8: %02f" % getadcreading(adc_address2, adc_channel4))
		
		time.sleep(1)	
