import os, sys

from lang import *
from ps4utils import *
from ps4hddeap import getHddEapKey

#==============================================================
# Nor Tools
#==============================================================



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
		    raw = clockToRaw(frq)
		else:
			frq = 0
			raw = 255
		
		setNorData(f, 'MEMCLK',  raw.to_bytes(1, 'big'))
		setNorDataB(f, 'MEMCLK', raw.to_bytes(1, 'big'))
		
		setStatus(MSG_MEMCLOCK_SET.format(frq,raw))



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
		
		print(MSG_CURRENT+getSlotSwitchInfo(f))
		
		print(TAB_DOWNGRADE,end='')
		
		for i in range(1, len(SWITCH_TYPES)):
			print('\n '+SWITCH_TYPES[i]+'\n')
			for n in range(len(SWITCH_BLOBS)):
				if SWITCH_BLOBS[n]['t'] == i:
					print('  '+str(n+1)+': '+getHex(SWITCH_BLOBS[n]['v']))
		
		print(DIVIDER)
		print(' 0:'+MSG_GO_BACK)
		
		showStatus()
		
		try:
			choice = int(input(MSG_CHOICE))
		except:
			return
		
		if choice == 0:
			return
		elif choice < 0 or choice > len(SWITCH_BLOBS):
			setStatus(MSG_ERROR_CHOICE)
		else:
			pattern = SWITCH_BLOBS[choice-1]
			setNorData(f, 'CORE_SWCH', bytes(pattern['v']))
			setStatus(MSG_DOWNGRADE_UPD + SWITCH_TYPES[pattern['t']] + ' [' + str(choice)+']')
	
	screenDowngrade(file)



def screenFlagsToggler(file):
	os.system('cls')
	print(TITLE + MSG_PATCHES + TAB_NOR_FLAGS)
	
	with open(file, 'rb') as f:
		
		patches = [
			{'k':'UART',	'v':[b'\x00',b'\x01'], 'd':[MSG_OFF,MSG_ON]},
			{'k':'MEMTEST',	'v':[b'\x00',b'\x01'], 'd':[MSG_OFF,MSG_ON]},
			{'k':'RNG_KEY',	'v':[b'\x00',b'\x01'], 'd':[MSG_OFF,MSG_ON]},
			{'k':'BTNSWAP',	'v':[b'\x00',b'\x01'], 'd':['O - select','X - select']},
			{'k':'SLOW_HDD','v':[b'\xFF',b'\xFE'], 'd':[MSG_OFF,MSG_ON]},
			{'k':'MEM_BGM',	'v':[b'\xFE',b'\xFF'], 'd':['Large','Normal']},
			{'k':'SAFE_BOOT','v':[b'\xFF',b'\x01'], 'd':[MSG_OFF,MSG_ON]},
			{'k':'UPD_MODE','v':[b'\x00',b'\x10'], 'd':[MSG_OFF,MSG_ON]},
			{'k':'ARCADE',	'v':[b'\x00',b'\x01'], 'd':[MSG_OFF,MSG_ON]},
			{'k':'REG_REC',	'v':[b'\x00',b'\x01'], 'd':[MSG_OFF,MSG_ON]},
			{'k':'IDU',		'v':[b'\x00',b'\x01'], 'd':[MSG_OFF,MSG_ON]},
			{'k':'BOOT_MODE','v':[b'\xFE',b'\xFB',b'\xFF'], 'd':['Development','Assist','Release']},
			{'k':'MANU',	'v':[b'\x00'*32,b'\xFF'*32], 'd':[MSG_OFF,MSG_ON]},
		]
		
		for i in range(len(patches)):
			name = getNorAreaName(patches[i]['k'])
			val = getNorData(f, patches[i]['k'])
			str = '['+getHex(val,'')[:32]+']'
			for k in range(len(patches[i]['v'])):
				if val == patches[i]['v'][k]:
					str = patches[i]['d'][k]
			print(' {:2d}: {:24s}: {}'.format(i+1, name, str))
	
	print(DIVIDER)
	print(' c:'+MSG_CLEAN_FLAGS)
	print(' 0:'+MSG_GO_BACK)
	
	showStatus()
	
	num = -1
	try:
		choice = input(MSG_CHOICE)
		num = int(choice)
	except:
		if choice == 'c':
			screenSysFlags(file)
	
	if num == 0:
		return
	elif num > 0 and num <= len(patches):
		toggleFlag(file, patches[num-1])
	
	screenFlagsToggler(file)



