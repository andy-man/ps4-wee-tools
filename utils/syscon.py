#==========================================================
# Syscon utils
# part of ps4 wee tools project
#==========================================================
from utils.utils import *
import lang._i18n_ as Lang



BLOCK_SIZE	= 0x400
BLOCK_COUNT	= 512
DUMP_SIZE	= BLOCK_SIZE * BLOCK_COUNT

MD5_SC_FW = {
	'125cd5cc2d854e5f2812f060a7031044':'1.00_0',
	'baea46d4d5bf6d9b00b51bda40db0f48':'1.0b_0',
	'6741017a1499384dd7b07dc6def28d1e':'2.06_1',
	'fa4dddb3f17315ecc028bf725b7702b1':'2.06_2',
	'1c70248c249f0ac4f0c5555499afa6ef':'2.13_1',
	'45ebe778279ca58b6bf200ff1bd2cb9e':'2.13_2',
	'581d42d6a6c83992521420a23f02427c':'2.13_3',
	'39a1bdd270d0dc2bdce8d81e7525af41':'2.23_1',
	'a7d36425e5881770b2e9c4f925ced39f':'2.23_2',
	'c42c250bbb7b30acd2f3960cfad9c8e3':'2.23_3',
	'f7e0a6157fa9c04944b927051b5d4196':'2.23_4',
	'263bd07f5b80f64aca8a107fee27ee08':'2.26_0',
}

SC_AREAS = {
	'MAGIC_1':	{'o':0x00000,	'l':2,		't':'b',	'n':b'\x80\x01'},
	'MAGIC_2':	{'o':0x000C4,	'l':10,		't':'s',	'n':b':Not:Used:'},
	'MAGIC_3':	{'o':0x00132,	'l':14,		't':'s',	'n':b' Sony Computer'},
	'FW':		{'o':0x00000,	'l':0x60000,'t':'b',	'n':'Syscon FW'},
	'DEBUG':	{'o':0x000C3,	'l':1,		't':'b',	'n':'Debug flag 0x04=off 0x85/0x84=on'},
	'VERSION':	{'o':0x00100,	'l':4,		't':'b',	'n':'FW version'},
	'SNVS':		{'o':0x60000,	'l':0xE000,	't':'b',	'n':'SNVS storage'},
	'NVS':		{'o':0x6E000,	'l':0x2000,	't':'b',	'n':'NVS storage'},
}

SC_E_TYPE = {
	'MODE0'		: 0x00,
	'MODE1'		: 0x01,
	'MODE2'		: 0x02,
	'MODE3'		: 0x03,
	'BOOT0'		: 0x04,
	'BOOT1'		: 0x05,
	'BOOT2'		: 0x06,
	'BOOT3'		: 0x07,
	'FW_A'		: 0x08,
	'FW_B'		: 0x09,
	'LIC1'		: 0x0A,
	'LIC2'		: 0x0B,
	'PRE0C'		: 0x0C,
	'PRE0D'		: 0x0D,
	'PRE0E'		: 0x0E,
	'PRE0F'		: 0x0F,
	'PRE20'		: 0x20,
	'PRE21'		: 0x21,
	'PRE22'		: 0x22,
	'PRE23'		: 0x23,
	'SYS24'		: 0x24,
	'SYS25'		: 0x25,
	'SYS26'		: 0x26,
	'SYS27'		: 0x27,
	'SYS28'		: 0x28,
	'SYS29'		: 0x29,
	'SYS2A'		: 0x2A,
	'SYS2B'		: 0x2B,
}

