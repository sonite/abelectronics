#!/usr/bin/env python3
# read abelectronics ADC Pi board inputs with repeating reading from each channel.
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
# for version 1 Raspberry PI boards use: 
# with i2c.I2CMaster(0) as bus:
# for version 2 Raspberry PI boards use: 
with i2c.I2CMaster(1) as bus:
	

	def ChangeChannel(address, channel):
		bus.transaction(i2c.writing_bytes(address, channel))
		time.sleep(0.001)

	def getrepeatadcreading(address):
			h, l, r = bus.transaction(i2c.reading(address,3))[0]
			time.sleep(0.001)
			t = (h << 8 | l)
			if (t >= 32768):
				t = 65536 -t
			v = (t * 0.000154	)
			if (v < 5.5):
				return v
		return 0.00
		
		
	while True:
		# init channel 1 on adc
		ChangeChannel(adc_address1, adc_channel1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		
		# init channel 2 on adc
		ChangeChannel(adc_address1, adc_channel2))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		print ("1: %02f" % getrepeatadcreading(adc_address1))
		
		
		time.sleep(0.001)