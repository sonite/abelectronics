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
# Version 1.1  - 17/10/2012
# Version History:
# 1.0 - Initial Release
# 1.1 - Added code for automatic port selection and 16, 14 & 12 bit conversion
#
# Usage: getadcreading(address, port, gain, resolution) to return value in millivolts.
#
# address = DSPi_address1 or DSPi_address2 - Hex address of I2C chips as configured by board header pins.
# port = adc input 1-4 for ADC Chips, ports 5-8 are referenced as 1-4 in code with DSPi_address2 as chip address.
# gain use 0 for 1x gain
# gain use 1 for 2x gain
# gain use 2 for 4x gain
# gain use 3 for 8x gain
# resolution use 0 for 12 bit
# resolution use 1 for 14 bit
# resolution use 2 for 16 bit
# resolution use 3 for 18 bit.
# 

import quick2wire.i2c as i2c

import time
import re

DSPi_GAIN_FIELD = 0X03
DSPi_GAIN_X1 = 0X00 # gain x1
DSPi_GAIN_X2 = 0X01 # gain x2
DSPi_GAIN_X4 = 0X02 # gain x4
DSPi_GAIN_X8 = 0X03 # gain x5

DSPi_RES_FIELD = 0X0C #resolution / rate field
DSPi_RES_SHIFT = 2 # shift to low bits
DSPi_12_BIT = 0X00 # 12 bit 240 SPS
DSPi_14_BIT = 0X04 # 14 bit 60 SPS
DSPi_16_BIT = 0X08 # 16 bit 15 SPS
DSPi_18_BIT = 0X0C # 18 bit 3.75 SPS

DSPi_CONTINUOUS = 0X10 # 1 = con, 0 = one shot

DSPi_CHAN_FIELD = 0X60 # channel field
DSPi_CHANNEL_1 = 0X00 # select channel 1
DSPi_CHANNEL_2 = 0X20 # select channel 2
DSPi_CHANNEL_3 = 0X40 # select channel 3
DSPi_CHANNEL_4 = 0X50 # select channel 4

DSPi_START = 0X80
DSPi_BUSY = 0X80


DSPi_address1 = 0x68
DSPi_address2 = 0x69

DSPi_channel1 = 0x98
DSPi_channel2 = 0xB8
DSPi_channel3 = 0xD8
DSPi_channel4 = 0xF8

varDivisior = 1


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
	
#bus.transaction(i2c.writing_bytes(DSPi_address1, 0X00, 0X0C))


	def getadcreading(address, channel, gain, res):
		channel = channel - 1
		adcConfig = DSPi_START | DSPi_CHANNEL_1 | DSPi_CONTINUOUS
		adcConfig |= chan << 5 | res << 2 | gain
		
		
		varDivisior = 1 << (gain + 2*res)
		# Select port to read
		bus.transaction(i2c.writing_bytes(address, adcConfig))
		
		time.sleep(0.05)
		if (res == 3):
			# 18 bit mode
			h, m, l ,s = bus.transaction(i2c.reading(address,4))[0]
			time.sleep(0.05)
			h, m, l, s  = bus.transaction(i2c.reading(address,4))[0]
			# shift bits to product result
			t = ((h & 0b00000001) << 16) | (m << 8) | l
		else:
			# 16, 14 or 12 bit
			h, l, s = bus.transaction(i2c.reading(address,3))[0]
			time.sleep(0.05)
			h, l, s = bus.transaction(i2c.reading(address,3))[0]
			# shift bits to product result
			t = (h << 8) | l
		
		# check if positive or negative number and invert if needed
		if (h > 128):
			t = ~(0x020000 - t)
		# return result 	
		return (t/varDivisior)
	
	while True:
		chan = 0
		gain = 0
		res = 3
		
		
		print ("Channel 1: %02f" % getadcreading(DSPi_address1, 1, gain, res))
		#print ("Channel 2: %02f" % getadcreading(DSPi_address1, 2, gain, res))
		#print ("Channel 3: %02f" % getadcreading(DSPi_address1, 3, gain, res))
		#print ("Channel 4: %02f" % getadcreading(DSPi_address1, 4, gain, res))
		#print ("Channel 5: %02f" % getadcreading(DSPi_address2, 1, gain, res))
		#print ("Channel 6: %02f" % getadcreading(DSPi_address3, 2, gain, res))
		#print ("Channel 7: %02f" % getadcreading(DSPi_address3, 3, gain, res))
		#print ("Channel 8: %02f" % getadcreading(DSPi_address4, 4, gain, res))
		time.sleep(1)	
