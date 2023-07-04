import hashlib, os

# Constants ===============================================

NOR_DUMP_SIZE = 0x2000000
NOR_BACKUP_OFFSET = 0x3000

SYSCON_DUMP_SIZE = 0x80000
SYSCON_NVS_OFFSET = 0x60000
SYSCON_BLOCK_SIZE = 0x400

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

# STRUCTIRES ==============================================

# 'KEY':{'o':<offset>, 'l':<length>, 't':<type>, 'n':<name>}
NOR_AREAS = {
	'MAC':		{'o':0x1C4021,	'l':6,	't':'b',	'n':'MAC Address'},
	'MB_SN':	{'o':0x1C8000,	'l':14,	't':'s',	'n':'Motherboard Serial'},
	'SN':		{'o':0x1C8030,	'l':17,	't':'s',	'n':'Console Serial'},
	'SKU':		{'o':0x1C8041,	'l':13,	't':'s',	'n':'SKU Version'},
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
	'UART':		{'o':0x1C931F,	'l':1,	't':'b',	'n':'UART flag'},
	'SYS_FLAGS':{'o':0x1C9310,	'l':64,	't':'b',	'n':'System flags'},
	'MEMTEST1':	{'o':0x1C9310,	'l':1,	't':'b',	'n':'Memtest in slot 1'},
	'MEMTEST2':	{'o':0x1C9312,	'l':1,	't':'b',	'n':'Memtest in slot 2'},
}

SC_AREAS = {
	'MAGIC_1':	{'o':0x00000,	'l':2,	't':'b',	'n':b'\x80\x01'},
	'MAGIC_2':	{'o':0x000C4,	'l':10,	't':'s',	'n':b':Not:Used:'},
	'MAGIC_3':	{'o':0x00132,	'l':14,	't':'s',	'n':b' Sony Computer'},
	'DEBUG':	{'o':0x000C3,	'l':1,	't':'b',	'n':'Debug flag 0x04=off 0x85/0x84=on'},
}

# Functions ==============================================

# syscon data

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

# NOR data

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

# Common

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

def getMemClock(file):
	raw1 = getNorData(file,'MEMCLK')[0]
	raw2 = getNorDataB(file,'MEMCLK')[0]
	return [raw1, rawToClock(raw1), raw2, rawToClock(raw2)]

def rawToClock(raw):
	if (0x10 <= raw <= 0x50):
		return (raw - 0x10) * 25 + 400
	return 0

def clockToRaw(frq):
	return (frq - 400) // 25 + 0x10

def getSlotSwitchInfo(file):
	pattern = list(getNorData(file,'CORE_SWCH'))
	for i in range(0,len(SWITCH_BLOBS)):
		if SWITCH_BLOBS[i]['v'] == pattern:
			return SWITCH_TYPES[SWITCH_BLOBS[i]['t']]+' [#'+str(i+1)+']'
	return SWITCH_TYPES[0]+' '+getHex(bytes(pattern),'')

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