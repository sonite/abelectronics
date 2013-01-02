#!/usr/bin/env python3
# abelectronics IO Pi Expander board output demo led matrix example
# uses quick2wire from http://quick2wire.com/ github: https://github.com/quick2wire/quick2wire-python-api
# Requries Python 3 
# GPIO API depends on Quick2Wire GPIO Admin. To install Quick2Wire GPIO Admin, follow instructions at http://github.com/quick2wire/quick2wire-gpio-admin
# I2C API depends on I2C support in the kernel

# Version 1.0  - 24/12/2012
# Version History:
# 1.0 - Initial Release
# 
import quick2wire.i2c as i2c
import time
import re

expander_address1 = 0x20
expander_address2 = 0x21


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
	def ClearAll():
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0xFF))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0x00))
		bus.transaction(i2c.writing_bytes(expander_address2, 0x12, 0x00))
		bus.transaction(i2c.writing_bytes(expander_address2, 0x13, 0x00))
		
	def ClearBus1():
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0xFF))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0x00))
		
	def ClearBus2():
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0xFF))
		bus.transaction(i2c.writing_bytes(expander_address2, 0x12, 0x00))
		
	def ClearBus3():
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0xFF))
		bus.transaction(i2c.writing_bytes(expander_address2, 0x13, 0x00))
	
	ClearAll()
	# cycle outputs to build image
	while True:
		# first 8 columns
		
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0x80))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x7E))
		ClearBus1()
		
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0x40))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x00))
		ClearBus1()
		
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0x20))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x7E))
		ClearBus1()
		
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0x10))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0xFF))
		ClearBus1()
		
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0x08))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0xC3))
		ClearBus1()
		
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0x04))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0xBD))
		ClearBus1()
		
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0x02))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x7E))
		ClearBus1()
		
		bus.transaction(i2c.writing_bytes(expander_address1, 0x13, 0x01))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x7E))
		ClearBus1()
		# second 8 columns
		bus.transaction(i2c.writing_bytes(expander_address2, 0x12, 0x80))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x7E))
		ClearBus2()
		
		bus.transaction(i2c.writing_bytes(expander_address2, 0x12, 0x40))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0xBD))
		ClearBus2()
		
		bus.transaction(i2c.writing_bytes(expander_address2, 0x12, 0x20))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0xC3))
		ClearBus2()
		
		bus.transaction(i2c.writing_bytes(expander_address2, 0x12, 0x02))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x00))
		ClearBus2()
		
		bus.transaction(i2c.writing_bytes(expander_address2, 0x12, 0x01))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x6F))
		ClearBus2()
		# third 8 columns
		bus.transaction(i2c.writing_bytes(expander_address2, 0x13, 0x80))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x6F))
		ClearBus3()
		
		bus.transaction(i2c.writing_bytes(expander_address2, 0x13, 0x40))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x6F))
		ClearBus3()
		
		bus.transaction(i2c.writing_bytes(expander_address2, 0x13, 0x20))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x9F))
		ClearBus3()
		
	
		bus.transaction(i2c.writing_bytes(expander_address2, 0x13, 0x04))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x7E))
		ClearBus3()
		
		bus.transaction(i2c.writing_bytes(expander_address2, 0x13, 0x02))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x00))
		ClearBus3()
		
		bus.transaction(i2c.writing_bytes(expander_address2, 0x13, 0x01))
		bus.transaction(i2c.writing_bytes(expander_address1, 0x12, 0x7E))
		ClearBus3()
		
		
		
		
		
