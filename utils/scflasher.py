#==========================================================
# Syscon flasher by Abkarino & EgyCnq
# https://github.com/AbkarinoMHM/PS4SysconTools
# part of ps4 wee tools project
#==========================================================

import time, sys
import utils.syscon as Syscon
from lang._i18n_ import *
from utils.serial import WeeSerial



class SysconFlasher(WeeSerial):
	
	VERSION                 = [2, 1] # Syscon flasher HW version here
	
	BUFFER                  = b''
	BUFFER_SIZE             = 0x8000
	
	class Cmd:
		PING1           = 0x00  # Params: - / Return: VERSION_MAJOR[1] / Check if Syscon tool connected and get its version major value
		PING2           = 0x01  # Params: - / Return: VERSION_MINOR[1] + FREEMEM[2] / Check if Syscon tool connected and get its version minor value + free ram size
		READ_BLOCK      = 0x02  # Params: START_BLOCK[2] + END_BLOCK[2] / Return: STATUS[1] + DATA[BLOCK_SIZE] / Read block data
		READ_CHIP       = 0x03  # Params: - / Return: STATUS[1] / Erase full chip data
		ERASE_BLOCK     = 0x04  # Params: START_BLOCK[2] + END_BLOCK[2] / Return: STATUS[1] / Erase block data
		ERASE_CHIP      = 0x05  # Params: - / Return: STATUS[1] / Erase full chip data
		WRITE_BLOCK     = 0x06  # Params: BLOCK_NUM[2] + DATA[BLOCK_SIZE] / Return: STATUS[1] / Write block data
		WRITE_BLOCK_EX  = 0x07  # Params: BLOCK_NUM[2] + DATA[BLOCK_SIZE] / Return: STATUS[1] / Extended Write block data
		SET_DATA        = 0x0A  # Params: ?? / Return: ?? / Set data to be written into syscon write buffer
		INIT            = 0x10  # Params: - / Return: STATUS[1] / Initialize syscon flasher
		UNINIT          = 0x20  # Params: - / Return: STATUS[1] / Uninitialize syscon flasher
		RESET           = 0x80  # Params: - / Return: - / Reset syscon flasher
	
	class Config:
		BLOCK_SIZE			= 0x400
		BLOCK_COUNT			= 512
		TOTAL_SIZE			= BLOCK_SIZE * BLOCK_COUNT
	
	# Private methods
	
	def __init__(self, port, ver = False):
		if port:
			super().__init__(port, {'baudrate':115200, 'timeout':10, 'write_timeout':5})
		
		self.BUFFER = b''
		if ver != False:
			self.VERSION = ver
	
	def __getStatusByCode(self, code):
		
		if code == b'\x00':
			return STR_OK
		if code == b'\xF0':
			return STR_SCF_ERR_INT
		if code == b'\xF1':
			return STR_SCF_ERR_READ
		if code == b'\xF4':
			return STR_SCF_ERR_ERASE
		if code == b'\xF6':
			return STR_SCF_ERR_WRITE
		if code == b'\xFA':
			return STR_SCF_ERR_CMD_LEN
		if code == b'\xFE':
			return STR_SCF_ERR_CMD_EXEC
		if code == b'\xFF':
			return STR_SCF_ERR_UNKNOWN
		
		return STR_SCF_ERR_UNK_STATUS + ' [0x{:02X}]'.format(code[0])
	
	def __getStatus(self):
		# read status byte
		res = self.__read(1)
		
		if (res != b'\x00'): # 0 = ok
			self.error('\n '+self.__getStatusByCode(res))
			self.close()
			return False
		
		return True
	
	# Main stuff
	
	def __getCmdData(self, cmd, block, count = ''):
		data = [0x00] * (5 if count != '' else 3)
		
		data[0] = cmd
		data[1] = (block >> 8) & 0xFF
		data[2] = block & 0xFF
		
		if count != '':
			end = block + count -1 
			data[3] = (end >> 8) & 0xFF
			data[4] = end & 0xFF
		
		return data
	
	def __eraseAll(self):
		
		self.__write(self.Cmd.ERASE_CHIP)
		
		if self.__getStatus() == False:
			self.error(STR_SCF_ERROR_ERASE_CHIP)
			return False
		
		return True
	
	def __eraseBlock(self, block, count = 1):
		
		cmd_data = self.__getCmdData(self.Cmd.ERASE_BLOCK, block, count)
		self.__write(cmd_data)
		
		if self.__getStatus() == False:
			self.error(STR_SCF_ERROR_ERASE_BLK%block)
			return False
		
		return True
	
	def __readAll(self):
		
		cmd_data = self.__getCmdData(self.Cmd.READ_CHIP)
		self.__write(cmd_data)
		
		data = self.__read(self.Config.TOTAL_SIZE)
		
		return data
	
	def __readBlock(self, block, count = 1):
		
		cmd_data = self.__getCmdData(self.Cmd.READ_BLOCK, block, count)
		self.__write(cmd_data)
		
		data = self.__read(self.Config.BLOCK_SIZE * count)
		
		return data
	
	def __writeBlock(self, data, block, ex = False):
		
		if len(data) != self.Config.BLOCK_SIZE:
			return False
		
		cmd_data = self.__getCmdData(self.Cmd.WRITE_BLOCK_EX if ex else self.Cmd.WRITE_BLOCK, block)
		self.__write(cmd_data)
		self.__write(data)
		
		if self.__getStatus() == False:
			self.error(STR_SCF_ERROR_WRITE_BLK%block)
			return False
		
		return True
	
	def __checkBC(self, block, count):
		
		if block >= self.Config.BLOCK_COUNT:
			block = self.Config.BLOCK_COUNT - 1
		
		if count == 0 or (block + count) > self.Config.BLOCK_COUNT:
			count = self.Config.BLOCK_COUNT - block
		
		return [block, count]
	
	# Public methods
	
	def reset(self):
		self.__clean()
		self.__write(self.Cmd.RESET)
		self.__flush()
	
	def connect(self):
		
		if not self.sp.is_open:
			self.sp.open()
		
		self.__clean()
		
		self.__write(self.Cmd.PING1)
		self.__write(self.Cmd.PING2)
		
		info = self.__read(4)
		info = b'\x00'*4 if len(info) != 4 else info
		
		ver = [info[0], info[1]]
		ram = (info[2] << 8) | info[3]
		
		if ver != self.VERSION:
			maj, min = self.VERSION
			self.error(STR_SCF_ERROR_VERSION%(maj, min))
			self.close()
		
		self.__write(self.Cmd.INIT)
		debug = self.__getStatus()
		
		return {'RAM':ram, 'VER':ver, 'DEBUG':debug}
	
	def getChipInfo(self):
		
		self.__clean()
		
		data = self.__readBlock(0)
		
		fw = Syscon.getSysconData(data, 'VERSION')
		magic = Syscon.checkSysconData(data, ['MAGIC_1', 'MAGIC_2', 'MAGIC_3'])
		debug = Syscon.getSysconData(data, 'DEBUG')
		
		info = {
			'FW'	: 'v%x.%02x'%(int.from_bytes(fw[0:1], byteorder='big'), int.from_bytes(fw[2:3], byteorder='big')),
			'Magic'	: STR_OK if magic else STR_FAIL,
			'Debug'	: '%s [0x%02X]'%(STR_ON if debug == b'\x84' or debug == b'\x85' else STR_OFF, debug[0]),
		}
		
		return info
	
	def disconnect(self):
		self.__clean()
		self.__write(self.Cmd.UNINIT)
		return self.__getStatus()
	
	def eraseChip(self, block = 0, count = 0):
		
		block, count = self.__checkBC(block, count)
		
		kb_pb = self.Config.BLOCK_SIZE // 1024
		total = count * kb_pb
		
		start = time.time()
		
		self.__clean()
		
		for b in range(block, block+count):
			"""
			res = True
			time.sleep(1)
			"""
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
		
		block, count = self.__checkBC(block, count)
		
		data = bytes()
		kb_pb = self.Config.BLOCK_SIZE // 1024
		total = count * kb_pb
		
		start = time.time()
		
		self.__clean()
		
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
	
	def writeChip(self, data, block = 0, count = 0, ex = False):
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
		
		self.__clean()
		
		for b in range(block, block + count):
			
			offset = self.Config.BLOCK_SIZE * (b - block)
			
			res = self.__writeBlock(data[offset:offset + self.Config.BLOCK_SIZE], b, ex)
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