def toggleFlag(file, patch):
	with open(file, 'r+b') as f:
		
		cur = getNorData(f, patch['k'])
		for i in range(0,len(patch['v'])):
			if cur == patch['v'][i]:
				break
		i = 0 if (i + 1) >= len(patch['v']) else i + 1
		val = patch['v'][i]
		
		setNorData(f, patch['k'],  patch['v'][i])
		#setNorDataB(f, patch['k'], patch['v'][i])
	
	setStatus(MSG_SET_TO.format(getNorAreaName(patch['k']),patch['d'][i]))



def screenEntropy(file):
	os.system('cls')
	print(TITLE + TAB_ENTROPY + '\n' + MSG_WAIT)
	
	stats = entropy(file)
	
	os.system('cls')
	print(TITLE+TAB_ENTROPY)
	
	info = {
		'Entropy': '{:.5f}'.format(stats['ent']),
		'0xFF': '{:.2f}%'.format(stats['ff']*100),
		'0x00': '{:.2f}%'.format(stats['00']*100),
		'Other': '{:.2f}%'.format((1 - stats['ff'] - stats['00'])*100),
	}
	
	showTable(info)
	
	input(MSG_BACK)



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
	    screenFlagsToggler(file)
	elif choice == '2':
	    screenMemClock(file)
	elif choice == '3':
	    screenSamuBoot(file)
	elif choice == '4':
		screenDowngrade(file)
	elif choice == '5':
		screenAdditionalTools(file)
	elif choice == '6':
	    exit(1)
	
	screenNorTools(file)



def screenAdditionalTools(file):
	os.system('cls')
	print(TITLE+TAB_ADDITIONAL)
	
	with open(file, 'rb') as f:
		sn = getNorData(f, 'SN').decode('utf-8','ignore')
	
	folder = os.path.dirname(file) + os.sep + sn
	
	getMenu(MENU_ADDTIONAL,1)
	
	showStatus()
	
	choice = input(MSG_CHOICE)
	
	if choice == '':
		return
	elif choice == '1':
		screenExtractNorDump(file)
	elif choice == '2':
		screenBuildNorDump(folder)
	elif choice == '3':
		screenHddKey(file)
	elif choice == '4':
		screenEntropy(file)
	
	screenAdditionalTools(file)



def screenHddKey(file):
	os.system('cls')
	print(TITLE+MSG_INFO_HDD_EAP+'\n')
	
	mode = input(MSG_USE_NEWBLOBS)
	
	print(TAB_HDD_KEY)
	getHddEapKey(file, True if mode == 'y' else False)
	
	input(MSG_BACK)



def screenExtractNorDump(file):
	os.system('cls')
	print(TITLE+TAB_NOR_EXTRACT)
	
	with open(file, 'rb') as f:
		sn = getNorData(f, 'SN').decode('utf-8','ignore')
		folder = os.path.dirname(file) + os.sep + sn + os.sep
		
		if not os.path.exists(folder):
			os.makedirs(folder)
		
		print(MSG_EXTRACTING.format(sn)+'\n')
		
		for i in range(len(NOR_PARTITIONS)):
			p = NOR_PARTITIONS[i]
			print(' {:2d}: {:16s} > {}'.format(i, p['t'], p['n']))
			
			with open(folder + p['n'],'wb') as out:
				out.write(getData(f, p['o'], p['l']))
		
		print('\n'+MSG_SAVED_TO.format(folder))
	
	print('\n'+MSG_DONE)
	
	input(MSG_BACK)



def screenBuildNorDump(folder):
	os.system('cls')
	print(TITLE+TAB_NOR_BUILD)
	
	if not os.path.exists(folder):
		print(MSG_NO_FOLDER.format(folder)+'\n\n'+MSG_ABORT)
		input(MSG_BACK)
		return
	
	print(MSG_FILES_CHECK.format(folder)+'\n')
	
	found = 0
	
	for i in range(len(NOR_PARTITIONS)):
		p = NOR_PARTITIONS[i]
		status = MSG_OK
		
		file = folder+os.sep+p['n']
		if not os.path.exists(file):
			status = MSG_NOT_FOUND
		elif os.stat(file).st_size != p['l']:
			status = MSG_BAD_SIZE
		else:
			found += 1
		
		print(' {:2d}: {:20s} - {}'.format(i, p['n'], status))
	
	print()
	
	if found == len(NOR_PARTITIONS):
		
		sn = '0'*17
		with open(folder+os.sep+NOR_PARTITIONS[8]['n']) as nvs:
			nvs.seek(0x4030)
			sn = nvs.read(17)
		
		fname = os.path.dirname(folder) + os.sep + sn + '.bin'
		
		print(MSG_BUILDING.format(fname))
		
		out = open(fname,"wb")
		
		for i in range(len(NOR_PARTITIONS)):
			file = folder+os.sep+NOR_PARTITIONS[i]['n']
			with open(file, 'rb') as f:
				out.write(f.read())
		
		out.close()
		
		print('\n'+MSG_DONE)
	else:
		print(MSG_ABORT)
	
	input(MSG_BACK)



