#==========================================================
# spiway (original idea by hjudges)
# part of ps4 wee tools project
#==========================================================
import sys
from lang._i18n_ import *
import utils.serial



class SpiFlasher(WeeSerial):
	# SECTORS': 16,	'SEC_SIZE: 0x1000
	configs = [
		{'VENDOR_ID': 0xC2,	'DEVICE_ID': 0x18,	'BRAND': 'Macronix',	'TYPE': 'MX25L25635F',	'BLOCKS': 512,	'ADDR_LEN': 4,	'B3_CMD': 0},
		{'VENDOR_ID': 0xC2,	'DEVICE_ID': 0x10,	'BRAND': 'Macronix',	'TYPE': 'MX25L1006E',	'BLOCKS': 2,	'ADDR_LEN': 3,	'B3_CMD': 0},
		
		{'VENDOR_ID': 0xEF,	'DEVICE_ID': 0x10,	'BRAND': 'Winbond',		'TYPE': 'W25X10CL',		'BLOCKS': 2,	'ADDR_LEN': 3,	'B3_CMD': 0},
		{'VENDOR_ID': 0xEF,	'DEVICE_ID': 0x13,	'BRAND': 'Winbond',		'TYPE': 'W25Q80BV',		'BLOCKS': 16,	'ADDR_LEN': 3,	'B3_CMD': 0},
		{'VENDOR_ID': 0xEF,	'DEVICE_ID': 0x18,	'BRAND': 'Winbond',		'TYPE': 'W25Q256FV',	'BLOCKS': 512,	'ADDR_LEN': 4,	'B3_CMD': 1},
	]
	
	"""
	# Extra configs
	{'VENDOR_ID': 0xC2,	'DEVICE_ID': 0x1920,	'BRAND': 'Macronix',		'TYPE': 'MX25L25635F',	'BLOCKS': 512,	'ADDR_LEN': 4,	'B3_CMD': 0},
	{'VENDOR_ID': 0xC2,	'DEVICE_ID': 0x1820,	'BRAND': 'Macronix',		'TYPE': 'MX25L12872F',	'BLOCKS': 256,	'ADDR_LEN': 3,	'B3_CMD': 0},
	{'VENDOR_ID': 0xC2,	'DEVICE_ID': 0x1120,	'BRAND': 'Macronix',		'TYPE': 'MX25L1006E',	'BLOCKS': 2,	'ADDR_LEN': 3,	'B3_CMD': 0},
	
	{'VENDOR_ID': 0xEF,	'DEVICE_ID': 0x0010,	'BRAND': 'Winbond',			'TYPE': 'W25X10CL',		'BLOCKS': 2,	'ADDR_LEN': 3,	'B3_CMD': 0},
	{'VENDOR_ID': 0xEF,	'DEVICE_ID': 0x0013,	'BRAND': 'Winbond',			'TYPE': 'W25Q80BV',		'BLOCKS': 16,	'ADDR_LEN': 3,	'B3_CMD': 0},
	{'VENDOR_ID': 0xEF,	'DEVICE_ID': 0x1940,	'BRAND': 'Winbond',			'TYPE': 'W25Q256FV',	'BLOCKS': 512,	'ADDR_LEN': 4,	'B3_CMD': 1},
	{'VENDOR_ID': 0xEF,	'DEVICE_ID': 0x1570,	'BRAND': 'Winbond',			'TYPE': '25Q16JVXXM',	'BLOCKS': 32,	'ADDR_LEN': 3,	'B3_CMD': 0},
	{'VENDOR_ID': 0xEF,	'DEVICE_ID': 0x1540,	'BRAND': 'Winbond',			'TYPE': '25Q16JVXXQ',	'BLOCKS': 32,	'ADDR_LEN': 3,	'B3_CMD': 0},
	{'VENDOR_ID': 0xEF,	'DEVICE_ID': 0x0060,	'BRAND': 'Winbond',			'TYPE': 'W25Q128JW',	'BLOCKS': 256,	'ADDR_LEN': 3,	'B3_CMD': 0},
	
	{'VENDOR_ID': 0x01,	'DEVICE_ID': 0x1960,	'BRAND': 'Cypress/Spansion','TYPE': 'S25FL256L',	'BLOCKS': 512,	'ADDR_LEN': 4,	'B3_CMD': 0},
	"""
	
	status = {
		b'K': 'OK',
		b'T': "RY/BY timeout error while writing!",
		b'R': "Teensy receive buffer timeout! Disconnect and reconnect Teensy!",
		b'V': "Verification error!",
		b'P': "Device is write-protected!",
		b'U': "Received unknown error! (Got 0x%02x)",
	}
	
	VERSION_MAJOR = 0
	VERSION_MINOR = 0
	
	VENDOR_ID = 0
	DEVICE_ID = 0
	
	# Config
	SPI_DISABLE_PULLUPS		= 0
	SPI_SECTOR_SIZE			= 0
	SPI_TOTAL_SECTORS		= 0
	SPI_BLOCK_COUNT			= 0
	SPI_SECTORS_PER_BLOCK	= 0
	SPI_BLOCK_SIZE			= 0
	SPI_ADDRESS_LENGTH		= 0
	SPI_USE_3BYTE_CMDS		= 0
	
	# Teensy commands
	CMD_PING1				= 0
	CMD_PING2				= 1
	CMD_BOOTLOADER			= 2
	CMD_IO_LOCK				= 3
	CMD_IO_RELEASE			= 4
	CMD_PULLUPS_DISABLE		= 5
	CMD_PULLUPS_ENABLE		= 6
	CMD_SPI_ID				= 7
	CMD_SPI_READBLOCK		= 8
	CMD_SPI_WRITESECTOR		= 9
	CMD_SPI_ERASEBLOCK		= 10
	CMD_SPI_ERASECHIP		= 11
	CMD_SPI_3BYTE_ADDRESS	= 12
	CMD_SPI_4BYTE_ADDRESS	= 13
	CMD_SPI_3BYTE_CMDS		= 14
	CMD_SPI_4BYTE_CMDS		= 15
	
	def __init__(self, port, ver_major, ver_minor):
		if port:
			super().__init__(self, port, {'baudrate':9600, 'timeout':300, 'write_timeout':120})
		self.SPI_DISABLE_PULLUPS = 0
		self.VERSION_MAJOR = ver_major
		self.VERSION_MINOR = ver_minor
	
	def readId(self):
		self.write(self.CMD_PULLUPS_ENABLE if self.SPI_DISABLE_PULLUPS == 0 else self.CMD_PULLUPS_DISABLE)
		self.write(self.CMD_SPI_ID)
		
		spi_info = self.read(2)
		
		self.VENDOR_ID = ord(spi_info[0])
		self.DEVICE_ID = ord(spi_info[1])
		
		self.loadConfig()
	
	def loadConfig(self, vendor = False, device = False):
		
		vendor = vendor if vendor else self.VENDOR_ID
		device = device if device else self.DEVICE_ID
		
		for n in self.configs:
			cfg = self.configs[n]
			if cfg['VENDOR_ID'] == vendor and cfg['DEVICE_ID'] == device:
				self.cfg = cfg
	
	def ping(self):
		self.write(self.CMD_PING1)
		self.write(self.CMD_PING2)
		
		ver_major = self.readbyte()
		ver_minor = self.readbyte()
		
		freeram = (self.readbyte() << 8) | self.readbyte()
		
		if (ver_major != self.VERSION_MAJOR) or (ver_minor != self.VERSION_MINOR):
			self.close()
			self.error("Ping failed (expected v%d.%02d, got v%d.%02d)"%(self.VERSION_MAJOR, self.VERSION_MINOR, ver_major, ver_minor))
			return 0
		
		return freeram
	
	def getChipInfo(self):
		self.readId()
		info = {
			'Vendor / Device'	: '[0x%02x / 0x%02x]'%(self.VENDOR_ID, self.DEVICE_ID),
			'Brand'				: '%s (0x%02x)'%(STR_UNKNOWN, self.VENDOR_ID),
			'Chip type'			: unknown (0x%02x)"%self.DEVICE_ID)
			'Chip size'			: %d MB"%(self.SPI_BLOCK_SIZE * self.SPI_BLOCK_COUNT / 1024 / 1024))
			'Sector size'		: %d bytes"%(self.SPI_SECTOR_SIZE))
			'Block size'		: %d bytes"%(self.SPI_BLOCK_SIZE))
			'Sectors per block'	: %d"%(self.SPI_SECTORS_PER_BLOCK))
			'Number of blocks'	: %d"%(self.SPI_BLOCK_COUNT))
			'Number of sectors'	: '%d'%self.SPI_TOTAL_SECTORS,
		}
		return info
	
	def bootloader(self):
		self.write(self.CMD_BOOTLOADER)
		self.flush()
	
	def setAddress(self, address):
		# set address (msb first)
		self.write((address >> 24) & 0xFF)
		self.write((address >> 16) & 0xFF)
		self.write((address >> 8) & 0xFF)
		self.write(address & 0xFF)
	
	def setMode(self):
		self.write(self.CMD_SPI_3BYTE_ADDRESS	if self.SPI_ADDRESS_LENGTH == 3 else self.CMD_SPI_4BYTE_ADDRESS)
		self.write(self.CMD_SPI_4BYTE_CMDS		if self.SPI_USE_3BYTE_CMDS == 0 else self.CMD_SPI_3BYTE_CMDS)
	
	def getStatus(self):
		# read status byte
		res = self.read(1)
		
		if (res != b'K'): # K = ok
			self.error(self.status[res] if c in self.status else self.status[b'U']%res)
			self.close()
			return 0
		
		return 1
	
	def eraseChip(self):
		self.write(self.CMD_SPI_ERASECHIP)
		
		if self.getStatus() == 0:
			self.error("Error erasing chip!")
			return 0
		
		return 1
	
	def eraseBlock(self, block):
		
		self.setMode()
		self.write(self.CMD_SPI_ERASEBLOCK)
		self.setAddress(block * self.SPI_BLOCK_SIZE)
		
		if self.getStatus() == 0:
			self.error("Block %d - error erasing block"%block)
			return 0
		
		return 1
	
	def readBlock(self, block):
		
		self.setMode()
		self.write(self.CMD_SPI_READBLOCK)
		self.setAddress(block * self.SPI_BLOCK_SIZE)
		
		if self.getStatus() == 0:
			return False
		
		data = self.read(self.SPI_BLOCK_SIZE)
		return data
	
	def writeSector(self, data, sector):
		if len(data) != self.SPI_SECTOR_SIZE:
			self.error("Incorrent data size %d"%(len(data)))
		
		self.setMode()
		self.write(self.CMD_SPI_WRITESECTOR)
		self.setAddress(sector * self.SPI_SECTOR_SIZE)
		
		self.write(data)
		
		return 0 if self.getStatus() == 0 else 1
	
	def writeBlock(self, data, block, verify):
		datasize = len(data)
		if datasize != self.SPI_BLOCK_SIZE:
			self.error("Incorrect length %d != %d!"%(datasize, self.SPI_BLOCK_SIZE))
			return -1
		
		sector = 0
		while sector < self.SPI_SECTORS_PER_BLOCK:
			real_sector = (block * self.SPI_SECTORS_PER_BLOCK) + sector
			if sector == 0:
				self.eraseBlock(block)
			
			self.writeSector(data[sector*self.SPI_SECTOR_SIZE:(sector+1)*self.SPI_SECTOR_SIZE], real_sector)
			
			sector += 1
		
		# verification
		if verify == 1:
			res = self.readBlock(block)
			if res == False or data != res:
				self.error("Error! Block verification failed (block=%d)."%block)
				return  -1
		
		return 0
	
	def dump(self, filename, block, count):
		fo = open(filename,"wb")
		
		if count == 0 or count > self.SPI_BLOCK_COUNT:
			count = self.SPI_BLOCK_COUNT
		
		for b in range(block, (block+count), 1):
			data = self.readBlock(b)
			fo.write(data)
			self.printf("%d KB / %d KB"%((b-block+1)*self.SPI_BLOCK_SIZE//1024, count*self.SPI_BLOCK_SIZE//1024), True)
		
		return
	
	def program(self, data, verify, start, count):
		datasize = len(data)
		
		if count == 0:
			count = self.SPI_BLOCK_COUNT - start
		
		if datasize % self.SPI_BLOCK_SIZE:
			self.error("Error: expecting file size to be a multiplication of block size: %d"%(self.SPI_BLOCK_SIZE))
			return -1
		
		if start + count > datasize // self.SPI_BLOCK_SIZE:
			self.error("Error: file is %d bytes long and last block is at %d!"%(datasize, (start + count + 1) * self.SPI_BLOCK_SIZE))
			return -1
		
		if start + count > self.SPI_BLOCK_COUNT:
			self.error("Error: chip has %d blocks. Writing outside the chip's capacity!"%self.SPI_BLOCK_COUNT)
			return -1
		
		self.printf("Writing %d blocks to device (starting at block %d)"%(count, start))
		b = 0
		while b < count:
			block = start + b
			self.writeBlock(data[block*self.SPI_BLOCK_SIZE:(block+1)*self.SPI_BLOCK_SIZE], block, verify)
			self.printf("%d KB / %d KB"%(((block+1)*self.SPI_BLOCK_SIZE)/1024, (count*self.SPI_BLOCK_SIZE)/1024), True)
			
			b += 1