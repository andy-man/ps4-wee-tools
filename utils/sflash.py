#==========================================================
# NOR utils
# part of ps4 wee tools project
#==========================================================
import hashlib, os, math, sys, ctypes
from lang._i18n_ import *
import data.data as Data
import lang._i18n_ as Lang
import utils.utils as Utils



DUMP_SIZE = 0x2000000
BACKUP_OFFSET = 0x3000
MBR_SIZE = 0x1000
BLOCK_SIZE = 0x200

PS_REGIONS = {
	'jp':{'n':'Japan',									'c':['00']},
	'us':{'n':'US, Canada (North America)',				'c':['01','15']},
	'au':{'n':'Australia / New Zealand (Oceania)',		'c':['02']},
	'uk':{'n':'U.K. / Ireland',							'c':['03']},
	'eu':{'n':'Europe / Middle East / Africa',			'c':['16','04']},
	'kr':{'n':'Korea (South Korea)',					'c':['05']},
	'sa':{'n':'Southeast Asia / Hong Kong',				'c':['06']},
	'tw':{'n':'Taiwan',									'c':['07']},
	'ru':{'n':'Russia, Ukraine, India, Central Asia',	'c':['08']},
	'cn':{'n':'Mainland China',							'c':['09']},
	'mx':{'n':'Mexico, Central America, South America',	'c':['11','14']},
	'kr':{'n':'Singapore, Korea, Asia',					'c':['18']},
}

SWITCH_TYPES = [
	'Off',
	'Fat 10xx/11xx',
	'Fat/Slim/PRO 12xx/2xxx/7xxx',
	'General',
	'Extra',
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
	
	{'t':4, 'v':[0xFF]*2 + [0x00]*14},
	{'t':4, 'v':[0x00]*2 + [0xFF]*14},
	{'t':4, 'v':[0xFF]*1 + [0x00]*15},
	{'t':4, 'v':[0x00]*1 + [0xFF]*15},
	{'t':4, 'v':[0xFF,0xF0] + [0x00]*14},
	{'t':4, 'v':[0x00,0x0F] + [0xFF]*14},
]

BOOT_MODES = {b'\xFE':'Development', b'\xFB':'Assist', b'\xFF':'Release'}

# {'o':<offset>, 'l':<length>, 't':<type>, 'n':<name>}
SFLASH_PARTITIONS = {
	"s0_header"			: {"o": 0x00000000,	"l": 0x1000,	"n":"s0_head"},
	"s0_active_slot"	: {"o": 0x00001000,	"l": 0x1000,	"n":"s0_act_slot"},
	"s0_MBR1"			: {"o": 0x00002000,	"l": 0x1000,	"n":"s0_mbr1"},
	"s0_MBR2"			: {"o": 0x00003000,	"l": 0x1000,	"n":"s0_mbr2"},
	"s0_emc_ipl_a"		: {"o": 0x00004000,	"l": 0x60000,	"n":"sflash0s0x32"},
	"s0_emc_ipl_b"		: {"o": 0x00064000,	"l": 0x60000,	"n":"sflash0s0x32b"},
	"s0_eap_kbl"		: {"o": 0x000C4000,	"l": 0x80000,	"n":"sflash0s0x33"},
	"s0_wifi"			: {"o": 0x00144000,	"l": 0x80000,	"n":"sflash0s0x38"},
	"s0_nvs"			: {"o": 0x001C4000,	"l": 0xC000,	"n":"sflash0s0x34"},
	"s0_blank"			: {"o": 0x001D0000,	"l": 0x30000,	"n":"sflash0s0x0"},
	"s1_header"			: {"o": 0x00200000,	"l": 0x1000,	"n":"s1_head.crypt"},
	"s1_active_slot"	: {"o": 0x00201000,	"l": 0x1000,	"n":"s1_act_slot.crypt"},
	"s1_MBR1"			: {"o": 0x00202000,	"l": 0x1000,	"n":"s1_mbr1.crypt"},
	"s1_MBR2"			: {"o": 0x00203000,	"l": 0x1000,	"n":"s1_mbr2.crypt"},
	"s1_samu_ipl_a"		: {"o": 0x00204000,	"l": 0x3E000,	"n":"sflash0s1.cryptx2"},
	"s1_samu_ipl_b"		: {"o": 0x00242000,	"l": 0x3E000,	"n":"sflash0s1.cryptx2b"},
	"s1_idata"			: {"o": 0x00280000,	"l": 0x80000,	"n":"sflash0s1.cryptx1"},
	"s1_bd_hrl"			: {"o": 0x00300000,	"l": 0x80000,	"n":"sflash0s1.cryptx39"},
	"s1_VTRM"			: {"o": 0x00380000,	"l": 0x40000,	"n":"sflash0s1.cryptx6"},
	"s1_CoreOS_A"		: {"o": 0x003C0000,	"l": 0xCC0000,	"n":"sflash0s1.cryptx3"},
	"s1_CoreOS_B"		: {"o": 0x01080000,	"l": 0xCC0000,	"n":"sflash0s1.cryptx3b"},
	"s1_blank"			: {"o": 0x01D40000,	"l": 0x2C0000,	"n":"sflash0s1.cryptx40"},
}