# Legacy syscon reader by DarkNESmonk
def sysconReader(sp, file):
	
	if not sp.is_open:
		sp.open()
		if not sp.is_open:
			print(UI.error(STR_PORT_CLOSED))
			return
	
	print(STR_WAITING+'\n')
	time.sleep(2)
	
	sp.write(b'\x00')
	
	wait = True
	start_time = time.time()
	
	while wait:
		resp = sp.read(1)
		
		if resp == b'\xEE':
			print('\n'+UI.warning(STR_CHIP_NOT_RESPOND))
		
		if resp == b'\x00':
			print(UI.cyan(' [GLITCH]'))
		
		if resp == b'\x91':
			print(UI.green(' [OCD CMD] connect'))
			while True:
				resp = sp.read(1)
				if resp == b'\x94':
					print(UI.green(' [OCD CMD] exec'))
					wait = False
					sp.read(1)
					break
	
	with open(file, 'wb') as f:
		counter = 0
		print()
		while True:
			data = sp.read(Syscon.BLOCK_SIZE)
			counter += Syscon.BLOCK_SIZE
			
			f.write(data)
			
			print(UI.highlight(STR_PROGRESS_KB%(os.stat(file).st_size // 2**10, Syscon.DUMP_SIZE // 2**10))+'\r',end='')
			sys.stdout.flush()
			
			if counter >= Syscon.DUMP_SIZE:
				sp.close()
				break
	
	return time.time() - start_time