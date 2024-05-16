#==========================================================
# SPIWAY (original idea by Judges)
# https://github.com/hjudges/NORway
# part of ps4 wee tools project
# https://github.com/andy-man/ps4-wee-tools
#==========================================================
import time
from lang._i18n_ import *
from utils.serial import WeeSerial



class SpiFlasher(WeeSerial):
	
	VERSION			= [0,60] # Teensy programm HW version here
	DISABLE_PULLUPS	= 0
	
	BUFFER			= b''
	BUFFER_SIZE		= 0x8000
	
	ICs = [
		#Ven_ID	Dev_ID	Brand Type	Blocks	Addr_length	3B_cmd	Sec_per_block	Sec_count
		[0xC2,	0x1920,	'Macronix',	'MX25L25635F',	512,	4,	0],
		[0xC2,	0x1820,	'Macronix',	'MX25L12872F',	256,	3,	0],
		[0xC2,	0x1120,	'Macronix',	'MX25L1006E',	2,		3,	0],
		
		[0xEF,	0x10,	'Winbond',	'W25X10CL',		2,		3,	0],
		[0xEF,	0x13,	'Winbond',	'W25Q80BV',		16,		3,	0],
		[0xEF,	0x1940,	'Winbond',	'W25Q256FV',	512,	4,	1],
		[0xEF,	0x1570,	'Winbond',	'25Q16JVXXM',	32,		3,	0],
		[0xEF,	0x1540,	'Winbond',	'25Q16JVXXQ',	32,		3,	0],
		[0xEF,	0x60,	'Winbond',	'W25Q128JW',	256,	3,	0],
		
		[0x01,	0x1960,	'Spansion',	'S25FL256L',	512,	4,	0],
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
			cls.load([0]*12, -1)
		
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
		PING1				= 0  # Params: - / Return: VERSION_MAJOR[1]
		PING2				= 1  # Params: - / Return: VERSION_MINOR[1] + Freemem[2]
		BOOTLOADER			= 2  # Params: - / Return: - / Exit to bootloader mode
		IO_LOCK				= 3  # - not implemented - in spiway fw
		IO_RELEASE			= 4  # - not implemented - in spiway fw
		PULLUPS_DISABLE		= 5  # Params: - / Return: - / Set IO_PULLUPS to 0x00
		PULLUPS_ENABLE		= 6  # Params: - / Return: - / Set IO_PULLUPS to 0xFF
		SPI_ID				= 7  # Params: - / Return: VENDOR_ID[1] + DEVICE_ID[2]
		SPI_READBLOCK		= 8  # Params: ADDRESS[4] / Return: STATUS[1] + DATA[BLOCK_SIZE]
		SPI_WRITESECTOR		= 9  # Params: ADDRESS[4] + DATA[SEC_SIZE] / Return: STATUS[1]
		SPI_ERASEBLOCK		= 10 # Params: ADDRESS[4] / Return: STATUS[1]
		SPI_ERASECHIP		= 11 # Params: - / Return: STATUS[1]
		SPI_3BYTE_ADDRESS	= 12 # Params: - / Return: - / Set mode: SPI_ADDRESS_LENGTH = 3
		SPI_4BYTE_ADDRESS	= 13 # Params: - / Return: - / Set mode: SPI_ADDRESS_LENGTH = 4
		SPI_3BYTE_CMDS		= 14 # Params: - / Return: - / Set mode: SPI_USE_3B_CMDS = 1
		SPI_4BYTE_CMDS		= 15 # Params: - / Return: - / Set mode: SPI_USE_3B_CMDS = 0
		# There is no RESET command. The only way to do it unplug teensy from USB
	
	def __init__(self, port, ver = False):
		if port:
			super().__init__(port, {'baudrate':9600, 'timeout':300, 'write_timeout':120})
		
		self.BUFFER = b''
		self.DISABLE_PULLUPS = 0
		if ver != False:
			self.VERSION = ver
	
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
		self._write((address >> 24) & 0xFF)
		self._write((address >> 16) & 0xFF)
		self._write((address >> 8) & 0xFF)
		self._write(address & 0xFF)
	
	def __setMode(self):
		self._write(self.Cmd.SPI_3BYTE_ADDRESS if self.Config.ADDR_LEN == 3 else self.Cmd.SPI_4BYTE_ADDRESS)
		self._write(self.Cmd.SPI_3BYTE_CMDS if self.Config.USE_3B_CMD == 1 else self.Cmd.SPI_4BYTE_CMDS)
	
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
		res = self._read(1)
		
		if (res != b'K'): # K = ok
			self.error('\n '+self.__getStatusByCode(res))
			self.close()
			return False
		
		return True
	
	def __eraseBlock(self, block):
		
		self.__setMode()
		self._write(self.Cmd.SPI_ERASEBLOCK)
		self.__setAddress(block * self.Config.BLOCK_SIZE)
		
		if self.__getStatus() == False:
			self.error(STR_SPW_ERROR_ERASE_BLK%block)
			return False
		
		return True
	
	def __readBlock(self, block):
		
		self.__setMode()
		self._write(self.Cmd.SPI_READBLOCK)
		self.__setAddress(block * self.Config.BLOCK_SIZE)
		
		if self.__getStatus() == False:
			return False
		
		data = self._read(self.Config.BLOCK_SIZE)
		return data
	
	def __writeSector(self, data, sector):
		if len(data) != self.Config.SEC_SIZE:
			self.error(STR_SPW_ERROR_DATA_SIZE%(len(data)))
		
		self.__setMode()
		self._write(self.Cmd.SPI_WRITESECTOR)
		self.__setAddress(sector * self.Config.SEC_SIZE)
		
		self._write(data)
		
		return self.__getStatus()
	
	def __writeBlock(self, data, block, verify):
		dsize = len(data)
		
		if dsize != self.Config.BLOCK_SIZE:
			self.error(STR_SPW_ERROR_LENGTH%(dsize, self.Config.BLOCK_SIZE))
			return False
		
		sector = 0
		while sector < self.Config.SEC_PER_BLOCK:
			real_sector = (block * self.Config.SEC_PER_BLOCK) + sector
			# At first erase block
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
		self._write(self.Cmd.BOOTLOADER)
		self._flush()
	
	def reset(self):
		# TODO: Find a way to reset, there is no cmd for reset in Teensy FW
		self._flush()
		self.BUFFER = b''
	
	def ping(self):
		self._write(self.Cmd.PING1)
		self._write(self.Cmd.PING2)
		
		info = self._read(4)
		info = b'\x00'*4 if len(info) != 4 else info
		
		ver = [info[0], info[1]]
		ram = (info[2] << 8) | info[3]
		
		if ver != self.VERSION:
			maj, min = self.VERSION
			self.error(STR_SPW_ERROR_VERSION%(maj, min))
			self.close()
		
		return {'RAM':ram, 'VER':ver}
	
	def getChipId(self):
		self._write(self.Cmd.PULLUPS_DISABLE if self.DISABLE_PULLUPS else self.Cmd.PULLUPS_ENABLE)
		self._write(self.Cmd.SPI_ID)
		
		info = self._read(3)
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
		
		# Check if chip config is known
		if self.Config.IC_ID <= 0: return False
		
		block, count = self.__checkBC(block, count)
		
		# Doesn't allow to handle progress
		#self._write(self.Cmd.SPI_ERASECHIP) 
		
		kb_pb = self.Config.BLOCK_SIZE // 1024
		total = count * kb_pb
		
		start = time.time()
		
		for b in range(block, block+count):
			res = self.__eraseBlock(b)
			if res == False:
				self.error(STR_SPW_ERROR_ERASE)
				return False
			progress = (b - block + 1) * kb_pb
			percent = 100 if progress == total else progress // (total / 100)
			elapsed = UI.cyan(STR_SECONDS%(time.time() - start))
			
			self.printf(STR_SPW_PROGRESS%(b, progress, total, percent, elapsed), True)
		
		return True
	
	def readChip(self, block = 0, count = 0):
		
		# Check if chip config is known
		if self.Config.IC_ID <= 0: return False
		
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
			elapsed = UI.cyan(STR_SECONDS%(time.time() - start))
			
			self.printf(STR_SPW_PROGRESS%(b, progress, total, percent, elapsed), True)
		
		return data
	
	def writeChip(self, data, verify = 0, block = 0, count = 0):
		
		# Check if chip config is known
		if self.Config.IC_ID <= 0: return False
		
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
			
			offset = self.Config.BLOCK_SIZE * (b - block)
			
			res = self.__writeBlock(data[offset:offset + self.Config.BLOCK_SIZE], b, verify)
			if res == False:
				self.error(STR_SPW_ERROR_WRITE)
				return False
			"""
			time.sleep(0.01)
			"""
			progress = (b - block + 1) * kb_pb
			percent = 100 if progress == total else progress // (total / 100)
			elapsed = UI.cyan(STR_SECONDS%(time.time() - start))
			
			self.printf(STR_SPW_PROGRESS%(b, progress, total, percent, elapsed), True)
			
			b += 1
		
		return True