# 'KEY':{'o':<offset>, 'l':<length>, 't':<type>, 'n':<name>}
SFLASH_AREAS = {
	
	'ACT_SLOT'	: {'o':0x001000,	'l':1,			't':'b',	'n':'Active slot'},			# 0x00 - A 0x80 - B
	
	'BOARD_ID'	: {'o':0x1C4000,	'l':8,			't':'b',	'n':'Board ID'},			# SAA-001, SAB-00, etc
	'MAC'		: {'o':0x1C4021,	'l':6,			't':'b',	'n':'MAC Address'},
	'MB_SN'		: {'o':0x1C8000,	'l':16,			't':'s',	'n':'Motherboard Serial'},
	'SN'		: {'o':0x1C8030,	'l':17,			't':'s',	'n':'Console Serial'},
	'SKU'		: {'o':0x1C8041,	'l':13,			't':'s',	'n':'SKU Version'},
	'REGION'	: {'o':0x1C8047,	'l':2,			't':'s',	'n':'Region code'},
	
	'NVS1'		: {'o':0x1C9000,	'l':0x1610,		't':'b',	'n':'1C9000 <-> 1CA610'},
	'NVS2'		: {'o':0x1CA000,	'l':0xFFF,		't':'b',	'n':'1CA000 <-> 1CAFFF'},
	
	'BOOT_MODE'	: {'o':0x1C9000,	'l':1,			't':'b',	'n':'Boot mode'},			# Development(FE), Assist(FB), Release(FF)
	'MEM_BGM'	: {'o':0x1C9003,	'l':1,			't':'b',	'n':'Memory budget mode'},	# Large(FE), Normal(FF)
	'SLOW_HDD'	: {'o':0x1C9005,	'l':1,			't':'b',	'n':'HDD slow mode'},		# On(FE), Off(FF)
	'SAFE_BOOT'	: {'o':0x1C9020,	'l':1,			't':'b',	'n':'Safe boot'},			# On(01), Off(00/FF)
	'SMI'		: {'o':0x1C9060,	'l':4,			't':'b',	'n':'SMI'},
	'FW_MIN'	: {'o':0x1C9062,	'l':2,			't':'b',	'n':'Minimal FW'},
	'FW_VER'	: {'o':0x1C906A,	'l':2,			't':'b',	'n':'FW in active slot'},
	'SAMUBOOT'	: {'o':0x1C9323,	'l':1,			't':'b',	'n':'SAMU enc'},	
	'HDD'		: {'o':0x1C9C00,	'l':60,			't':'s',	'n':'HDD'},
	'HDD_TYPE'	: {'o':0x1C9C3C,	'l':4,			't':'s',	'n':'HDD type'},
	
	'EAP_MGC'	: {'o':0x1C91FC,	'l':4,			't':'b',	'n':b'\xE5\xE5\xE5\x01'},	# Eap key magic
	
	'EAP_KEY'	: {'o':0x1C9200,	'l':0x60,		't':'b',	'n':'Hdd eap key'},			# Length 0x40 / 0x60
	'SYS_FLAGS'	: {'o':0x1C9310,	'l':64,			't':'b',	'n':'System flags'},		# Clean FF*64
	'MEMTEST'	: {'o':0x1C9310,	'l':1,			't':'b',	'n':'Memory test'},			# On(01), Off(00/FF)
	'RNG_KEY'	: {'o':0x1C9312,	'l':1,			't':'b',	'n':'RNG/Keystorage test'},	# On(01), Off(00/FF)
	'UART'		: {'o':0x1C931F,	'l':1,			't':'b',	'n':'UART'},				# On(01), Off(00)
	'MEMCLK'	: {'o':0x1C9320,	'l':1,			't':'b',	'n':'GDDR5 Memory clock'},
	'RESOLUTION': {'o':0x1CD048,	'l':1,			't':'b',	'n':'Resolution'},			# Reset(00), 1080i(01), 720p(02), 1080p(03), 4K(04), 4K HDR(05), Auto(13)
	'RES_RESET'	: {'o':0x1CD188,	'l':1,			't':'b',	'n':'Reset resolution'},	# On(01), Off(00)
	
	'BTNSWAP'	: {'o':0x1CA040,	'l':1,			't':'b',	'n':'Buttons swap'},		# X(01), O(00/FF)
	'FW_C'		: {'o':0x1CA5D8,	'l':1,			't':'b',	'n':'FW Counter'},
	'FW_PC'		: {'o':0x1CA5D9,	'l':1,			't':'b',	'n':'FW Patch Counter'},
	'IDU'		: {'o':0x1CA600,	'l':1,			't':'b',	'n':'IDU (Kiosk mode)'},	# On(01), Off(00/FF)
	'UPD_MODE'	: {'o':0x1CA601,	'l':1,			't':'b',	'n':'Update mode'},			# On(10), Off(00)
	'UPD_VAR'	: {'o':0x1CA602,	'l':1,			't':'b',	'n':'Update variant'},		# 0x30 hdd
	'REG_REC'	: {'o':0x1CA603,	'l':1,			't':'b',	'n':'Registry recovery'},	# On(01), Off(00)
	'FW_V'		: {'o':0x1CA606,	'l':2,			't':'s',	'n':'FW Version'},
	'ARCADE'	: {'o':0x1CA609,	'l':1,			't':'s',	'n':'Arcade mode'},			# On(01), Off(00/FF)
	
	'MANU'		: {'o':0x1CBC00,	'l':32,			't':'b',	'n':'MANU mode'},			# Enabled(0*32), Disabled(FF*32)
	
	'CORE_SWCH'	: {'o':0x201000,	'l':16,			't':'b',	'n':'Slot switch hack'},
}

