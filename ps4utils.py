import hashlib, os, math

STR_UNKNOWN = '- Unknown -'

#==========================================================
# NOR stuff
#==========================================================

NOR_DUMP_SIZE = 0x2000000
NOR_BACKUP_OFFSET = 0x3000
NOR_MBR_SIZE = 0x1000
NOR_BLOCK_SIZE = 0x200

PS4_REGIONS = {
	'00':'Japan',
	'01':'US, Canada (North America)',
	'15':'US, Canada (North America)',
	'02':'Australia / New Zealand (Oceania)',
	'03':'U.K. / Ireland',
	'04':'Europe / Middle East / Africa',
	'16':'Europe / Middle East / Africa',
	'05':'Korea (South Korea)',
	'06':'Southeast Asia / Hong Kong',
	'07':'Taiwan',
	'08':'Russia, Ukraine, India, Central Asia',
	'09':'Mainland China',
	'11':'Mexico, Central America, South America',
	'14':'Mexico, Central America, South America',
}

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

BOOT_MODES = {b'\xFE':'Development', b'\xFB':'Assist', b'\xFF':'Release'}

# {'o':<offset>, 'l':<length>, 't':<type>, 'n':<name>}
NOR_PARTITIONS = [
	{"o": 0x00000000,	"l": 0x1000,	"t":"header",		"n":"s0_head"},
	{"o": 0x00001000,	"l": 0x1000,	"t":"active_slot",	"n":"s0_act_slot"},
	{"o": 0x00002000,	"l": 0x1000,	"t":"MBR1",			"n":"s0_mbr1"},
	{"o": 0x00003000,	"l": 0x1000,	"t":"MBR2",			"n":"s0_mbr2"},
	{"o": 0x00004000,	"l": 0x60000,	"t":"emc_ipl_a",	"n":"sflash0s0x32"},
	{"o": 0x00064000,	"l": 0x60000,	"t":"emc_ipl_b",	"n":"sflash0s0x32b"},
	{"o": 0x000C4000,	"l": 0x80000,	"t":"eap_kbl",		"n":"sflash0s0x33"},
	{"o": 0x00144000,	"l": 0x80000,	"t":"wifi",			"n":"sflash0s0x38"},
	{"o": 0x001C4000,	"l": 0xC000,	"t":"nvs",			"n":"sflash0s0x34"},
	{"o": 0x001D0000,	"l": 0x30000,	"t":"blank",		"n":"sflash0s0x0"},
	{"o": 0x00200000,	"l": 0x1000,	"t":"header",		"n":"s1_head.crypt"},
	{"o": 0x00201000,	"l": 0x1000,	"t":"active_slot",	"n":"s1_act_slot.crypt"},
	{"o": 0x00202000,	"l": 0x1000,	"t":"MBR1",			"n":"s1_mbr1.crypt"},
	{"o": 0x00203000,	"l": 0x1000,	"t":"MBR2",			"n":"s1_mbr2.crypt"},
	{"o": 0x00204000,	"l": 0x3E000,	"t":"samu_ipl_a",	"n":"sflash0s1.cryptx2"},
	{"o": 0x00242000,	"l": 0x3E000,	"t":"samu_ipl_b",	"n":"sflash0s1.cryptx2b"},
	{"o": 0x00280000,	"l": 0x80000,	"t":"idata",		"n":"sflash0s1.cryptx1"},
	{"o": 0x00300000,	"l": 0x80000,	"t":"bd_hrl",		"n":"sflash0s1.cryptx39"},
	{"o": 0x00380000,	"l": 0x40000,	"t":"Virtual_TRM",	"n":"sflash0s1.cryptx6"},
	{"o": 0x003C0000,	"l": 0xCC0000,	"t":"CoreOS_A",		"n":"sflash0s1.cryptx3"},
	{"o": 0x01080000,	"l": 0xCC0000,	"t":"CoreOS_B",		"n":"sflash0s1.cryptx3b"},
	{"o": 0x01D40000,	"l": 0x2C0000,	"t":"blank",		"n":"sflash0s1.cryptx40"},
]