def showNorInfo(file = '-'):
	if not checkFileSize(file, NOR_DUMP_SIZE):
		return False
	
	with open(file, 'rb') as f:
		
		sku = getNorData(f, 'SKU').decode('utf-8','ignore')
		
		old_fw = getNorData(f, 'FW_V')
		fw = getNorData(f, 'FW_VER') if old_fw[0] == 0xFF else old_fw
		
		sb = getNorData(f, 'SAMUBOOT')[0]
		region = getConsoleRegion(f)
		
		try:
			hdd = (' / ').join(swapBytes(getNorData(f, 'HDD')).decode('utf-8').split())
		except:
			hdd = MSG_NO_INFO
		
		info = {
			'FILE'			: os.path.basename(file),
			'MD5'			: getFileMD5(file),
			'SKU'			: sku,
			'Region'		: '[{}] {}'.format(region[0], region[1]),
			'SN / Mobo SN'	: getNorData(f, 'SN').decode('utf-8','ignore')+' / '+getNorData(f, 'MB_SN').decode('utf-8','ignore'),
			'MAC'			: getHex(getNorData(f, 'MAC'),':'),
			'HDD'			: hdd,
			'FW'			: '{:X}.{:02X} '.format(fw[1], fw[0]),
			'GDDR5'			: ('0x{:02X} {:d}MHz | 0x{:02X} {:d}MHz').format(*getMemClock(f)),
			'SAMU BOOT'		: ('{:d} [0x{:02X}]').format(sb,sb),
			'UART'			: (MSG_ON if getNorData(f, 'UART')[0] == 1 else MSG_OFF),
			'Slot switch'	: getSlotSwitchInfo(f)
		}
	
	showTable(info)
	
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



def printSnvsEntries(base,entries):
	
	for i,v in enumerate(entries):
		color = ''
		if v[1] in SC_UPD_TYPES:
			color = Clr.fg.cyan
		elif v[1] in SC_PRE1_TYPE:
			color = Clr.fg.orange
		elif v[1] in SC_PRE2_TYPE:
			color = Clr.fg.red
		print(' {:5X} | '.format(base + (i * NvsEntry.getEntrySize())) + color + getHex(v)+Clr.reset)



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
	base = SNVS.getLastDataBlockOffset(True)
	
	printSnvsEntries(base, entries)
	
	input(MSG_BACK)



def screenAutoPatchSNVS(file):
	os.system('cls')
	print(TITLE+TAB_APATCH_SVNS)
	
	with open(file, 'rb') as f:
		data = f.read()
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
	
	entries = SNVS.getLastDataEntries()
	
	base = SNVS.getLastDataBlockOffset(True)
	last = NvsEntry(entries[-1])
	
	index = getLast_080B_Index(entries)
	prev_index = getLast_080B_Index(entries[:index])
	
	cur_o = index * NvsEntry.getEntrySize() + base
	pre_o = prev_index * NvsEntry.getEntrySize() + base
	
	if index < 0 or prev_index < 0 or not isSysconPatchable(entries):
		print(MSG_UNPATCHABLE.format(len(entries),last.getCounter(),last.getIndex(), index, prev_index ))
		input(MSG_BACK)
		return
	
	out_file = os.path.basename(file).replace(" ", "_").rsplit('.', maxsplit=1)[0]
	
	options = MENU_PATCHES
	options[1] = options[1].format(len(entries) - index)
	
	print(Clr.fg.cyan+MSG_PATCH_INDEXES.format(cur_o, pre_o)+Clr.reset)
	getMenu(options,1)
	showStatus()
	
	choice = input(MSG_CHOICE)
	
	if choice == '':
	    return
	elif choice == '1':
		ofile = out_file+'_patch_A.bin'
		savePatchData(ofile, data, [{'o':cur_o,'d':b'\xFF'*NvsEntry.getEntrySize()*4}]);
		setStatus(MSG_PATCH_SAVED.format(ofile))
	elif choice == '2':
		ofile = out_file+'_patch_B.bin'
		savePatchData(ofile, data, [{'o':cur_o,'d':b'\xFF'*NvsEntry.getEntrySize()*(len(entries) - index)}]);
		setStatus(MSG_PATCH_SAVED.format(ofile))
	elif choice == '3':
		ofile = out_file+'_patch_C.bin'
		savePatchData(ofile, data, [{'o':cur_o,'d':data[pre_o:pre_o + NvsEntry.getEntrySize()*4]}]);
		setStatus(MSG_PATCH_SAVED.format(ofile))
	elif choice == '4':
		ofile = out_file+'_patch_D.bin'
		new_entries = bytearray()
		prev_c = False
		for i in range(len(entries)):
			record = NvsEntry(entries[i])
			cur_c = record.getCounter()
			if prev_c and cur_c != prev_c+1:
				cur_c = prev_c+1
				record.setCounter(cur_c)
			prev_c = cur_c
			new_entries += record.entry
		savePatchData(ofile, data, [{'o':base,'d':new_entries}]);
		setStatus(MSG_PATCH_SAVED.format(ofile))
	else:
		setStatus(MSG_ERROR_CHOICE)
	
	screenAutoPatchSNVS(file)