SC_TYPES_BOOT	= [SC_E_TYPE['BOOT0'], SC_E_TYPE['BOOT1'], SC_E_TYPE['BOOT2'], SC_E_TYPE['BOOT3']]
SC_TYPES_MODES	= [SC_E_TYPE['MODE0'], SC_E_TYPE['MODE1'], SC_E_TYPE['MODE2'], SC_E_TYPE['MODE3']]
SC_TYPES_UPD	= [SC_E_TYPE['FW_A'], SC_E_TYPE['FW_B'], SC_E_TYPE['LIC1'], SC_E_TYPE['LIC2']]
SC_TYPES_PRE0	= [SC_E_TYPE['PRE0C'], SC_E_TYPE['PRE0D'], SC_E_TYPE['PRE0E'], SC_E_TYPE['PRE0F']]
SC_TYPES_PRE2	= [SC_E_TYPE['PRE20'], SC_E_TYPE['PRE21'], SC_E_TYPE['PRE22'], SC_E_TYPE['PRE23']]
SC_TYPES_SYS0	= [SC_E_TYPE['SYS24'], SC_E_TYPE['SYS25'], SC_E_TYPE['SYS26'], SC_E_TYPE['SYS27']]
SC_TYPES_SYS2	= [SC_E_TYPE['SYS28'], SC_E_TYPE['SYS29'], SC_E_TYPE['SYS2A'], SC_E_TYPE['SYS2B']]

# Functions ===============================================

def setSysconData(file, key, val):
	if not key in SC_AREAS:
		return False
	return setData(file, SC_AREAS[key]['o'], val)



def getSysconData(fod, key):
	if not key in SC_AREAS:
		return False
	if isinstance(fod, bytes):
		return getMemData(fod, SC_AREAS[key]['o'], SC_AREAS[key]['l'])
	else:
		return getData(fod, SC_AREAS[key]['o'], SC_AREAS[key]['l'])



def checkSysconData(fod, keys):
	for key in keys:
		if getSysconData(fod, key) != SC_AREAS[key]['n']:
			return False
	return True



def checkSysconFW(file):
	fw = bytearray(getSysconData(file, 'FW'))
	# All hashes was calculated for non-debug syscon (0x04)
	fw[SC_AREAS['DEBUG']['o']] = 0x04
	md5 = hashlib.md5(fw).hexdigest()
	
	if md5 in MD5_SC_FW:
		return {'md5':md5, 'fw':MD5_SC_FW[md5]}
	else:
		return {'md5':md5, 'fw':False}



def getEntriesByType(type, entries):
	indexes = []
	for i in range(len(entries)-len(type)+1):
		found = True
		for k in range(len(type)):
			if entries[i+k][1] != type[k]:
				found = False
				break
		if found:
			indexes.append(i)
	return indexes



