import os, sys

from lang import *
from ps4utils import *

#==============================================================
# Nor Tools
#==============================================================

def toggleUart(file):
	with open(file, 'r+b') as f:
		
		cur = getNorData(f, 'UART')[0]
		val = b'\x01' if cur == 0 else b'\x00'
		
		setNorData(f, 'UART',  val)
		setNorDataB(f, 'UART', val)
	
	setStatus(MSG_UART+(MSG_OFF if val != b'\x01' else MSG_ON))



def toggleMemtest(file):
	with open(file, 'r+b') as f:
		
		cur = getNorData(f, 'MEMTEST1')[0]
		val = b'\x01' if cur == 0 else b'\x00'
		
		setNorData(f, 'MEMTEST1',  val)
		setNorDataB(f, 'MEMTEST1', val)
		
		setNorData(f, 'MEMTEST2',  val)
		setNorDataB(f, 'MEMTEST2', val)

	
	setStatus(MSG_MEMTEST.format('ON' if val == b'\x01' else 'OFF'))



def screenSysFlags(file):
	os.system('cls')
	print(TITLE + TAB_SYSFLAGS)
	
	with open(file, 'r+b') as f:
		
		print(MSG_CURRENT+'\n'+DIVIDER_DASH)
		flags = getNorData(f, 'SYS_FLAGS')
		for i in range(0, len(flags), 0x10):
			print(' '+getHex(flags[i:i+0x10]))
		
		choice = input(MSG_CONFIRM)
		
		if choice.lower() != 'y':
			return 0
		
		val = b'\xFF'*64
		setNorData(f, 'SYS_FLAGS',  val)
		setNorDataB(f, 'SYS_FLAGS', val)
	
	setStatus(MSG_SYSFLAGS_CLEAN)


def screenMemClock(file):
	os.system('cls')
	print(TITLE + MSG_OVERCLOCKING)
	print(TAB_MEMCLOCK)
	
	with open(file, 'r+b') as f:
		
		clocks = getMemClock(f)
		
		print(MSG_CURRENT+('0x{:02X} {:d}MHz | 0x{:02X} {:d}MHz').format(*clocks))
		if clocks[0] != clocks[2]:
			print(MSG_DIFF_SLOT_VALUES)
		
		try:
		    frq = int(input(MSG_MEMCLOCK_INPUT))
		except:
		    return
		
		if frq >= 400 and frq <= 2000:
		    frq = clockToRaw(frq)
		else:
		    frq = 255
		
		setNorData(f, 'MEMCLK',  frq.to_bytes(1, 'big'))
		setNorDataB(f, 'MEMCLK', frq.to_bytes(1, 'big'))



def screenSamuBoot(file):
	os.system('cls')
	print(TITLE + TAB_SAMU_BOOT)
	
	with open(file, 'r+b') as f:
		
		cur = getNorData(f, 'SAMUBOOT')[0]
		print(MSG_CURRENT+('{:d} [0x{:02X}]').format(cur,cur))
		
		try:
		    frq = int(input(MSG_SAMU_INPUT))
		except:
		    return
		
		if frq < 0 or frq > 255:
		    frq = 255
		
		setNorData(f, 'SAMUBOOT',  frq.to_bytes(1, 'big'))
		setNorDataB(f, 'SAMUBOOT', frq.to_bytes(1, 'big'))
	
	setStatus(MSG_SAMU_UPD+('{:d} [0x{:02X}]').format(frq,frq))



def screenDowngrade(file):
	os.system('cls')
	print(TITLE + MSG_DOWNGRADE)
	
	with open(file, 'r+b') as f:
		
		print(MSG_CURRENT+'\n'+DIVIDER_DASH+' '+getHex(getNorData(f, 'CORE_SWCH')))
		
		print(TAB_DOWNGRADE)
		
		for i in range(1, len(SWITCH_TYPES)):
			print(' '+SWITCH_TYPES[i]+'\n')
			for n in range(len(SWITCH_BLOBS)):
				if SWITCH_BLOBS[n]['t'] == i:
					print('  '+str(n+1)+': '+getHex(SWITCH_BLOBS[n]['v']))
			print('')
		
		while 1:
			try:
				choice = int(input(MSG_CHOICE))
			except:
				return
			
			if choice <= 0 or choice > len(SWITCH_BLOBS):
				print(MSG_ERROR_CHOICE)
			else:
				pattern = SWITCH_BLOBS[choice-1]
				break
		
		setNorData(f, 'CORE_SWCH', bytes(pattern['v']))
	
	setStatus(MSG_DOWNGRADE_UPD + SWITCH_TYPES[pattern['t']] + ' [' + str(choice)+']')