def screenManualPatchSNVS(file):
	os.system('cls')
	print(TITLE+MSG_INFO_SC_MPATCH+TAB_MPATCH_SVNS)
	
	with open(file, 'r+b') as f:
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
		entries = SNVS.getLastDataEntries()
		
		records_count = 16 if len(entries) > 16 else len(entries)
		print(MSG_LAST_DATA.format(records_count, len(entries)))
		print()
		
		base = SNVS.getLastDataBlockOffset(True) + NvsEntry.getEntrySize() * (len(entries) - records_count)
		printSnvsEntries(base, entries[-records_count:])
		
		try:
			num = int(input(MSG_MPATCH_INPUT))
		except:
			return
		
		if num > 0 and num < len(entries):
			length = num*NvsEntry.getEntrySize()
			offset += NvsEntry.getEntrySize() - length
			setData(f, offset, b'\xFF'*length)
			setStatus(MSG_PATCH_SUCCESS.format(num)+' [{:X} - {:X}]'.format(offset,offset + length))
		else:
			setStatus(MSG_PATCH_CANCELED)



def showSysconInfo(file):
	if not checkFileSize(file, SYSCON_DUMP_SIZE):
		return False
	
	with open(file, 'rb') as f:
		magic = checkSysconData(f, 'MAGIC_1') and checkSysconData(f, 'MAGIC_2') and checkSysconData(f, 'MAGIC_3')
		debug = getSysconData(f, 'DEBUG')[0]
		debug = MSG_ON if debug == 0x84 or debug == 0x85 else MSG_OFF
		ver = getSysconData(f, 'VERSION')
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
		entries = SNVS.getLastDataEntries()
		snvs_info = 'Vol[{:d}] Data[{:d}] Counter[0x{:X}]'.format(
			SNVS.active_volume,
			SNVS.active_entry.getLink(),
			SNVS.active_entry.getCounter(),
		)
		
		info = {
			'FILE'			: os.path.basename(file),
			'MD5'			: getFileMD5(file),
			'Magic'			: ('True' if magic else 'False'),
			'Debug'			: debug,
			'Version'		: '{:X}.{:X}'.format(ver[0],ver[2]),
			'SNVS'			: snvs_info,
			'Entries'		: MSG_SNVS_ENTRIES.format(len(SNVS.getLastDataEntries()), SNVS.getLastDataBlockOffset(True)),
			'Patchable'		: MSG_NO if isSysconPatchable(entries) == 0 else MSG_PROBABLY
		}
	
	showTable(info)
	
	return True

#==============================================================
# Common
#==============================================================

def launchTool(fname):
	
	if os.path.isdir(fname):
		return screenBuildNorDump(fname)
	
	f_size = os.stat(fname).st_size
	
	if f_size == NOR_DUMP_SIZE:
		return screenNorTools(fname)
	elif f_size == SYSCON_DUMP_SIZE:
		return screenSysconTools(fname)
	else:
		setStatus(MSG_UNK_FILE_TYPE + ' {}'.format(fname))
		return screenFileSelect()



def screenFileSelect(fname = ''):
	
	if len(fname) and os.path.exists(fname):
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
	
	try:
		choice = int(input(MSG_CHOICE))
		if 1 <= choice <= len(files):
			launchTool(os.getcwd() + os.sep + files[choice - 1])
		else:
			setStatus(MSG_ERROR_CHOICE)
	except:
		setStatus(MSG_ERROR_INPUT)
	
	screenFileSelect()



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