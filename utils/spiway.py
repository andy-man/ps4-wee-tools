#==========================================================
# SPIWAY (original idea by Judges)
# https://github.com/hjudges/NORway
# part of ps4 wee tools project
#==========================================================
import time
from lang._i18n_ import *
from utils.serial import WeeSerial



class SpiFlasher(WeeSerial):
	
	VERSION			= [0,60] # Teensy programm version here
	DISABLE_PULLUPS	= 0
	
	BUFFER			= b''
	BUFFER_SIZE		= 0x8000
	
	ICs = [
		# Ven_ID Dev_ID Brand Type Blocks Addr_length 3B_cmd Sec_per_block Sec_count
		[0xC2,	0x1920,	'Macronix',	'MX25L25635F',	512,	4],
		[0xC2,	0x1820,	'Macronix',	'MX25L12872F',	256,	3],
		[0xC2,	0x1120,	'Macronix',	'MX25L1006E',	2,		3],
		
		[0xEF,	0x10,	'Winbond',	'W25X10CL',		2,		3],
		[0xEF,	0x13,	'Winbond',	'W25Q80BV',		16,		3],
		[0xEF,	0x1940,	'Winbond',	'W25Q256FV',	512,	4,	1],
		[0xEF,	0x1570,	'Winbond',	'25Q16JVXXM',	32,		3],
		[0xEF,	0x1540,	'Winbond',	'25Q16JVXXQ',	32,		3],
		[0xEF,	0x60,	'Winbond',	'W25Q128JW',	256,	3],
		
		[0x01,	0x1960,	'Cypress/Spansion',	'S25FL256L',	512,	4],
	]
	
	# Main config
	class Config:
		IC_ID			= 0
		VENDOR_ID		= 0
		DEVICE_ID		= 0
		BRAND			= STR_UNKNOWN
		TYPE			= STR_UNKNOWN
		BLOCK_COUNT		= 0
		ADDR_LEN		= 0
		USE_3B_CMD		= 0
		SEC_PER_BLOCK	= 0
		SEC_SIZE		= 0
		BLOCK_SIZE		= 0
		SEC_COUNT		= 0
		TOTAL_SIZE		= 0
		
		@classmethod
		def reset(cls):
			cls.load([0]*12)
		
		@classmethod
		def load(cls, cfg, id = 0):
			
			cls.IC_ID			= id + 1
			cls.VENDOR_ID		= cfg[0]
			cls.DEVICE_ID		= cfg[1]
			cls.BRAND			= cfg[2]
			cls.TYPE			= cfg[3]
			cls.BLOCK_COUNT		= cfg[4]
			cls.ADDR_LEN		= cfg[5]
			cls.USE_3B_CMD		= cfg[6] if len(cfg) > 6 else 0
			cls.SEC_PER_BLOCK	= cfg[7] if len(cfg) > 7 else 16
			cls.SEC_SIZE		= cfg[8] if len(cfg) > 8 else 0x1000
			
			cls.BLOCK_SIZE		= cls.SEC_PER_BLOCK	* cls.SEC_SIZE
			cls.SEC_COUNT		= cls.SEC_PER_BLOCK	* cls.BLOCK_COUNT
			cls.TOTAL_SIZE		= cls.BLOCK_SIZE	* cls.BLOCK_COUNT
	
	# Teensy commands
	class Cmd:
		PING1				= 0
		PING2				= 1
		BOOTLOADER			= 2
		IO_LOCK				= 3
		IO_RELEASE			= 4
		PULLUPS_DISABLE		= 5
		PULLUPS_ENABLE		= 6
		SPI_ID				= 7
		SPI_READBLOCK		= 8
		SPI_WRITESECTOR		= 9
		SPI_ERASEBLOCK		= 10
		SPI_ERASECHIP		= 11
		SPI_3BYTE_ADDRESS	= 12
		SPI_4BYTE_ADDRESS	= 13
		SPI_3BYTE_CMDS		= 14
		SPI_4BYTE_CMDS		= 15
	
	def __init__(self, port, ver = False):
		if port:
			super().__init__(port, {'baudrate':9600, 'timeout':300, 'write_timeout':120})
		
		self.BUFFER = b''
		self.DISABLE_PULLUPS = 0
		if ver != False:
			self.VERSION = ver
	
	# Private methods
	
	def __write(self, s):
		try:
			if isinstance(s, int):
				s = s.to_bytes(1,'big')
			elif isinstance(s,tuple) or isinstance(s,list):
				s = bytes(s)
			
			self.BUFFER += s
			
			while len(self.BUFFER) > self.BUFFER_SIZE:
				self.sp.write(self.BUFFER[:self.BUFFER_SIZE])
				self.BUFFER = self.BUFFER[self.BUFFER_SIZE:]
		except Exception as e:
			self.error(str(e))
	
	def __flush(self):
		try:
			if len(self.BUFFER):
				self.sp.write(self.BUFFER)
				self.sp.flush()
				self.BUFFER = b''
		except Exception as e:
			self.error(str(e))
	
	def __read(self, size):
		self.__flush()
		try:
			data = self.sp.read(size)
			return data
		except Exception as e:
			self.error(str(e))
			return b''
	
	# Main stuff
	
	def __setConfig(self, ven_id = False, dev_id = False):
		
		self.Config.reset()
		
		if ven_id == False and dev_id == False:
			return False
		
		for id in range(len(self.ICs)):
			cfg = self.ICs[id]
			if cfg[0] == ven_id and cfg[1] == dev_id:
				self.Config.load(cfg, id)
				return id
		
		self.Config.VENDOR_ID = ven_id
		self.Config.DEVICE_ID = dev_id
		self.error(STR_SPW_ERROR_CHIP)
		
		return False
	
	def __setAddress(self, address):
		# set address (msb first)
		self.__write((address >> 24) & 0xFF)
		self.__write((address >> 16) & 0xFF)
		self.__write((address >> 8) & 0xFF)
		self.__write(address & 0xFF)
	
	def __setMode(self):
		self.__write(self.Cmd.SPI_3BYTE_ADDRESS if self.Config.ADDR_LEN == 3 else self.Cmd.SPI_4BYTE_ADDRESS)
		self.__write(self.Cmd.SPI_3BYTE_CMDS if self.Config.USE_3B_CMD == 1 else self.Cmd.SPI_4BYTE_CMDS)
	
	def __getStatusByCode(self, code):
		
		if code == b'K':
			return STR_OK
		if code == b'T':
			return STR_SPW_ERROR_WRITE
		if code == b'R':
			return STR_SPW_ERROR_READ
		if code == b'V':
			return STR_SPW_ERROR_VERIFY
		if code == b'P':
			return STR_SPW_ERROR_PROTECTED
		if code == b'U':
			return STR_SPW_ERROR_UNKNOWN
		
		return STR_SPW_ERROR_UNK_STATUS + ' [0x{:02X}]'.format(code[0])
	
	def __getStatus(self):
		# read status byte
		res = self.__read(1)
		
		if (res != b'K'): # K = ok
			self.error('\n '+self.__getStatusByCode(res))
			self.close()
			return False
		
		return True
	
	def __eraseBlock(self, block):
		
		self.__setMode()
		self.__write(self.Cmd.SPI_ERASEBLOCK)
		self.__setAddress(block * self.Config.BLOCK_SIZE)
		
		if self.__getStatus() == False:
			self.error(STR_SPW_ERROR_ERASE_BLK%block)
			return False
		
		return True
	
	def __readBlock(self, block):
		
		self.__setMode()
		self.__write(self.Cmd.SPI_READBLOCK)
		self.__setAddress(block * self.Config.BLOCK_SIZE)
		
		if self.__getStatus() == False:
			return False
		
		data = self.__read(self.Config.BLOCK_SIZE)
		return data
	
	def __writeSector(self, data, sector):
		if len(data) != self.Config.SEC_SIZE:
			self.error(STR_SPW_ERROR_DATA_SIZE%(len(data)))
		
		self.__setMode()
		self.__write(self.Cmd.SPI_WRITESECTOR)
		self.__setAddress(sector * self.Config.SEC_SIZE)
		
		self.__write(data)
		
		return self.__getStatus()
	
	def __writeBlock(self, data, block, verify):
		dsize = len(data)
		
		if dsize != self.Config.BLOCK_SIZE:
			self.error(STR_SPW_ERROR_LENGTH%(dsize, self.Config.BLOCK_SIZE))
			return False
		
		sector = 0
		while sector < self.Config.SEC_PER_BLOCK:
			real_sector = (block * self.Config.SEC_PER_BLOCK) + sector
			if sector == 0:
				self.__eraseBlock(block)
			
			res = 1
			self.__writeSector(data[sector*self.Config.SEC_SIZE:(sector+1)*self.Config.SEC_SIZE], real_sector)
			if res == False:
				return False
			
			sector += 1
		
		# verification
		if verify == 1:
			res = self.__readBlock(block)
			if res == False or data != res:
				self.error(STR_SPW_ERROR_BLK_CHK%block)
				return  -1
		
		return True
	
	def __checkBC(self, block, count):
		
		if block >= self.Config.BLOCK_COUNT:
			block = self.Config.BLOCK_COUNT - 1
		
		if count == 0 or (block + count) > self.Config.BLOCK_COUNT:
			count = self.Config.BLOCK_COUNT - block
		
		return [block, count]
	
	# Public methods
	
	def bootloader(self):
		self.__write(self.Cmd.BOOTLOADER)
		self.__flush()
	
	def reset(self):
		# TODO: Find a way to reset, there is no cmd for reset in Teensy FW
		self.__flush()
		self.BUFFER = b''
	
	def ping(self):
		self.__write(self.Cmd.PING1)
		self.__write(self.Cmd.PING2)
		
		info = self.__read(4)
		info = b'\x00'*4 if len(info) != 4 else info
		
		ver = [info[0], info[1]]
		ram = (info[2] << 8) | info[3]
		
		if ver != self.VERSION:
			maj, min = self.VERSION
			self.error(STR_SPW_ERROR_VERSION%(maj, min))
			self.close()
		
		return {'RAM':ram, 'VER':ver}
	
	def getChipId(self):
		self.__write(self.Cmd.PULLUPS_DISABLE if self.DISABLE_PULLUPS else self.Cmd.PULLUPS_ENABLE)
		self.__write(self.Cmd.SPI_ID)
		
		info = self.__read(3)
		info = b'\x00'*3 if len(info) != 3 else info
		
		ven_id = info[0]
		dev_id = (info[2] << 8) | info[1]
		
		self.__setConfig(ven_id, dev_id)
	
	def getChipInfo(self):
		self.getChipId()
		cfg = self.Config
		
		info = {
			'Vendor / Device'	: '0x%02X / 0x%04X'%(cfg.VENDOR_ID, cfg.DEVICE_ID),
			'Brand'				: cfg.BRAND,
			'Chip type'			: cfg.TYPE,
			'Chip size'			: '%d MB'%(cfg.TOTAL_SIZE // 1024**2),
			'Sector size'		: '%d bytes'%cfg.SEC_SIZE,
			'Block size'		: '%d bytes'%cfg.BLOCK_SIZE,
			'Flash config'		: '%d:%d | %d | %d | %d'%(cfg.ADDR_LEN, cfg.USE_3B_CMD, cfg.SEC_PER_BLOCK, cfg.BLOCK_COUNT, cfg.SEC_COUNT),
		}
		
		return info
	
	def eraseChip(self, block = 0, count = 0):
		
		block, count = self.__checkBC(block, count)
		
		# Doesn't allow to handle progress
		#self.__write(self.Cmd.SPI_ERASECHIP) 
		
		kb_pb = self.Config.BLOCK_SIZE // 1024
		total = count * kb_pb
		
		start = time.time()
		
		for b in range(block, block+count):
			res = self.__eraseBlock(block)
			if res == False:
				self.error(STR_SPW_ERROR_ERASE)
				return False
			progress = (b - block + 1) * kb_pb
			percent = 100 if progress == total else progress // (total / 100)
			elapsed = UI.cyan(STR_SECONDS.format(time.time() - start))
			
			self.printf(STR_SPW_PROGRESS%(b, progress, total, percent, elapsed), True)
		
		return True
	
	def readChip(self, block = 0, count = 0):
		
		block, count = self.__checkBC(block, count)
		
		data = bytes()
		kb_pb = self.Config.BLOCK_SIZE // 1024
		total = count * kb_pb
		
		start = time.time()
		
		for b in range(block, block+count):
			buf = self.__readBlock(b)
			if buf == False:
				return False
			data += buf
			
			progress = (b - block + 1) * kb_pb
			percent = 100 if progress == total else progress // (total / 100)
			elapsed = UI.cyan(STR_SECONDS.format(time.time() - start))
			
			self.printf(STR_SPW_PROGRESS%(b, progress, total, percent, elapsed), True)
		
		return data
	
	def writeChip(self, data, verify = 0, block = 0, count = 0):
		dsize = len(data)
		
		block, count = self.__checkBC(block, count)
		
		if dsize % self.Config.BLOCK_SIZE:
			self.error(STR_SPW_ERR_BLOCK_ALIGN%self.Config.BLOCK_SIZE)
			return False
		
		if dsize != count * self.Config.BLOCK_SIZE:
			self.error(STR_SPW_ERR_DATA_SIZE%(dsize, count * self.Config.BLOCK_SIZE))
			return False
		
		if block + count > self.Config.BLOCK_COUNT:
			self.error(STR_SPW_ERR_OVERFLOW%self.Config.BLOCK_COUNT)
			return False
		
		kb_pb = self.Config.BLOCK_SIZE // 1024
		total = count * kb_pb
		
		start = time.time()
		
		for b in range(block, block + count):
			
			offset = self.Config.BLOCK_SIZE * (block - b)
			
			res = self.__writeBlock(data[offset:offset + self.Config.BLOCK_SIZE], b, verify)
			if res == False:
				self.error(STR_SPW_ERROR_WRITE)
				return False
			"""
			time.sleep(0.01)
			"""
			progress = (b - block + 1) * kb_pb
			percent = 100 if progress == total else progress // (total / 100)
			elapsed = UI.cyan(STR_SECONDS.format(time.time() - start))
			
			self.printf(STR_SPW_PROGRESS%(b, progress, total, percent, elapsed), True)
			
			b += 1
		
		return True