def screenNorTools(file):
	os.system('cls')
	print(TITLE+TAB_NOR_INFO)
	
	if not showNorInfo(file):
		return screenFileSelect()
	
	print(TAB_ACTIONS)
	getMenu(MENU_NOR_ACTIONS)
	
	showStatus()
	
	choice = input(MSG_CHOICE)
	
	if choice == '0':
	    return screenFileSelect()
	elif choice == '1':
	    toggleUart(file)
	elif choice == '2':
	    toggleMemtest(file)
	elif choice == '3':
		screenSysFlags(file)
	elif choice == '4':
	    screenMemClock(file)
	elif choice == '5':
	    screenSamuBoot(file)
	elif choice == '6':
		screenDowngrade(file)
	elif choice == '7':
	    exit(1)
	
	screenNorTools(file)



def showNorInfo(file = '-'):
	if not checkFileSize(file, NOR_DUMP_SIZE):
		return False
	
	with open(file, 'rb') as f:
	
		fw1 = getNorData(f, 'FW_SLOT1')
		fw2 = getNorData(f, 'FW_SLOT2')
		sb = getNorData(f, 'SAMUBOOT')[0]
		
		try:
			hdd = (' / ').join(swapBytes(getNorData(f, 'HDD')).decode('utf-8').split())
		except:
			hdd = MSG_NO_INFO
		
		INFO = {
			'FILE'			: os.path.basename(file),
			'MD5'			: getFileMD5(file),
			'SKU'			: getNorData(f, 'SKU').decode('utf-8'),
			'SN / Mobo SN'	: getNorData(f, 'SN').decode('utf-8')+' / '+getNorData(f, 'MB_SN').decode('utf-8'),
			'MAC'			: getHex(getNorData(f, 'MAC'),':'),
			'HDD'			: hdd,
			'VERS'			: ('{:02X}.{:02X} | {:02X}.{:02X}').format(fw1[1], fw1[0], fw2[1], fw2[0]),
			'GDDR5'			: ('0x{:02X} {:d}MHz | 0x{:02X} {:d}MHz').format(*getMemClock(f)),
			'SAMU BOOT'		: ('{:d} [0x{:02X}]').format(sb,sb),
			'UART'			: (MSG_ON if getNorData(f, 'UART')[0] == 1 else MSG_OFF),
			'MEMTEST'		: (MSG_ON if getNorData(f, 'MEMTEST1')[0] == 1 else MSG_OFF),
			'Slot switch'	: getSlotSwitchInfo(f)
		}
	
	for key in INFO:
		print(' '+key.ljust(16,' ')+' : '+INFO[key])
	
	return True


#==============================================================
# Syscon Tools
#==============================================================


def toggleDebug(file):
	with open(file, 'r+b') as f:
		
		cur = getSysconData(f, 'DEBUG')[0]
		val = b'\x04' if cur == 0x84 or cur == 0x85 else b'\x85'
		
		setSysconData(f, 'DEBUG',  val)
	
	setStatus(MSG_DEBUG+(MSG_OFF if val == b'\x04' else MSG_ON))

def screenSysconTools(file):
	os.system('cls')
	print(TITLE+TAB_SYSCON_INFO)
	
	if not showSysconInfo(file):
		return screenFileSelect()
	
	print(TAB_ACTIONS)
	getMenu(MENU_SC_ACTIONS)
	
	showStatus()
	
	choice = input(MSG_CHOICE)
	
	if choice == '0':
	    return screenFileSelect()
	elif choice == '1':
		toggleDebug(file)
	elif choice == '2':
		screenActiveSNVS(file)
	elif choice == '3':
		screenAutoPatchSNVS(file)
	elif choice == '4':
		screenManualPatchSNVS(file)
	elif choice == '5':
	    exit(1)
	
	screenSysconTools(file)



