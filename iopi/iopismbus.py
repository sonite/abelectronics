#!/usr/bin/env python
# abelectronics IO Pi Expander board output demo led matrix example using smbus for python 2
# Writes "IO Pi" to a 24 x 8 led matrix 
# Requries Python 2 and smbus
# I2C API depends on I2C support in the kernel

# Version 1.0  - 24/12/2012
# Version History:
# 1.0 - Initial Release
# 
from smbus import SMBus

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

            
bus = SMBus(i2c_bus)

#set both busses as outputs on both chips
bus.write_byte_data(expander_address1, 0x00, 0x00)
bus.write_byte_data(expander_address1, 0x01, 0x00)
bus.write_byte_data(expander_address2, 0x00, 0x00)
bus.write_byte_data(expander_address2, 0x01, 0x00)

def ClearAll():
	bus.write_byte_data(expander_address1, 0x12, 0xFF)
	bus.write_byte_data(expander_address1, 0x13, 0x00)
	bus.write_byte_data(expander_address2, 0x12, 0x00)
	bus.write_byte_data(expander_address2, 0x13, 0x00)
		
def ClearBus1():
	bus.write_byte_data(expander_address1, 0x12, 0xFF)
	bus.write_byte_data(expander_address1, 0x13, 0x00)
		
def ClearBus2():
	bus.write_byte_data(expander_address1, 0x12, 0xFF)
	bus.write_byte_data(expander_address2, 0x12, 0x00)
		
def ClearBus3():
	bus.write_byte_data(expander_address1, 0x12, 0xFF)
	bus.write_byte_data(expander_address2, 0x13, 0x00)
	
ClearAll()
		
# cycle outputs to build image
while True:		
	# first 8 columns
	bus.write_byte_data(expander_address1, 0x13, 0x80)
	bus.write_byte_data(expander_address1, 0x12, 0x7E)
	ClearBus1()
	
	bus.write_byte_data(expander_address1, 0x13, 0x40)
	bus.write_byte_data(expander_address1, 0x12, 0x00)
	ClearBus1()
	
	bus.write_byte_data(expander_address1, 0x13, 0x20)
	bus.write_byte_data(expander_address1, 0x12, 0x7E)
	ClearBus1()
	
	bus.write_byte_data(expander_address1, 0x13, 0x10)
	bus.write_byte_data(expander_address1, 0x12, 0xFF)
	ClearBus1()
	
	bus.write_byte_data(expander_address1, 0x13, 0x08)
	bus.write_byte_data(expander_address1, 0x12, 0xC3)
	ClearBus1()
	
	bus.write_byte_data(expander_address1, 0x13, 0x04)
	bus.write_byte_data(expander_address1, 0x12, 0xBD)
	ClearBus1()
	
	bus.write_byte_data(expander_address1, 0x13, 0x02)
	bus.write_byte_data(expander_address1, 0x12, 0x7E)
	ClearBus1()
	
	bus.write_byte_data(expander_address1, 0x13, 0x01)
	bus.write_byte_data(expander_address1, 0x12, 0x7E)
	ClearBus1()
	# second 8 columns
	bus.write_byte_data(expander_address2, 0x12, 0x80)
	bus.write_byte_data(expander_address1, 0x12, 0x7E)
	ClearBus2()
	
	bus.write_byte_data(expander_address2, 0x12, 0x40)
	bus.write_byte_data(expander_address1, 0x12, 0xBD)
	ClearBus2()
	
	bus.write_byte_data(expander_address2, 0x12, 0x20)
	bus.write_byte_data(expander_address1, 0x12, 0x3C)
	ClearBus2()
	
	bus.write_byte_data(expander_address2, 0x12, 0x02)
	bus.write_byte_data(expander_address1, 0x12, 0x00)
	ClearBus2()
	
	bus.write_byte_data(expander_address2, 0x12, 0x01)
	bus.write_byte_data(expander_address1, 0x12, 0x6F)
	ClearBus2()
	
	# third 8 columns
	bus.write_byte_data(expander_address2, 0x13, 0x80)
	bus.write_byte_data(expander_address1, 0x12, 0x6F)
	ClearBus3()
	
	bus.write_byte_data(expander_address2, 0x13, 0x40)
	bus.write_byte_data(expander_address1, 0x12, 0x6F)
	ClearBus3()
	
	bus.write_byte_data(expander_address2, 0x13, 0x20)
	bus.write_byte_data(expander_address1, 0x12, 0x9F)
	ClearBus3()
	
	bus.write_byte_data(expander_address2, 0x13, 0x04)
	bus.write_byte_data(expander_address1, 0x12, 0x7E)
	ClearBus3()
	
	bus.write_byte_data(expander_address2, 0x13, 0x02)
	bus.write_byte_data(expander_address1, 0x12, 0x00)
	ClearBus3()
	
	bus.write_byte_data(expander_address2, 0x13, 0x01)
	bus.write_byte_data(expander_address1, 0x12, 0x7E)
	ClearBus3()