#!/usr/bin/env python3
# read abelectronics ADC Pi V2 board inputs with repeating reading from each channel.
# uses quick2wire from http://quick2wire.com/ github: https://github.com/quick2wire/quick2wire-python-api
# Requries Python 3 
# GPIO API depends on Quick2Wire GPIO Admin. To install Quick2Wire GPIO Admin, follow instructions at http://github.com/quick2wire/quick2wire-gpio-admin
# I2C API depends on I2C support in the kernel

# Version 1.0  - 18/11/2012
# Version History:
# 1.0 - Initial Release
# 
#
# Usage: getadcreading(address, port, gain, resolution) to return value in volts.
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

MCP342X_GAIN_FIELD = 0X03
MCP342X_GAIN_X1 = 0X00 # gain x1
MCP342X_GAIN_X2 = 0X01 # gain x2
MCP342X_GAIN_X4 = 0X02 # gain x4
MCP342X_GAIN_X8 = 0X03 # gain x8

MCP342X_RES_FIELD = 0X0C #resolution / rate field
MCP342X_RES_SHIFT = 2 # shift to low bits
MCP342X_12_BIT = 0X00 # 12 bit 240 SPS
MCP342X_14_BIT = 0X04 # 14 bit 60 SPS
MCP342X_16_BIT = 0X08 # 16 bit 15 SPS
MCP342X_18_BIT = 0X0C # 18 bit 3.75 SPS

MCP342X_CONTINUOUS = 0X10 # 1 = con, 0 = one shot

MCP342X_CHAN_FIELD = 0X60 # channel field
MCP342X_CHANNEL_1 = 0X00 # select channel 1
MCP342X_CHANNEL_2 = 0X20 # select channel 2
MCP342X_CHANNEL_3 = 0X40 # select channel 3
MCP342X_CHANNEL_4 = 0X50 # select channel 4

MCP342X_START = 0X80
MCP342X_BUSY = 0X80


adc_address1 = 0x68
adc_address2 = 0x69

adc_channel1 = 0x98
adc_channel2 = 0xB8
adc_channel3 = 0xD8
adc_channel4 = 0xF8

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
	
#bus.transaction(i2c.writing_bytes(adc_address1, 0X00, 0X0C))


	def getadcreading(address, channel, gain, res):
		channel = channel - 1
		adcConfig = MCP342X_START | MCP342X_CHANNEL_1 | MCP342X_CONTINUOUS
		adcConfig |= channel << 5 | res << 2 | gain
		#print("adcConfig")
		#print(adcConfig)
		
		varDivisior = 1 << (gain + 2*res)
		
		bus.transaction(i2c.writing_bytes(address, adcConfig))
		
		
		time.sleep(0.05)
		if (res ==3):
			h, m, l ,s = bus.transaction(i2c.reading(address,4))[0]
			time.sleep(0.05)
			h, m, l, s  = bus.transaction(i2c.reading(address,4))[0]
		

			t = ((h & 0b00000001) << 16) | (m << 8) | l
		else:
			h, m, l = bus.transaction(i2c.reading(address,3))[0]
			time.sleep(0.05)
			h, m, l  = bus.transaction(i2c.reading(address,3))[0]
			t = (h << 8) | m	
		if (h > 128):
			t = ~(0x020000 - t)

		# remove / 1000 to return value in milivolts
		return ((t/varDivisior) * 2.4705882) / 1000
	
	while True:
		gain = 0
		res = 3
		
		
		print ("Channel 1: %02f" % getadcreading(adc_address1, 1, gain, res))
		print ("Channel 2: %02f" % getadcreading(adc_address1, 2, gain, res))
		print ("Channel 3: %02f" % getadcreading(adc_address1, 3, gain, res))
		print ("Channel 4: %02f" % getadcreading(adc_address1, 4, gain, res))
		
		print ("Channel 5: %02f" % getadcreading(adc_address2, 1, gain, res))
		print ("Channel 6: %02f" % getadcreading(adc_address2, 2, gain, res))
		print ("Channel 7: %02f" % getadcreading(adc_address2, 3, gain, res))
		print ("Channel 8: %02f" % getadcreading(adc_address2, 4, gain, res))
		
		time.sleep(0.2)	