SOUTHBRIDGES = [
	{'code':[0x01, 0x02], 'name':'Aeolia A0',	'ic':'CXD90025'},
	{'code':[0x0D, 0x0E], 'name':'Aeolia A1/A2','ic':'CXD90025'},
	{'code':[0x20, 0x21], 'name':'Belize A0/B0','ic':'CXD90036'},
	{'code':[0x24, 0x25], 'name':'Baikal B1',	'ic':'CXD90042'},
	{'code':[0x2A, 0x2B], 'name':'Belize 2 A0',	'ic':'CXD90046'},
]

TORUS_VERS = [
	{'code':0x03, 'name':'Version 1'},
	{'code':0x22, 'name':'Version 2'},
	{'code':0x30, 'name':'Version 3'},
]

MAGICS = {
	"MBR"		: {"o": 0x00,		"v":b'SONY COMPUTER ENTERTAINMENT INC.'},
	"MBR1"		: {"o": 0x2000,		"v":b'Sony Computer Entertainment Inc.'},
	"MBR2"		: {"o": 0x3000,		"v":b'Sony Computer Entertainment Inc.'},
}



# MBR parser

class Partition(ctypes.Structure):
	_pack_ = 1
	_fields_ = [
		("start_lba",	ctypes.c_uint32),
		("n_sectors",	ctypes.c_uint32),
		("type",		ctypes.c_uint8),		# part_id?
		("flag",		ctypes.c_uint8),
		("unknown",		ctypes.c_uint16),
		("padding",		ctypes.c_uint64)
	]
	
	def getName(self):
		code = self.type
		return PARTITIONS_TYPES[code] if code in PARTITIONS_TYPES else 'UNK_'+str(code)
	
	def getOffset(self):
		return self.start_lba * BLOCK_SIZE
	
	def getSize(self):
		return self.n_sectors * BLOCK_SIZE

class MBR_v1(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("magic", 		ctypes.c_uint8 * 0x20),	# SONY COMPUTER ENTERTAINMENT INC.
        ("version", 	ctypes.c_uint32),		# 1
        ("mbr1_start",	ctypes.c_uint32),		# ex: 0x10
        ("mbr2_start",	ctypes.c_uint32),		# ex: 0x18
        ("unk",			ctypes.c_uint32 * 4),	# ex: (1, 1, 8, 1)
        ("reserved",	ctypes.c_uint32),
        ("unused",		ctypes.c_uint8 * 0x1C0)
    ]

