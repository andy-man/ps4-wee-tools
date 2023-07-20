#==============================================================
# PS4 Nor Tools
# part of ps4 wee tools project
#==============================================================
import os
from lang._i18n_ import *
from utils.nor import *
import data.data as Data
import utils.slb2 as Slb2
import utils.encdec as Encdec
import tools.Tools as Tools
import tools.AdvNorTools as AdvNorTools



def screenSysFlags(file):
	os.system('cls')
	print(TITLE + getTab(STR_SYSFLAGS))
	
	with open(file, 'r+b') as f:
		
		print(warning(STR_CURRENT)+'\n')
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
	print(TITLE + getTab(STR_WARNING))
	
	print(warning(STR_OVERCLOCKING))
	
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
	print(TITLE + getTab(STR_COREOS_SWITCH))
	
	print(warning(STR_DOWNGRADE))
	
	with open(file, 'r+b') as f:
		
		print('\n'+STR_CURRENT+getSlotSwitchInfo(f))
		
		print(getTab(STR_SWITCH_PATTERNS),end='')
		
		for i in range(1, len(SWITCH_TYPES)):
			print('\n '+SWITCH_TYPES[i]+'\n')
			for n in range(len(SWITCH_BLOBS)):
				if SWITCH_BLOBS[n]['t'] == i:
					print(' %2d: %s'%(n+1,getHex(SWITCH_BLOBS[n]['v'])))
		
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
				patch = [
					{'o':NOR_AREAS['CORE_SWCH']['o'],	'd':bytes(pattern['v'])},
					{'o':NOR_AREAS['UART']['o'],		'd':b'\x01'},
				]
				savePatchData(ofile, f.read(), patch);
				setStatus(STR_PATCH_SAVED.format(ofile))
			else:
				setNorData(f, 'CORE_SWCH', bytes(pattern['v']))
				setStatus(STR_DOWNGRADE_UPD + SWITCH_TYPES[pattern['t']] + ' [' + str(choice)+']')
	
	screenDowngrade(file)



def screenFlagsToggler(file):
	os.system('cls')
	print(TITLE+getTab(STR_WARNING))
	
	print(warning(STR_PATCHES))
	
	print(getTab(STR_NOR_FLAGS))
	
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



def screenNorTools(file):
	os.system('cls')
	print(TITLE+getTab(STR_NOR_INFO))
	
	info = getNorInfo(file)
	if info:
		showTable(info)
	else:
		return Tools.screenFileSelect(file)
	
	print(getTab(STR_ACTIONS))
	getMenu(MENU_NOR_ACTIONS)
	
	showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == '0':
		return Tools.screenFileSelect(file)
	elif choice == '1':
	    screenFlagsToggler(file)
	elif choice == '2':
	    screenMemClock(file)
	elif choice == '3':
	    screenSamuBoot(file)
	elif choice == '4':
		screenDowngrade(file)
	elif choice == '5':
		AdvNorTools.screenAdvNorTools(file)
	elif choice == '6':
	    quit()
	
	screenNorTools(file)



def getNorInfo(file = '-'):
	if not checkFileSize(file, NOR_DUMP_SIZE):
		return False
	
	with open(file, 'rb') as f:
		
		sku = getNorData(f, 'SKU').decode('utf-8','ignore')
		
		fw = getNorFW(f)
		
		active_slot = 'a' if getNorData(f, 'ACT_SLOT')[0] == 0x00 else 'b'
		inactive_slot = 'a' if active_slot == 'b' else 'b'
		
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
			'FW (active)'	: fw['c'] + ' ['+active_slot.upper()+']' + (' [min '+fw['min']+']' if fw['min'] else ''),
			'FW (backup)'	: '',
			'GDDR5'			: ('0x{:02X} {:d}MHz | 0x{:02X} {:d}MHz').format(*getMemClock(f)),
			'SAMU BOOT'		: ('{:d} [0x{:02X}]').format(samu,samu),
			'UART'			: (STR_ON if getNorData(f, 'UART')[0] == 1 else STR_OFF),
			'Slot switch'	: getSlotSwitchInfo(f),
		}
		
		md5 = getNorPartitionMD5(f, 's0_emc_ipl_'+inactive_slot)
		if md5 in Data.EMC_IPL_MD5:
			fw2 = Data.EMC_IPL_MD5[md5]['fw']
			info['FW (backup)'] = (fw2[0] if len(fw2) == 1 else fw2[0]+' <-> '+fw2[-1])
	
	return info
