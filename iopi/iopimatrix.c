/*
 abelectronics IO Pi Expander board output demo led matrix example using smbus for C
 Writes "IO Pi" to a 24 x 8 led matrix 
 Requries Python 2 and smbus
 I2C API depends on I2C support in the kernel

 Version 1.0  - 24/12/2012
 Version History:
 1.0 - Initial Release

Required package:
apt-get install libi2c-dev

Compile with gcc: 
gcc iomatrix.c -o iomatrix

Execute with:
./iomatrix

*/
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <linux/i2c-dev.h>


int fd;
char *fileName = "/dev/i2c-1"; // use "/dev/i2c-0" for first revision Raspberry Pi's
int expanderaddress1 = 0x20; // default address
int expanderaddress2 = 0x21; // default address
unsigned char buf[10]; // setup empty buffer

// declare functions
void writetoIO(int, int, int ) ;
void ClearAll();
void ClearBus1();
void ClearBus2();
void ClearBus3();

int main(int argc, char **argv) {
	printf("*** led matrix demo ***\n");
	
	if ((fd = open(fileName, O_RDWR)) < 0) {
			printf("Failed to open 12c port\n");
			exit(1);
	}

	
	
	// set both chips to be outputs each bus
	writetoIO(expanderaddress1, 0x00, 0x00);
	writetoIO(expanderaddress1, 0x01, 0x00);
	writetoIO(expanderaddress2, 0x00, 0x00);
	writetoIO(expanderaddress2, 0x01, 0x00);
	ClearAll();
	
	// loop forever writing pixel data to the led matrix
	while(1) {
	// first 8 columns
	writetoIO(expanderaddress1, 0x13, 0x80);
	writetoIO(expanderaddress1, 0x12, 0x81);
	ClearBus1();
	
	writetoIO(expanderaddress1, 0x13, 0x40);
	writetoIO(expanderaddress1, 0x12, 0xFF);
	ClearBus1();
	
	writetoIO(expanderaddress1, 0x13, 0x20);
	writetoIO(expanderaddress1, 0x12, 0x81);
	ClearBus1();
	
	writetoIO(expanderaddress1, 0x13, 0x10);
	writetoIO(expanderaddress1, 0x12, 0x00);
	ClearBus1();
	
	writetoIO(expanderaddress1, 0x13, 0x08);
	writetoIO(expanderaddress1, 0x12, 0x3C);
	ClearBus1();
	
	writetoIO(expanderaddress1, 0x13, 0x04);
	writetoIO(expanderaddress1, 0x12, 0x42);
	ClearBus1();
	
	writetoIO(expanderaddress1, 0x13, 0x02);
	writetoIO(expanderaddress1, 0x12, 0x81);
	ClearBus1();
	
	writetoIO(expanderaddress1, 0x13, 0x01);
	writetoIO(expanderaddress1, 0x12, 0x81);
	ClearBus1();
	// second 8 columns
	writetoIO(expanderaddress2, 0x12, 0x80);
	writetoIO(expanderaddress1, 0x12, 0x81);
	ClearBus2();
	
	writetoIO(expanderaddress2, 0x12, 0x40);
	writetoIO(expanderaddress1, 0x12, 0x42);
	ClearBus2();
	
	writetoIO(expanderaddress2, 0x12, 0x20);
	writetoIO(expanderaddress1, 0x12, 0x3C);
	ClearBus2();
	
	writetoIO(expanderaddress2, 0x12, 0x02);
	writetoIO(expanderaddress1, 0x12, 0xFF);
	ClearBus2();
	
	writetoIO(expanderaddress2, 0x12, 0x01);
	writetoIO(expanderaddress1, 0x12, 0x90);
	ClearBus2();
	//third 8 columns
	writetoIO(expanderaddress2, 0x13, 0x80);
	writetoIO(expanderaddress1, 0x12, 0x90);
	ClearBus3();
	
	writetoIO(expanderaddress2, 0x13, 0x40);
	writetoIO(expanderaddress1, 0x12, 0x90);
	ClearBus3();
	
	writetoIO(expanderaddress2, 0x13, 0x20);
	writetoIO(expanderaddress1, 0x12, 0x60);
	ClearBus3();
	
	writetoIO(expanderaddress2, 0x13, 0x04);
	writetoIO(expanderaddress1, 0x12, 0x2F);
		ClearBus3();
	}

}

void writetoIO(int address, int val1, int val2) {
	ioctl(fd,I2C_SLAVE,address);
	buf[0] = val1;
	buf[1] = val2;
	write(fd, buf, 2);
	

}
void ClearAll() {
	writetoIO(expanderaddress1, 0x12, 0x00);
	writetoIO(expanderaddress1, 0x13, 0x00);
	writetoIO(expanderaddress2, 0x12, 0x00);
	writetoIO(expanderaddress2, 0x13, 0x00);
}

		
void ClearBus1(){;
	writetoIO(expanderaddress1, 0x12, 0x00);
	writetoIO(expanderaddress1, 0x13, 0x00);
}
		
void ClearBus2(){
	writetoIO(expanderaddress1, 0x12, 0x00);
	writetoIO(expanderaddress2, 0x12, 0x00);
}	
void ClearBus3(){
	writetoIO(expanderaddress1, 0x12, 0x00);
	writetoIO(expanderaddress2, 0x13, 0x00);
}

