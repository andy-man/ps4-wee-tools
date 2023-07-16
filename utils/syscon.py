#==========================================================
# Syscon utils
# part of ps4 wee tools project
#==========================================================
from utils.utils import *

SYSCON_DUMP_SIZE = 0x80000
SYSCON_BLOCK_SIZE = 0x400

SC_AREAS = {
	'MAGIC_1':	{'o':0x00000,	'l':2,		't':'b',	'n':b'\x80\x01'},
	'MAGIC_2':	{'o':0x000C4,	'l':10,		't':'s',	'n':b':Not:Used:'},
	'MAGIC_3':	{'o':0x00132,	'l':14,		't':'s',	'n':b' Sony Computer'},
	'DEBUG':	{'o':0x000C3,	'l':1,		't':'b',	'n':'Debug flag 0x04=off 0x85/0x84=on'},
	'VERSION':	{'o':0x00100,	'l':4,		't':'b',	'n':'FW version'},
	'SNVS':		{'o':0x60000,	'l':0xE000,	't':'b',	'n':'SNVS storage'},
	'NVS':		{'o':0x6E000,	'l':0x2000,	't':'b',	'n':'NVS storage'},
}

# Functions ===============================================

def setSysconData(file, key, val):
	if not key in SC_AREAS:
		return False
	return setData(file, SC_AREAS[key]['o'], val)



def getSysconData(file, key):
	if not key in SC_AREAS:
		return False
	return getData(file, SC_AREAS[key]['o'], SC_AREAS[key]['l'])



def checkSysconData(file, key):
	if not key in SC_AREAS:
		return False
	if getData(file, SC_AREAS[key]['o'], SC_AREAS[key]['l']) == SC_AREAS[key]['n']:
		return True
	else:
		return False



def getLast_080B_Index(entries):
	length = len(entries)
	if length < 4:
		return -1
	for i in range(length):
		if entries[length-4-i][1] != SC_UPD_TYPES[0]:
			continue
		if entries[length-3-i][1] != SC_UPD_TYPES[1]:
			continue
		if entries[length-2-i][1] != SC_UPD_TYPES[2]:
			continue
		if entries[length-1-i][1] != SC_UPD_TYPES[3]:
			continue
		return length-i-4
	return -1



def isSysconPatchable(records):
	type = NvsEntry(records[-1]).getIndex()
	if type in SC_UPD_TYPES:
		return 1
	if type in SC_PRE1_TYPE:
		return 0
	if type in SC_PRE2_TYPE:
		return 0
	return 2

# NVS Parser ==============================================

class NvsConfig:
	
	cfg = {}
	
	def __init__(self, cfg):
		self.cfg = cfg
	
	def getOffset(self):
		return self.cfg['offset']
	
	def getHeaderLength(self):
		return self.cfg['header']['length']
	
	def getHeaderCount(self):
		return self.cfg['header']['count']
	
	def getHeaderSize(self):
		return self.getHeaderLength() * self.getHeaderCount()
	
	def getDataFlatLength(self):
		return self.cfg['data']['flat']
	
	def getDataRecordsLength(self):
		return self.cfg['data']['records']
	
	def getDataCount(self):
		return self.cfg['data']['count']
	
	def getDataLength(self):
		return self.getDataFlatLength() + self.getDataRecordsLength()
	
	def getDataSize(self):
		return self.getDataLength() * self.getDataCount()



class NvsEntry:
	
	entry = b''
	
	def __init__(self, buf):
		if len(buf) < self.getEntryHeadSize() or self.checkMagic(buf) == 0:
			self.entry = [0x00] * self.getEntryHeadSize()
		else:
			self.entry = bytearray(buf)
	
	def getHeader(self):
		return self.entry[:self.getHeaderSize()];
	
	def getData(self):
		return self.entry[self.getHeaderSize():self.getHeaderSize()+self.getDataSize()];
	
	def getCounter(self):
		return int.from_bytes(self.entry[4:4+3],"little")
	
	def setCounter(self,val):
		self.entry[4+0] = val & 0xFF
		self.entry[4+1] = val >> 8 & 0xFF
		self.entry[4+2] = val >> 16 & 0xFF
	
	def getIndex(self):
		return int.from_bytes(self.entry[1:1+2],"little")
	
	def getLink(self):
		return int.from_bytes(self.entry[3:3+1],"little")
	
	def hasMagic(self):
		return self.checkMagic(self.entry)
	
	@staticmethod
	def checkMagic(e):
		m1 = 0b01 if e[0] == 0xA5 else 0
		m2 = 0b10 if e[7] == 0xC3 else 0
		return m1 | m2
	
	@staticmethod
	def getEntryHeadSize():
		return 8
	
	@staticmethod
	def getEntryDataSize():
		return 8
	
	@staticmethod
	def getEntrySize():
		return 16