# 'KEY':{'o':<offset>, 'l':<length>, 't':<type>, 'n':<name>}
NOR_AREAS = {
	
	'MAC':		{'o':0x1C4021,	'l':6,			't':'b',	'n':'MAC Address'},
	'MB_SN':	{'o':0x1C8000,	'l':16,			't':'s',	'n':'Motherboard Serial'},
	'SN':		{'o':0x1C8030,	'l':17,			't':'s',	'n':'Console Serial'},
	'SKU':		{'o':0x1C8041,	'l':13,			't':'s',	'n':'SKU Version'},
	'REGION':	{'o':0x1C8047,	'l':2,			't':'s',	'n':'Region code'},
	
	'BOOT_MODE':{'o':0x1C9000,	'l':1,			't':'b',	'n':'Boot mode'},			# Development(FE), Assist(FB), Release(FF)
	'MEM_BGM':	{'o':0x1C9003,	'l':1,			't':'b',	'n':'Memory budget mode'},	# Large(FE), Normal(FF)
	'SLOW_HDD':	{'o':0x1C9005,	'l':1,			't':'b',	'n':'HDD slow mode'},		# On(FE), Off(FF)
	'SAFE_BOOT':{'o':0x1C9020,	'l':1,			't':'b',	'n':'Safe boot'},			# On(01), Off(00/FF)
	'FW_EXP':	{'o':0x1C9062,	'l':2,			't':'b',	'n':'FW in backup slot?'},
	'FW_VER':	{'o':0x1C906A,	'l':2,			't':'b',	'n':'FW in active slot'},
	'SAMUBOOT':	{'o':0x1C9323,	'l':1,			't':'b',	'n':'SAMU enc'},	
	'HDD':		{'o':0x1C9C00,	'l':60,			't':'s',	'n':'HDD'},
	'HDD_TYPE':	{'o':0x1C9C3C,	'l':4,			't':'s',	'n':'HDD type'},
	
	# Sys flags
	'SYS_FLAGS':{'o':0x1C9310,	'l':64,			't':'b',	'n':'System flags'},		# Clean FF*64
	'MEMTEST':	{'o':0x1C9310,	'l':1,			't':'b',	'n':'Memory test'},			# On(01), Off(00/FF)
	'RNG_KEY':	{'o':0x1C9312,	'l':1,			't':'b',	'n':'RNG/Keystorage test'},	# On(01), Off(00/FF)
	'UART':		{'o':0x1C931F,	'l':1,			't':'b',	'n':'UART'},				# On(01), Off(00)
	'MEMCLK':	{'o':0x1C9320,	'l':1,			't':'b',	'n':'GDDR5 Memory clock'},
	
	'BTNSWAP':	{'o':0x1CA040,	'l':1,			't':'b',	'n':'Buttons swap'},		# X(01), O(00/FF)
	'FW_C':		{'o':0x1CA5D8,	'l':1,			't':'b',	'n':'FW Counter'},
	'FW_PC':	{'o':0x1CA5D9,	'l':1,			't':'b',	'n':'FW Patch Counter'},
	'IDU':		{'o':0x1CA600,	'l':1,			't':'b',	'n':'IDU (Kiosk mode)'},	# On(01), Off(00/FF)
	'UPD_MODE':	{'o':0x1CA601,	'l':1,			't':'b',	'n':'Update mode'},			# On(10), Off(00)
	'REG_REC':	{'o':0x1CA603,	'l':1,			't':'b',	'n':'Registry recovery'},	# On(01), Off(00)
	'FW_V':		{'o':0x1CA606,	'l':2,			't':'s',	'n':'FW Version'},
	'ARCADE':	{'o':0x1CA609,	'l':1,			't':'s',	'n':'Arcade mode'},			# On(01), Off(00/FF)
	
	'MANU':		{'o':0x1CBC00,	'l':32,			't':'b',	'n':'MANU mode'},			# Enabled(0*32), Disabled(FF*32)
	
	'CORE_SWCH':{'o':0x201000,	'l':16,			't':'b',	'n':'Slot switch hack'},
}

PARTITIONS_TYPES = {
	0:"empty",
	1:"idstorage",
	2:"sam_ipl",
	3:"core_os",
	6:"bd_hrl",
	13:"emc_ipl",
	14:"eap_kbl",
	32:"emc_ipl",
	33:"eap_kbl",
	34:"nvs",
	38:"wifi",
	39:"vtrm",
	40:"empty",
	41:"C0050100",
}

# Functions ===============================================

def getConsoleRegion(file):
	code = getNorData(file,'REGION').decode('utf-8','ignore')
	desc = PS4_REGIONS[code] if code in PS4_REGIONS else STR_UNKNOWN
	return [code, desc]



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

# NOR Areas data utils

def getNorAreaName(key):
	if key in NOR_AREAS:
		return NOR_AREAS[key]['n']
	return STR_UNKNOWN



def setNorData(file, key, val):
	if not key in NOR_AREAS:
		return False
	return setData(file, NOR_AREAS[key]['o'], val)



def setNorDataB(file, key, val):
	if not key in NOR_AREAS:
		return False
	return setData(file, NOR_AREAS[key]['o'] + NOR_BACKUP_OFFSET, val)



def getNorData(file, key):
	if not key in NOR_AREAS:
		return False
	return getData(file, NOR_AREAS[key]['o'], NOR_AREAS[key]['l'])



def getNorDataB(file, key):
	if not key in NOR_AREAS:
		return False
	return getData(file, NOR_AREAS[key]['o'] + NOR_BACKUP_OFFSET, NOR_AREAS[key]['l'])



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

SC_UPD_TYPES = [0x08, 0x09, 0x0A, 0x0B]
SC_PRE1_TYPE = [0x0C, 0x0D, 0x0E, 0x0F]
SC_PRE2_TYPE = [0x20, 0x21, 0x22, 0x23]

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



def savePatchData(file, data, patch = False):
	with open(file, 'wb') as f:
		f.write(data)
	
	if not patch:
		return
	
	with open(file, 'r+b') as f:
		for i in range(len(patch)):
			f.seek(patch[i]['o'],0)
			f.write(patch[i]['d'])


def entropy(file):
	with open(file, "rb") as f:
		
		vals = {byte: 0 for byte in range(2**8)}
		
		for byte in f.read():
			vals[byte] += 1
		
		probs = [val / f.tell() for val in vals.values()]
		entropy = -sum(prob * math.log2(prob) for prob in probs if prob > 0)
		
		return {'00':probs[0],'ff':probs[0xff],'ent':entropy}