def getRecordPos(index, nvs):
	data = {}
	if index < 0:
		return data
	
	block_order = nvs.getDataBlocksOrder()
	records_per_block = nvs.cfg.getDataRecordsCount()
	
	data['block'] = block_order[len(block_order)-1 - index // records_per_block]
	data['num'] = index % records_per_block
	data['offset'] = nvs.getDataBlockOffset(data['block'], True) + data['num'] * NvsEntry.getEntrySize()
	
	return data



def isSysconPatchable(records):
	
	inds = getEntriesByType(SC_TYPES_UPD, records)
	
	if len(inds) == 0:
		return 0
	
	last_fw_ind = inds[-1]
	
	type = NvsEntry(records[last_fw_ind - len(SC_TYPES_UPD)]).getIndex()
	if not type in SC_TYPES_UPD:
		return 2
	
	if last_fw_ind == len(records) - len(SC_TYPES_UPD):
		return 1
	
	for i in range(last_fw_ind, len(records)):
		type = NvsEntry(records[i]).getIndex()
		if type in SC_TYPES_PRE0 or type in SC_TYPES_PRE2:
			return 0
	
	return 3

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
	
	def getDataRecordsCount(self):
		return self.getDataRecordsLength() // NvsEntry.getEntrySize()



class NvsEntry:
	
	entry = b''
	
	def __init__(self, buf):
		if len(buf) < self.getEntryHeadSize() or self.checkMagic(buf) == 0:
			self.entry = [0x00] * self.getEntryHeadSize()
		else:
			self.entry = bytearray(buf)
	
	def getHeader(self):
		return self.entry[:self.getEntryHeadSize()];
	
	def getData(self):
		return self.entry[self.getEntryHeadSize():self.getEntryHeadSize()+self.getEntryDataSize()];
	
	def getEntry(self):
		return self.entry
	
	def getCounter(self):
		return int.from_bytes(self.entry[4:4+3],"little")
	
	def setCounter(self,val):
		self.entry[4+0] = val & 0xFF
		self.entry[4+1] = val >> 8 & 0xFF
		self.entry[4+2] = val >> 16 & 0xFF
	
	def getIndex(self):
		return int.from_bytes(self.entry[1:1+2],"little")
	
	def setIndex(self, val):
		self.entry[1+0] = val & 0xFF
		self.entry[1+1] = val >> 8 & 0xFF
	
	def getLink(self):
		return int.from_bytes(self.entry[3:3+1],"little")
	
	def setLink(self, val):
		self.entry[3] = val & 0xFF
	
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
	active_entry_num = 1
	
	def __init__(self, config, buffer):
		self.cfg = config
		if buffer and len(buffer):
			self.load(buffer)
	
	def load(self, buf):
		self.header = buf[:self.cfg.getHeaderSize()]
		self.data = buf[len(self.header):]
		self.findActive()
	
	def getHeader(self):
		return self.header
	
	def getData(self):
		return self.data
	
	def getBytes(self):
		return self.header + self.data
	
	def findActive(self):
		
		for volume in range(0, self.cfg.getHeaderCount()):
			counter = self.getVolumeCounter(volume)
			entries = self.getVolumeEntries(volume)
			if len(entries) and counter > 0:
				self.active_volume = volume
				self.active_entry = NvsEntry(entries[len(entries)-1])
				self.active_entry_num = len(entries)-1
		
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
	
	def getOWC(self):
		# overwrite count
		c = len(self.getVolumeEntries()) - 1
		return 0 if c <= self.cfg.getDataCount() else c // self.cfg.getDataCount()
	
	def getLastDataEntries(self):
		return self.getDataBlockEntries(self.active_entry.getLink())
	
	def getLastFlatEntries(self):
		return self.getFlatDataEntries(self.active_entry.getLink())
	
	def getLastFlatDataOffset(self, real = False):
		return self.getFlatDataOffset(self.active_entry.getLink(), real)
	
	def getLastDataBlockOffset(self, real = False):
		return self.getDataBlockOffset(self.active_entry.getLink(), real)
	
	def getFlatDataOffset(self, index = 0, real = False):
		offset = self.cfg.getDataLength() * index
		return self.cfg.getOffset() + self.cfg.getHeaderSize() + offset if real else offset
	
	def getDataBlockOffset(self, index = 0, real = False):
		offset = self.cfg.getDataLength() * index
		return self.cfg.getOffset() + self.cfg.getHeaderSize() + offset + self.cfg.getDataFlatLength() if real else offset
	
	def getDataBlock(self, index = 0):
		offset = self.getDataBlockOffset(index)
		return self.data[ offset : offset + self.cfg.getDataLength()]
	
	def getDataBlockFlat(self, index = 0):
		block = self.getDataBlock(index)
		return block[:self.cfg.getDataFlatLength()]
	
	def getDataBlockRecords(self, index = 0):
		block = self.getDataBlock(index)
		return block[self.cfg.getDataFlatLength():]
	
	def getFlatDataEntries(self, index = 0):
		
		flatdata = self.getDataBlockFlat(index)
		entry_size = NvsEntry.getEntrySize()
		entries = []
		
		for i in range(0, len(flatdata), entry_size):
			entry = flatdata[i:i+entry_size]
			entries.append(entry)
		
		empty = 0
		for i in range(len(entries)-1, -1, -1):
			if entries[i] != b'\xFF'*entry_size:
				entries = entries[0:i+1]
				break
			empty += 1
		
		if empty == len(entries): entries = []
		
		return entries
	
	def getDataBlockEntries(self, index = 0):
		
		data = self.getDataBlockRecords(index)
		entry_size = NvsEntry.getEntrySize()
		entries = []
		
		for i in range(0, len(data), entry_size):
			entry = data[i:i+entry_size]
			if NvsEntry.checkMagic(entry) != 0:
				entries.append(entry)
		
		return entries
	
	def getVolumeEntry(self, volume = 0, index = 0):
		offset = (index) * NvsEntry.getEntryHeadSize() + self.cfg.getHeaderLength() * volume;
		return self.header[offset:offset + NvsEntry.getEntryHeadSize()]
	
	def getLastVolumeEntryOffset(self, real = False):
		return self.getVolumeEntryOffset(self.active_entry_num, real)
	
	def getVolumeEntryOffset(self, index, real = False):
		offset = NvsEntry.getEntryHeadSize() * index
		return self.cfg.getOffset() + offset if real else offset
	
	def getVolumeCounter(self, volume = 0):
		entry = NvsEntry(self.getVolumeEntry(volume,0))
		return entry.getCounter()
	
	def getDataBlocksOrder(self):
		v_entries = self.getVolumeEntries()
		max = len(v_entries) - self.cfg.getDataCount()
		return [NvsEntry(v_entries[i-1]).getLink() for i in range(len(v_entries), max if max > 0 else 1, -1)]
	
	def getAllDataEntries(self):
		entries = []
		for n in self.getDataBlocksOrder():
			entries = self.getDataBlockEntries(n) + entries
		return entries
	
	def getAllFlatData(self):
		flatdata = []
		for n in self.getDataBlocksOrder():
			flatdata = [self.getDataBlockFlat(n)] + flatdata
		return flatdata
	
	def getRebuilded(self, entries = False, flatdata = False):
		# get all enties and flatdata
		entries = self.getAllDataEntries() if entries == False else entries
		flatdata = self.getAllFlatData() if flatdata == False else flatdata
		flatlength = self.cfg.getDataFlatLength()
		
		# fix counters
		for i in range(len(entries)):
			entry = NvsEntry(entries[i])
			entry.setCounter(i)
			entries[i] = entry.getEntry()
		
		# create new
		header = b'\xA5\x00\x00\xFF\xFF\xFF\xFF\xC3'
		data = b''
		for i in range(self.cfg.getDataCount()):
			start = i * self.cfg.getDataRecordsCount()
			if start >= len(entries):
				break
			data += b'\xFF'*flatlength if i >= len(flatdata) or len(flatdata[i]) < flatlength else flatdata[i]
			end = start + self.cfg.getDataRecordsCount()
			for n in range(start, end if end <= len(entries) else len(entries)):
				data += entries[n]
			first = NvsEntry(entries[start])
			first.setIndex(i)
			first.setLink(i)
			header += first.getHeader()
		
		# adjust padding
		hsize = self.cfg.getHeaderSize()
		if len(header) < hsize:
			header += b'\xFF'*(hsize - len(header))
		
		dsize = self.cfg.getDataSize()
		if len(data) < dsize:
			data += b'\xFF'*(dsize - len(data))
		
		return header + data



SNVS_CONFIG = NvsConfig({ 
	"offset":	SC_AREAS['SNVS']['o'],
	"header":	{ "length":BLOCK_SIZE, "count":2 }, 
	"data":		{ "flat":BLOCK_SIZE, "records":BLOCK_SIZE * 5, "count":8 },
})

NVS_CONFIG = NvsConfig({ 
	"offset":	SC_AREAS['NVS']['o'],
	"header":	{ "length":BLOCK_SIZE, "count":2 },
	"data":		{ "flat":BLOCK_SIZE, "records":BLOCK_SIZE * 2, "count":2 },
})



def getCanonicalName(fpath):
	with open(fpath, 'rb') as f:
		
		fw = getSysconData(f, 'VERSION')
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
		records = SNVS.getAllDataEntries()
		order = ''.join(str(x) for x in SNVS.getDataBlocksOrder())
		status = Lang.MENU_SC_STATUSES[isSysconPatchable(records)].replace(' ','_').lower()
	
	return '_'.join(['syscon', '%X.%02X'%(fw[0],fw[2]), '%d'%len(records), '['+order+']', status])