class NVStorage:
	
	cfg = NvsConfig({})
	
	header = b''
	data = b''	
	
	active_volume = 0
	active_entry = NvsEntry('')
	
	def __init__(self, config, buffer):
		self.cfg = config
		if buffer and len(buffer):
			self.load(buffer)
	
	def load(self, buf):
		self.header = buf[:self.cfg.getHeaderSize()]
		self.data = buf[len(self.header):]
		self.findActive()
	
	def findActive(self):
		
		for volume in range(0, self.cfg.getHeaderCount()):
			counter = self.getVolumeCounter(volume)
			entries = self.getVolumeEntries(volume)
			if len(entries) and counter > 0:
				self.active_volume = volume
				self.active_entry = NvsEntry(entries[len(entries)-1])
		
		return self.active_volume
	
	def getVolumeEntries(self, volume = 0):
		
		length = self.cfg.getHeaderLength()
		step = NvsEntry.getEntryHeadSize()
		offset = length * volume;
		entries = list()
		
		for i in range(0, offset+length, step):
			entry = self.header[i:i+step]
			if NvsEntry.checkMagic(entry) != 0:
				entries.append(entry)
		
		return entries
	
	def getLastDataEntries(self):
		return self.getDataBlockEntries(self.active_entry.getLink())
	
	def getLastDataBlockOffset(self, real = False):
		return self.getDataBlockOffset(self.active_entry.getLink(), real)
	
	def getDataBlockOffset(self, index = 0, real = False):
		offset = self.cfg.getDataLength() * index
		if real:
			return self.cfg.getOffset() + self.cfg.getHeaderSize() + offset + self.cfg.getDataFlatLength()
		else:
			return offset
	
	def getDataBlock(self, index = 0):
		offset = self.getDataBlockOffset(index)
		return self.data[ offset : offset + self.cfg.getDataLength()]
	
	def getDataBlockFlat(self, index = 0):
		block = self.getDataBlock(index)
		return block[:self.cfg.getDataFlatLength()]
	
	def getDataBlockEntries(self, index = 0):
		
		data = self.getDataBlock(index)[self.cfg.getDataFlatLength():]
		step = NvsEntry.getEntrySize()
		entries = list()
		
		for i in range(0, len(data), step):
			entry = data[i:i+step]
			if NvsEntry.checkMagic(entry) != 0:
				entries.append(entry)
		
		return entries
	
	def getVolumeEntry(self, volume = 0, index = 0):
		offset = (index) * NvsEntry.getEntryHeadSize() + self.cfg.getHeaderLength() * volume;
		return self.header[offset:offset + NvsEntry.getEntryHeadSize()]
	
	def getVolumeCounter(self, volume = 0):
		entry = NvsEntry(self.getVolumeEntry(volume,0))
		return entry.getCounter()



SNVS_CONFIG = NvsConfig({ 
	"offset":	SC_AREAS['SNVS']['o'],
	"header":	{ "length":SYSCON_BLOCK_SIZE, "count":2 }, 
	"data":		{ "flat":SYSCON_BLOCK_SIZE, "records":SYSCON_BLOCK_SIZE * 5, "count":8 },
})

NVS_CONFIG = NvsConfig({ 
	"offset":	SC_AREAS['NVS']['o'],
	"header":	{ "length":SYSCON_BLOCK_SIZE, "count":2 },
	"data":		{ "flat":SYSCON_BLOCK_SIZE, "records":SYSCON_BLOCK_SIZE * 5, "count":8 },
})

SC_UPD_TYPES = [0x08, 0x09, 0x0A, 0x0B]
SC_PRE1_TYPE = [0x0C, 0x0D, 0x0E, 0x0F]
SC_PRE2_TYPE = [0x20, 0x21, 0x22, 0x23]