class MBR_v4(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("magic",		ctypes.c_uint8 * 0x20),	# Sony Computer Entertainment Inc.
        ("version",		ctypes.c_uint32),		# 4
        ("n_sectors",	ctypes.c_uint32),
        ("reserved",	ctypes.c_uint64),
        ("loader_start",ctypes.c_uint32),		# ex: 0x11, 0x309
        ("loader_count",ctypes.c_uint32),		# ex: 0x267
        ("reserved2",	ctypes.c_uint64),
        ("partitions",	Partition * 16)
	]

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
	code = getNorData(file, 'REGION', True)
	for k in PS_REGIONS:
		if code in PS_REGIONS[k]['c']:
			return [code, PS_REGIONS[k]['n']]
	return [code, STR_UNKNOWN]



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
	return SWITCH_TYPES[0]+' '+Utils.hex(bytes(pattern),'')



def getNorFW(f, active_slot = ''):
	
	fw = getNorData(f, 'FW_VER')
	
	if 0xFF in fw:
		fw = getNorData(f, 'FW_V')
	
	fw = '{:X}.{:02X}'.format(fw[1], fw[0])
	"""
	fw = getNorData(f, 'FW_VER')
	o_fw = getNorData(f, 'FW_V')
	fw = '{:X}.{:02X}'.format(fw[1], fw[0]) + ' {:X}.{:02X}'.format(o_fw[1], o_fw[0])
	"""
	mfw = getNorData(f, 'FW_MIN')
	mfw = '{:X}.{:02X}'.format(mfw[1], mfw[0]) if mfw[0] != 0xFF else ''
	
	bfw = ['']
	if active_slot:
		slot = 'a' if active_slot == 'b' else 'b'
		pname = 's0_emc_ipl_'+slot
		md5 = getNorPartitionMD5(f, pname)
		data = getDataByPartition(pname)
		
		if md5 in data:
			fw2 = data[md5]['fw']
			bfw = fw2 if len(fw2) == 1 else [fw2[0], fw2[-1]]
	
	return {'c':fw, 'b':bfw, 'min':mfw}



def isFwInList(fw, fw_list):
	try: fw_cur = int(fw.replace('.',''))
	except: fw_cur = 0
	fw_min = int(fw_list[0].replace('.',''))
	fw_max = int(fw_list[-1].replace('.',''))
	return fw_cur >= fw_min and fw_cur <= fw_max



def getFwFilename(item, folder):
	md5 = item['md5']
	#print(folder, md5)
	for file in os.listdir(folder):
		path = os.path.join(folder, file)
		if not os.path.isdir(path) and md5 in file:
			return path
	return ''



def getPartitionName(code):
	return PARTITIONS_TYPES[code] if code in PARTITIONS_TYPES else 'Unk_'+str(code)



def getNorPartition(f, name):
	if not name in SFLASH_PARTITIONS:
		return ''
	return Utils.getData(f, SFLASH_PARTITIONS[name]['o'], SFLASH_PARTITIONS[name]['l'])



def getNorPartitionMD5(f, name):
	data = getNorPartition(f, name)
	if len(data) > 0:
		return hashlib.md5(data).hexdigest()
	return ''



def getDataByPartition(name):
	
	if not name:
		return False
	elif name.find('eap_kbl') >= 0:
		return Data.EAP_KBL_MD5
	elif name.find('emc_ipl') >= 0:
		return Data.EMC_IPL_MD5
	elif name.find('wifi') >= 0:
		return Data.TORUS_FW_MD5
	
	return False



def getDataByPartitionAndType(name, type, fw = False):
	data = getDataByPartition(name)
	items = []
	if not data:
		return items
	for key in data:
		if data[key]['t'] == type:
			item = data[key]
			item['md5'] = key
			if fw and isFwInList(fw, item['fw']):
				return item
			items.append(item)
	
	return {} if fw else items



def checkMagic(data, key):
	if len(data) <= 0:
		return False
	if key in MAGICS:
		offset = MAGICS[key]['o']
		length = offset + len(MAGICS[key]['v'])
		if data[offset:length] == MAGICS[key]['v']:
			return True
	return False



