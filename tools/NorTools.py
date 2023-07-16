#==============================================================
# PS4 Nor Tools
# part of ps4 wee tools project
#==============================================================
import os
from lang._i18n_ import *
from utils.nor import *
from utils.hdd_eap import getHddEapKey



def screenSysFlags(file):
	os.system('cls')
	print(TITLE + getTab(STR_SYSFLAGS))
	
	with open(file, 'r+b') as f:
		
		print(STR_CURRENT+'\n'+DIVIDER_DASH)
		flags = getNorData(f, 'SYS_FLAGS')
		for i in range(0, len(flags), 0x10):
			print(' '+getHex(flags[i:i+0x10]))
		
		choice = input(STR_CONFIRM)
		
		if choice.lower() != 'y':
			return 0
		
		val = b'\xFF'*64
		setNorData(f, 'SYS_FLAGS',  val)
		setNorDataB(f, 'SYS_FLAGS', val)
	
	setStatus(STR_SYSFLAGS_CLEAN)



def screenMemClock(file):
	os.system('cls')
	print(TITLE + STR_OVERCLOCKING)
	print(getTab(STR_MEMCLOCK))
	
	with open(file, 'r+b') as f:
		
		clocks = getMemClock(f)
		
		print(STR_CURRENT+('0x{:02X} {:d}MHz | 0x{:02X} {:d}MHz').format(*clocks))
		if clocks[0] != clocks[2]:
			print(STR_DIFF_SLOT_VALUES)
		
		try:
		    frq = int(input(STR_MEMCLOCK_INPUT))
		except:
		    return
		
		if frq >= 400 and frq <= 2000:
		    raw = clockToRaw(frq)
		else:
			frq = 0
			raw = 255
		
		setNorData(f, 'MEMCLK',  raw.to_bytes(1, 'big'))
		setNorDataB(f, 'MEMCLK', raw.to_bytes(1, 'big'))
		
		setStatus(STR_MEMCLOCK_SET.format(frq,raw))



def screenSamuBoot(file):
	os.system('cls')
	print(TITLE + getTab(STR_SAMU_BOOT))
	
	with open(file, 'r+b') as f:
		
		cur = getNorData(f, 'SAMUBOOT')[0]
		print(STR_CURRENT+('{:d} [0x{:02X}]').format(cur,cur))
		
		try:
		    frq = int(input(STR_SAMU_INPUT))
		except:
		    return
		
		if frq < 0 or frq > 255:
		    frq = 255
		
		setNorData(f, 'SAMUBOOT',  frq.to_bytes(1, 'big'))
		setNorDataB(f, 'SAMUBOOT', frq.to_bytes(1, 'big'))
	
	setStatus(STR_SAMU_UPD+('{:d} [0x{:02X}]').format(frq,frq))



def screenDowngrade(file):
	os.system('cls')
	print(TITLE + STR_DOWNGRADE)
	
	with open(file, 'r+b') as f:
		
		print(STR_CURRENT+getSlotSwitchInfo(f))
		
		print(getTab(STR_DOWNGRADE),end='')
		
		for i in range(1, len(SWITCH_TYPES)):
			print('\n '+SWITCH_TYPES[i]+'\n')
			for n in range(len(SWITCH_BLOBS)):
				if SWITCH_BLOBS[n]['t'] == i:
					print('  '+str(n+1)+': '+getHex(SWITCH_BLOBS[n]['v']))
		
		print(DIVIDER)
		print(' 0:'+STR_GO_BACK)
		
		showStatus()
		
		try:
			choice = int(input(STR_CHOICE))
		except:
			return
		
		if choice == 0:
			return
		elif choice < 0 or choice > len(SWITCH_BLOBS):
			setStatus(STR_ERROR_CHOICE)
		else:
			pattern = SWITCH_BLOBS[choice-1]
			
			c = input('\n'+STR_CONFIRM_SEPARATE)
			
			if c == 'y':
				ofile = os.path.splitext(file)[0]+'_slot_switch_'+str(choice)+'.bin'
				f.seek(0,0)
				savePatchData(ofile, f.read(), [{'o':NOR_AREAS['CORE_SWCH']['o'],'d':bytes(pattern['v'])}]);
				setStatus(STR_PATCH_SAVED.format(ofile))
			else:
				setNorData(f, 'CORE_SWCH', bytes(pattern['v']))
				setStatus(STR_DOWNGRADE_UPD + SWITCH_TYPES[pattern['t']] + ' [' + str(choice)+']')
	
	screenDowngrade(file)



