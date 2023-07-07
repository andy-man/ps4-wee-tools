import hashlib, os, math

#==========================================================
# NOR stuff
#==========================================================

NOR_DUMP_SIZE = 0x2000000
NOR_BACKUP_OFFSET = 0x3000

SWITCH_TYPES = [
	'Off',
	'Fat 10xx/11xx',
	'Fat/Slim/PRO 12xx/2xxx/7xxx',
	'General',
]

SWITCH_BLOBS = [
	{'t':1, 'v':[0xFF]*8 + [0x00]*8},
	{'t':1, 'v':[0x00]*8 + [0xFF]*8},
	{'t':2, 'v':[0xFF]*16},
	{'t':2, 'v':[0x00]*16},
	{'t':3, 'v':[0xFF]*4 + [0x00]*12},
	{'t':3, 'v':[0x00]*4 + [0xFF]*12},
	{'t':3, 'v':[0xFF]*12 + [0x00]*4},
	{'t':3, 'v':[0x00]*12 + [0xFF]*4},
]

# 'KEY':{'o':<offset>, 'l':<length>, 't':<type>, 'n':<name>}
NOR_AREAS = {
	'MAC':		{'o':0x1C4021,	'l':6,	't':'b',	'n':'MAC Address'},
	'MB_SN':	{'o':0x1C8000,	'l':16,	't':'s',	'n':'Motherboard Serial'},
	'SN':		{'o':0x1C8030,	'l':16,	't':'s',	'n':'Console Serial'},
	'SKU':		{'o':0x1C8040,	'l':16,	't':'s',	'n':'SKU Version'},
	'HDD':		{'o':0x1C9C00,	'l':60,	't':'s',	'n':'HDD'},
	'HDD_TYPE':	{'o':0x1C9C3C,	'l':4,	't':'s',	'n':'HDD type'},
	'FW_C':		{'o':0x1CA5D8,	'l':1,	't':'b',	'n':'FW Counter'},
	'FWP_C':	{'o':0x1CA5D9,	'l':1,	't':'b',	'n':'FW Patch Counter'},
	'FWV':		{'o':0x1CA604,	'l':4,	't':'s',	'n':'FW Version'},
	'FW_SLOT1':	{'o':0x1C906A,	'l':2,	't':'b',	'n':'FW in slot 1'},
	'FW_SLOT2':	{'o':0x1CC06A,	'l':2,	't':'b',	'n':'FW in slot 2'},
	'SAMUBOOT':	{'o':0x1C9323,	'l':1,	't':'b',	'n':'SAMU enc'},
	'MEMCLK':	{'o':0x1C9320,	'l':1,	't':'b',	'n':'GDDR5 Memory clock'},
	'CORE_SWCH':{'o':0x201000,	'l':16,	't':'b',	'n':'Slot switch hack'},
	'SAMU_SL1':	{'o':0x204000,	'l':16,	't':'b',	'n':'slot 1 loader'},
	'SAMU_SL2':	{'o':0x242000,	'l':16,	't':'b',	'n':'slot 2 loader'},
	'UART':		{'o':0x1C931F,	'l':1,	't':'b',	'n':'UART flag'},
	'SYS_FLAGS':{'o':0x1C9310,	'l':64,	't':'b',	'n':'System flags'},
	'MEMTEST1':	{'o':0x1C9310,	'l':1,	't':'b',	'n':'Memtest in slot 1'},
	'MEMTEST2':	{'o':0x1C9312,	'l':1,	't':'b',	'n':'Memtest in slot 2'},
}

# Functions ===============================================

def getMemClock(file):
	raw1 = getNorData(file,'MEMCLK')[0]
	raw2 = getNorDataB(file,'MEMCLK')[0]
	return [raw1, rawToClock(raw1), raw2, rawToClock(raw2)]



def getSlotSwitchInfo(file):
	pattern = list(getNorData(file,'CORE_SWCH'))
	for i in range(0,len(SWITCH_BLOBS)):
		if SWITCH_BLOBS[i]['v'] == pattern:
			return SWITCH_TYPES[SWITCH_BLOBS[i]['t']]+' [#'+str(i+1)+']'
	return SWITCH_TYPES[0]+' '+getHex(bytes(pattern),'')

# NOR data utils

def setNorData(file, name, val):
	if not name in NOR_AREAS:
		return False
	return setData(file, NOR_AREAS[name]['o'], val)



def setNorDataB(file, name, val):
	if not name in NOR_AREAS:
		return False
	return setData(file, NOR_AREAS[name]['o'] + NOR_BACKUP_OFFSET, val)