def getPartitionsInfo(f):
	# f - file in rb/r+b mode
	f.seek(MBR_SIZE)
	# active slot at 0x1000
	active = f.read(1)
	
	base = MBR_SIZE*2 if active == 0x00 else MBR_SIZE*3
	f.seek(base)
	mbr = MBR_v4()
	f.readinto(mbr)
	
	partitions = []
	
	for i in range(len(mbr.partitions)):
		p = mbr.partitions[i]
		if p.getSize() == 0:
			continue
		partitions.append({
			'name'		: p.getName(),
			'offset'	: p.getOffset() + base,
			'size'		: p.getSize(),
			'type'		: p.type,
		})
	
	return {'slot':active, 'base':base, 'parts':partitions}



def getTorusInfo(f):
	torus_md5 = getNorPartitionMD5(f, 's0_wifi')
	torus = Data.TORUS_FW_MD5[torus_md5]['t'] if torus_md5 in Data.TORUS_FW_MD5 else 0
	
	for k in range(len(TORUS_VERS)):
		if torus == TORUS_VERS[k]['code']:
			return TORUS_VERS[k]
	
	return {'code':torus, 'name':STR_UNKNOWN}



def getSouthBridge(f):
	
	slot = getActiveSlot(f)
	md5_emc_a = getNorPartitionMD5(f, 's0_emc_ipl_a')
	md5_emc_b = getNorPartitionMD5(f, 's0_emc_ipl_b')
	md5_eap = getNorPartitionMD5(f, 's0_eap_kbl')
	
	emc_a = Data.EMC_IPL_MD5[md5_emc_a]['t'] if md5_emc_a in Data.EMC_IPL_MD5 else 0
	emc_b = Data.EMC_IPL_MD5[md5_emc_b]['t'] if md5_emc_b in Data.EMC_IPL_MD5 else 0
	eap = Data.EAP_KBL_MD5[md5_eap]['t'] if md5_eap in Data.EAP_KBL_MD5 else 0
	
	# check EAP first
	for k in range(len(SOUTHBRIDGES)):
		code = SOUTHBRIDGES[k]['code']
		if code[1] == eap: return SOUTHBRIDGES[k]
	
	# check emc (active slot)
	for k in range(len(SOUTHBRIDGES)):
		code = SOUTHBRIDGES[k]['code']
		if code[0] == (emc_a if slot == 'a' else emc_b): return SOUTHBRIDGES[k]
	
	# check emc (inactive slot) last chance
	for k in range(len(SOUTHBRIDGES)):
		code = SOUTHBRIDGES[k]['code']
		if code[0] == (emc_b if slot == 'a' else emc_a): return SOUTHBRIDGES[k]
	
	# unknown SB
	return {'code':[emc_a if emc_a else emc_b, eap], 'name':STR_UNKNOWN, 'ic':'XX'}

# NOR Areas data utils

def getNorAreaName(key):
	if key in SFLASH_AREAS:
		return SFLASH_AREAS[key]['n']
	return STR_UNKNOWN



def setNorData(file, key, val):
	if not key in SFLASH_AREAS:
		return False
	return Utils.setData(file, SFLASH_AREAS[key]['o'], val)



def setNorDataB(file, key, val):
	if not key in SFLASH_AREAS:
		return False
	return Utils.setData(file, SFLASH_AREAS[key]['o'] + BACKUP_OFFSET, val)



def getNorData(file, key, decode = False):
	if not key in SFLASH_AREAS:
		return 'False' if decode else False
	data = Utils.getData(file, SFLASH_AREAS[key]['o'], SFLASH_AREAS[key]['l'])
	return data.decode('utf-8','ignore').strip('\x00') if decode else data



def getNorDataB(file, key, decode = False):
	if not key in SFLASH_AREAS:
		return 'False' if decode else False
	data = Utils.getData(file, SFLASH_AREAS[key]['o'] + BACKUP_OFFSET, SFLASH_AREAS[key]['l'])
	return data.decode('utf-8','ignore').strip('\x00') if decode else data



def getModel(f):
	try:
		model = int(getNorData(f, 'SKU', True)[4:6])
	except:
		model = 0
	return model