def screenFlagsToggler(file):
	os.system('cls')
	print(TITLE + STR_PATCHES + getTab(STR_NOR_FLAGS))
	
	with open(file, 'rb') as f:
		
		patches = [
			{'k':'UART',	'v':[b'\x00',b'\x01'], 'd':[STR_OFF,STR_ON]},
			{'k':'MEMTEST',	'v':[b'\x00',b'\x01'], 'd':[STR_OFF,STR_ON]},
			{'k':'RNG_KEY',	'v':[b'\x00',b'\x01'], 'd':[STR_OFF,STR_ON]},
			{'k':'BTNSWAP',	'v':[b'\x00',b'\x01'], 'd':['O - select','X - select']},
			{'k':'SLOW_HDD','v':[b'\xFF',b'\xFE'], 'd':[STR_OFF,STR_ON]},
			{'k':'MEM_BGM',	'v':[b'\xFE',b'\xFF'], 'd':['Large','Normal']},
			{'k':'SAFE_BOOT','v':[b'\xFF',b'\x01'], 'd':[STR_OFF,STR_ON]},
			{'k':'UPD_MODE','v':[b'\x00',b'\x10'], 'd':[STR_OFF,STR_ON]},
			{'k':'ARCADE',	'v':[b'\x00',b'\x01'], 'd':[STR_OFF,STR_ON]},
			{'k':'REG_REC',	'v':[b'\x00',b'\x01'], 'd':[STR_OFF,STR_ON]},
			{'k':'IDU',		'v':[b'\x00',b'\x01'], 'd':[STR_OFF,STR_ON]},
			{'k':'BOOT_MODE','v':[b'\xFE',b'\xFB',b'\xFF'], 'd':['Development','Assist','Release']},
			{'k':'MANU',	'v':[b'\x00'*32,b'\xFF'*32], 'd':[STR_OFF,STR_ON]},
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
	print(' c:'+STR_CLEAN_FLAGS)
	print(' 0:'+STR_GO_BACK)
	
	showStatus()
	
	num = -1
	try:
		choice = input(STR_CHOICE)
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
	
	setStatus(STR_SET_TO.format(getNorAreaName(patch['k']),patch['d'][i]))



def screenValidate(file):
	os.system('cls')
	print(TITLE + getTab(STR_NOR_VALIDATOR) + '\n' + STR_WAIT)
	
	stats = entropy(file)
	
	os.system('cls')
	print(TITLE+getTab(STR_ENTROPY))
	
	info = {
		'Entropy': '{:.5f}'.format(stats['ent']),
		'0xFF': '{:.2f}%'.format(stats['ff']*100),
		'0x00': '{:.2f}%'.format(stats['00']*100),
		'Other': '{:.2f}%'.format((1 - stats['ff'] - stats['00'])*100),
	}
	
	showTable(info)
	
	input(STR_BACK)



def screenNorTools(file):
	os.system('cls')
	print(TITLE+getTab(STR_NOR_INFO))
	
	if not showNorInfo(file):
		return screenFileSelect()
	
	print(getTab(STR_ACTIONS))
	getMenu(MENU_NOR_ACTIONS)
	
	showStatus()
	
	choice = input(STR_CHOICE)
	
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
	print(TITLE+getTab(STR_ADDITIONAL))
	
	with open(file, 'rb') as f:
		sn = getNorData(f, 'SN').decode('utf-8','ignore')
	
	folder = os.path.dirname(file) + os.sep + sn
	
	getMenu(MENU_ADDTIONAL,1)
	
	showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == '':
		return
	elif choice == '1':
		screenExtractNorDump(file)
	elif choice == '2':
		screenBuildNorDump(folder)
	elif choice == '3':
		screenHddKey(file)
	elif choice == '4':
		screenValidate(file)
	
	screenAdditionalTools(file)



def screenHddKey(file):
	os.system('cls')
	print(TITLE+STR_INFO_HDD_EAP+'\n')
	
	mode = input(STR_USE_NEWBLOBS)
	
	print(getTab(STR_HDD_KEY))
	getHddEapKey(file, True if mode == 'y' else False)
	
	input(STR_BACK)



def screenExtractNorDump(file):
	os.system('cls')
	print(TITLE+getTab(STR_NOR_EXTRACT))
	
	with open(file, 'rb') as f:
		sn = getNorData(f, 'SN').decode('utf-8','ignore')
		folder = os.path.dirname(file) + os.sep + sn + os.sep
		
		if not os.path.exists(folder):
			os.makedirs(folder)
		
		print(STR_EXTRACTING.format(sn)+'\n')
		
		i = 0
		for k in NOR_PARTITIONS:
			p = NOR_PARTITIONS[k]
			i += 1
			print(' {:2d}: {:16s} > {}'.format(i, k, p['n']))
			
			with open(folder + p['n'],'wb') as out:
				out.write(getData(f, p['o'], p['l']))
		
		print('\n'+STR_SAVED_TO.format(folder))
	
	print('\n'+STR_DONE)
	
	input(STR_BACK)



def screenBuildNorDump(folder):
	os.system('cls')
	print(TITLE+getTab(STR_NOR_BUILD))
	
	if not os.path.exists(folder):
		print(STR_NO_FOLDER.format(folder)+'\n\n'+STR_ABORT)
		input(STR_BACK)
		return
	
	print(STR_FILES_CHECK.format(folder)+'\n')
	
	found = 0
	
	i = 0
	for k in NOR_PARTITIONS:
		p = NOR_PARTITIONS[k]
		i += 1
		status = STR_OK
		
		file = folder+os.sep+p['n']
		if not os.path.exists(file):
			status = STR_NOT_FOUND
		elif os.stat(file).st_size != p['l']:
			status = STR_BAD_SIZE
		else:
			found += 1
		
		print(' {:2d}: {:20s} - {}'.format(i, p['n'], status))
	
	print()
	
	if found == len(NOR_PARTITIONS):
		
		sn = '0'*17
		with open(folder+os.sep+NOR_PARTITIONS['s0_nvs']['n']) as nvs:
			nvs.seek(0x4030)
			sn = nvs.read(17)
		
		fname = os.path.dirname(folder) + os.sep + sn + '.bin'
		
		print(STR_BUILDING.format(fname))
		
		out = open(fname,"wb")
		
		for k in NOR_PARTITIONS:
			file = folder+os.sep+NOR_PARTITIONS[k]['n']
			with open(file, 'rb') as f:
				out.write(f.read())
		
		out.close()
		
		print('\n'+STR_DONE)
	else:
		print(STR_ABORT)
	
	input(STR_BACK)



def showNorInfo(file = '-'):
	if not checkFileSize(file, NOR_DUMP_SIZE):
		return False
	
	with open(file, 'rb') as f:
		
		sku = getNorData(f, 'SKU').decode('utf-8','ignore')
		
		old_fw = getNorData(f, 'FW_V')
		
		fw = getNorData(f, 'FW_VER') if old_fw[0] == 0xFF else old_fw
		fw = '{:X}.{:02X} '.format(fw[1], fw[0])
		ffw = getNorData(f, 'FW_EXP')
		ffw = '[min {:X}.{:02X}] '.format(ffw[1], ffw[0]) if ffw[0] != 0xFF else ''
		
		samu_ipl_a = getNorPartition(f, 's1_samu_ipl_a')
		samu_ipl_b = getNorPartition(f, 's1_samu_ipl_b')
		
		ipl_eq = 'IPL:EQ' if samu_ipl_a == samu_ipl_b else 'IPL:DIFF'
		
		southbridge = getSouthBridge(f)
		torus = getTorusVersion(f)
		
		samu = getNorData(f, 'SAMUBOOT')[0]
		region = getConsoleRegion(f)
		
		try:
			hdd = (' / ').join(swapBytes(getNorData(f, 'HDD')).decode('utf-8').split())
		except:
			hdd = STR_NO_INFO
		
		info = {
			'FILE'			: os.path.basename(file),
			'MD5'			: getFileMD5(file),
			'SKU'			: sku,
			'Region'		: '[{}] {}'.format(region[0], region[1]),
			'SN / Mobo SN'	: getNorData(f, 'SN').decode('utf-8','ignore')+' / '+getNorData(f, 'MB_SN').decode('utf-8','ignore'),
			'Southbridge'	: southbridge if southbridge else STR_UNKNOWN,
			'Torus (WiFi)'	: torus if len(torus) else STR_UNKNOWN,
			'MAC'			: getHex(getNorData(f, 'MAC'),':'),
			'HDD'			: hdd,
			'FW'			: fw + ffw + ipl_eq,
			'GDDR5'			: ('0x{:02X} {:d}MHz | 0x{:02X} {:d}MHz').format(*getMemClock(f)),
			'SAMU BOOT'		: ('{:d} [0x{:02X}]').format(samu,samu),
			'UART'			: (STR_ON if getNorData(f, 'UART')[0] == 1 else STR_OFF),
			'Slot switch'	: getSlotSwitchInfo(f)
		}
	
	showTable(info)
	
	return True