def getNorData(file, name):
	if not name in NOR_AREAS:
		return False
	return getData(file, NOR_AREAS[name]['o'], NOR_AREAS[name]['l'])



def getNorDataB(file, name):
	if not name in NOR_AREAS:
		return False
	return getData(file, NOR_AREAS[name]['o'] + NOR_BACKUP_OFFSET, NOR_AREAS[name]['l'])



#==========================================================
# Syscon stuff
#==========================================================

SYSCON_DUMP_SIZE = 0x80000
SYSCON_BLOCK_SIZE = 0x400

SC_AREAS = {
	'MAGIC_1':	{'o':0x00000,	'l':2,		't':'b',	'n':b'\x80\x01'},
	'MAGIC_2':	{'o':0x000C4,	'l':10,		't':'s',	'n':b':Not:Used:'},
	'MAGIC_3':	{'o':0x00132,	'l':14,		't':'s',	'n':b' Sony Computer'},
	'DEBUG':	{'o':0x000C3,	'l':1,		't':'b',	'n':'Debug flag 0x04=off 0x85/0x84=on'},
	'SNVS':		{'o':0x60000,	'l':0xE000,	't':'b',	'n':'SNVS storage'},
	'NVS':		{'o':0x6E000,	'l':0x2000,	't':'b',	'n':'NVS storage'},
}

# Functions ===============================================

def setSysconData(file, name, val):
	if not name in SC_AREAS:
		return False
	return setData(file, SC_AREAS[name]['o'], val)



def getSysconData(file, name):
	if not name in SC_AREAS:
		return False
	return getData(file, SC_AREAS[name]['o'], SC_AREAS[name]['l'])



def checkSysconData(file, name):
	if not name in SC_AREAS:
		return False
	if getData(file, SC_AREAS[name]['o'], SC_AREAS[name]['l']) == SC_AREAS[name]['n']:
		return True
	else:
		return False



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
			self.entry = b'\x00' * self.getEntryHeadSize()
		else:
			self.entry = buf
	
	def getHeader(self):
		return self.entry[:self.getHeaderSize()];
	
	def getData(self):
		return self.entry[self.getHeaderSize():self.getHeaderSize()+self.getDataSize()];
	
	def getCounter(self):
		return int.from_bytes(self.entry[4:4+3],"little")
	
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
		offset = self.getDataBlockOffset(self.active_entry.getLink())
		if real:
			return self.cfg.getOffset() + self.cfg.getHeaderSize() + offset + self.cfg.getDataFlatLength()
		else:
			return offset
	
	def getDataBlockOffset(self, index = 0):
		return self.cfg.getDataLength() * index
	
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

#==========================================================
# Common
#==========================================================

def getData(file, off, len):
	#file must be in rb/r+b mode
	file.seek(off);
	return file.read(len)



def setData(file, off, val):
	#file must be in r+b mode
	file.seek(off);
	return file.write(val)



def checkFileSize(file, size):
	if not file or not os.path.isfile(file):
		print((MSG_FILE_NOT_EXISTS).format(file))
		input(MSG_BACK)
		return False
	
	if os.stat(file).st_size != size:
		print((MSG_INCORRECT_SIZE).format(file))
		input(MSG_BACK)
		return False
	
	return True



def getFileMD5(file):
    f = open(file, 'rb')
    f.seek(0)
    with f:
        res = f.read()
        return hashlib.md5(res).hexdigest()



def getHex(buf,sep=' '):
	str = ""
	for c in buf:
		str += format(c, '02X')+sep
	return str[:len(str)-len(sep)]



def swapBytes(arr):
	res = [0]*len(arr)
	for i in range(0,len(arr),2):
		res[i] = arr[i+1]
		res[i+1] = arr[i]
	return bytes(res)



def rawToClock(raw):
	if (0x10 <= raw <= 0x50):
		return (raw - 0x10) * 25 + 400
	return 0



def clockToRaw(frq):
	return (frq - 400) // 25 + 0x10



def isSysconPatchable(records):
	type = NvsEntry(records[-1]).getIndex()
	if type in [0x08, 0x09, 0x0A, 0x0B]:
		return 1
	if type in [0x0C, 0x0D, 0x0E, 0x0F]:
		return 0
	if type in [0x20, 0x21, 0x22, 0x23]:
		return 0
	return 2


def entropy(file):
	with open(file, "rb") as f:
		
		vals = {byte: 0 for byte in range(2**8)}
		
		for byte in f.read():
			vals[byte] += 1
		
		probs = [val / f.tell() for val in vals.values()]
		entropy = -sum(prob * math.log2(prob) for prob in probs if prob > 0)
		
		return {'00':probs[0],'ff':probs[0xff],'ent':entropy}