def getMobo(board):
	#mb_codes = 0x1c4000
	codes = { 2: 'CV', 3: 'SA', 4: 'HA', 5: 'NV', }
	
	prefix = codes[board[0]] if board[0] in codes else '??'
	
	#mb_suffix = 0x1c4002 - All prefix 'CV' is 'N', all 'HA' is 'C', 'NV' is 'A','B' and 'G' no exist 'C'
	suffix = '?'
	if prefix == 'CV' and board[2] == 1: suffix = 'N'
	if prefix == 'HA' and board[2] == 1: suffix = 'C'
	if prefix == 'NV' and board[2] == 3: suffix = 'G'
	if prefix == 'SA' or (prefix == 'NV' and board[2] <= 2):
		suffix = chr(ord('A')-1+board[2])
	
	#mb_rev = Revision of board - ??? No exist SAA, SAB, SAC and HAC > 001, all are 001 - if board[0] <= 'HA' and board[2] <= 'C' Revision is 001
	rev = '001' if board[0] <= 4 and board[2] <= 3 else '00X'
	
	return {'name':prefix + suffix + '-' + rev, 'type':'Retail' if board[1] == 2 else 'Non-Retail'}



def getInfoForLegitSwitch(f):
	data = {
		'sn':getNorData(f, 'SN', True),
		'fw':getNorFW(f)['c'],
		'slot':getNorData(f, 'ACT_SLOT'),
		'switch':getNorData(f, 'CORE_SWCH'),
	}
	return data



def getActiveSlot(f):
	return 'a' if getNorData(f, 'ACT_SLOT')[0] == 0x00 else 'b'


def checkNVS(data, key = 'NVS1'):
	return STR_OK if not all(b == 0xFF or b == 0x00 for b in data) else STR_FAIL


def getOffsetRange(k, backup = False):
	extra = BACKUP_OFFSET if backup else 0
	return '%X~%X'%(SFLASH_AREAS[k]['o'] + extra, SFLASH_AREAS[k]['o'] + SFLASH_AREAS[k]['l'] + extra)



def getSFlashInfo(file = '-'):
	with open(file, 'rb') as f:
		
		active_slot = getActiveSlot(f)
		
		sku = getNorData(f, 'SKU', True)
		fw = getNorFW(f, active_slot)
		SB = getSouthBridge(f)
		torus = getTorusInfo(f)
		
		samu = getNorData(f, 'SAMUBOOT')[0]
		region = getConsoleRegion(f)
		board = getNorData(f, 'BOARD_ID')
		mobo = getMobo(board)
		
		try:
			hdd = (' / ').join(Utils.swapBytes(getNorData(f, 'HDD')).decode('utf-8').split())
		except:
			hdd = STR_NO_INFO
		
		info = {
			'FILE'			: os.path.basename(file),
			'MD5'			: Utils.getFileMD5(file),
			'SKU / Board ID': sku + ' [' + UI.highlight(Utils.hex(board, ':')) + '] ~' + mobo['name'],
			'Region'		: '[%s] %s / [%s]'%(region[0], region[1], mobo['type']),
			'SN / Mobo SN'	: getNorData(f, 'SN', True)+' / '+getNorData(f, 'MB_SN', True),
			'Southbridge'	: '%s [%s] [%02X:%02X]'%(SB['name'], SB['ic'], SB['code'][0], SB['code'][1]),
			'Torus (WiFi)'	: '%s [0x%02X]'%(torus['name'],torus['code']),
			'MAC'			: Utils.hex(getNorData(f, 'MAC'),':'),
			'HDD'			: hdd,
			'FW (active)'	: fw['c'] + ' ['+active_slot.upper()+']' + (' [min '+fw['min']+']' if fw['min'] else ''),
			'FW (backup)'	: ' <-> '.join(fw['b']),
			'GDDR5'			: ('0x{:02X} {:d}MHz | 0x{:02X} {:d}MHz').format(*getMemClock(f)),
			'SAMU BOOT'		: ('%d [0x%02X]')%(samu, samu),
			'UART'			: (Lang.STR_ON if getNorData(f, 'UART')[0] == 1 else Lang.STR_OFF),
			'Slot switch'	: getSlotSwitchInfo(f),
		}
	
	return info



def getCanonicalName(fpath):
	with open(fpath, 'rb') as f:
		
		sku = getNorData(f, 'SKU', True)[:9].replace('-','')
		sn = getNorData(f, 'SN', True)
		sn = sn if sn else '0'*10
		sb = getSouthBridge(f)['ic'][-2:]
		mobo = getMobo(getNorData(f, 'BOARD_ID'))['name']
		slot = 'a' if getNorData(f, 'ACT_SLOT') == b'\x00' else 'b'
		fw = getNorFW(f, slot)
		fws = '-'.join(fw['b'])
	
	return '_'.join([sku, sn, sb, mobo, fw['c'], slot, fws]).upper()