def screenActiveSNVS(file):
	os.system('cls')
	print(TITLE+TAB_LAST_SVNS)
	
	with open(file, 'rb') as f:
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
	
	entries = SNVS.getLastDataEntries()
	for i,v in enumerate(entries):
		base = SNVS.getLastDataBlockOffset(True)
		print(' {:5X} | '.format(base + (i * NvsEntry.getEntrySize())) + getHex(v))
	
	input(MSG_BACK)



def screenAutoPatchSNVS(file):
	os.system('cls')
	print(TITLE+TAB_APATCH_SVNS)
	input(MSG_BACK)


def screenManualPatchSNVS(file):
	os.system('cls')
	print(TITLE+TAB_MPATCH_SVNS)
	input(MSG_BACK)


def showSysconInfo(file):
	if not checkFileSize(file, SYSCON_DUMP_SIZE):
		return False
	
	with open(file, 'rb') as f:
		magic = checkSysconData(f, 'MAGIC_1') and checkSysconData(f, 'MAGIC_2') and checkSysconData(f, 'MAGIC_3')
		debug = getSysconData(f, 'DEBUG')[0]
		debug = MSG_ON if debug == 0x84 or debug == 0x85 else MSG_OFF
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
		SNVS_INFO = 'Vol[{:d}] Data[{:d}] Counter[0x{:X}] offset[0x{:5X}]'.format(
			SNVS.active_volume,
			SNVS.active_entry.getLink(),
			SNVS.active_entry.getCounter(),
			SNVS.getLastDataBlockOffset(True)
		)
		
		INFO = {
			'FILE'			: os.path.basename(file),
			'MD5'			: getFileMD5(file),
			'Magic'			: ('True' if magic else 'False'),
			'Debug'			: debug,
			'SNVS'			: SNVS_INFO,
		}
	
	for key in INFO:
		print(' '+key.ljust(16,' ')+' : '+INFO[key])
	
	return True

#==============================================================
# Common
#==============================================================

def launchTool(fname):
	f_size = os.stat(fname).st_size
	
	if f_size == NOR_DUMP_SIZE:
		return screenNorTools(fname)
	elif f_size == SYSCON_DUMP_SIZE:
		return screenSysconTools(fname)
	else:
		setStatus(MSG_UNK_FILE_TYPE + ' {}'.format(fname))
		return screenFileSelect()



def screenFileSelect(fname = ''):
	
	if len(fname) and os.path.isfile(fname):
		return launchTool(fname)
	
	os.system('cls')
	print(TITLE + TAB_FILE_LIST)
	
	files = []
	for f in os.listdir(os.getcwd()):
		if f.lower().endswith('.bin'):
			files.append(f)
			print(' '+str(len(files))+': '+f)
	
	if len(files) == 0:
		return screenHelp()
	
	showStatus()
	
	file = ''
	while not file:
	    try:
	        choice = int(input(MSG_CHOICE))
	        if 1 <= choice <= len(files):
	            file = files[choice - 1]
	        else:
	            print(MSG_ERROR_CHOICE)
	    except ValueError:
	        print(MSG_ERROR_INPUT)
	
	launchTool(file)



def screenCompareFiles(list):
	os.system('cls')
	print(TITLE + TAB_COMPARE)
	
	res = True
	c_md5 = False
	for i, file in enumerate(list):
		if not file or not os.path.isfile(file):
			print((MSG_FILE_NOT_EXISTS).format(file))
			continue
		else:
			md5 = getFileMD5(file)
			c_md5 = md5 if not c_md5 else c_md5
			if c_md5 != md5:
				res = False
			print((' [{}] {}').format(md5,  os.path.basename(file)))
	
	print(DIVIDER)
	print((MSG_FILES_MATCH if res else MSG_FILES_MISMATCH)+' | Result: '+str(res))
	input(MSG_BACK)
	
	screenFileSelect()



def screenHelp():
	os.system('cls')
	print(TITLE + MSG_HELP)
	
	showStatus()
	
	input(MSG_BACK)



def main(args):
    
    args.pop(0)
    
    if len(args) >= 2:
    	screenCompareFiles(args)
    elif len(args) == 1:
    	if args[0] in ['help','-help','h','-h','?']:
    		screenHelp()
    	else:
    		screenFileSelect(args[0])
    else:
    	screenFileSelect()



main(sys.argv)