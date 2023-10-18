#==============================================================
# PS4 Nor Tools
# part of ps4 wee tools project
#==============================================================
import os, time
from lang._i18n_ import *
import utils.utils as Utils
import utils.sflash as SFlash
import utils.slb2 as Slb2
import utils.encdec as Encdec
import tools.Tools as Tools
import tools.AdvSFlashTools as AdvSFlashTools


def screenSysFlags(file):
	os.system('cls')
	print(TITLE + UI.getTab(STR_SYSFLAGS))
	
	with open(file, 'r+b') as f:
		
		print(UI.warning(STR_CURRENT)+'\n')
		flags = SFlash.getNorData(f, 'SYS_FLAGS')
		for i in range(0, len(flags), 0x10):
			print(' '+Utils.hex(flags[i:i+0x10]))
		
		choice = input(STR_CONFIRM)
		
		if choice.lower() != 'y':
			return 0
		
		val = b'\xFF'*64
		SFlash.setNorData(f, 'SYS_FLAGS',  val)
		SFlash.setNorDataB(f, 'SYS_FLAGS', val)
	
	UI.setStatus(STR_SYSFLAGS_CLEAN)



def screenMemClock(file):
	os.system('cls')
	print(TITLE + UI.getTab(STR_WARNING))
	
	print(UI.warning(STR_OVERCLOCKING))
	
	print(UI.getTab(STR_MEMCLOCK))
	
	with open(file, 'r+b') as f:
		
		clocks = SFlash.getMemClock(f)
		
		print(STR_CURRENT+('0x{:02X} {:d}MHz | 0x{:02X} {:d}MHz').format(*clocks))
		if clocks[0] != clocks[2]:
			print(STR_DIFF_SLOT_VALUES)
		
		try:
		    frq = int(input(STR_MEMCLOCK_INPUT))
		except:
		    return
		
		if frq >= 400 and frq <= 2000:
		    raw = SFlash.clockToRaw(frq)
		else:
			frq = 0
			raw = 255
		
		SFlash.setNorData(f, 'MEMCLK',  raw.to_bytes(1, 'big'))
		SFlash.setNorDataB(f, 'MEMCLK', raw.to_bytes(1, 'big'))
		
		UI.setStatus(STR_MEMCLOCK_SET.format(frq,raw))



def screenSamuBoot(file):
	os.system('cls')
	print(TITLE + UI.getTab(STR_SAMU_BOOT))
	
	with open(file, 'r+b') as f:
		
		cur = SFlash.getNorData(f, 'SAMUBOOT')[0]
		print(STR_CURRENT+('{:d} [0x{:02X}]').format(cur,cur))
		
		try:
		    frq = int(input(STR_SAMU_INPUT))
		except:
		    return
		
		if frq < 0 or frq > 255:
		    frq = 255
		
		SFlash.setNorData(f, 'SAMUBOOT',  frq.to_bytes(1, 'big'))
		SFlash.setNorDataB(f, 'SAMUBOOT', frq.to_bytes(1, 'big'))
	
	UI.setStatus(STR_SAMU_UPD+('{:d} [0x{:02X}]').format(frq,frq))



def screenLegitimatePatch(file, path = ''):
	
	os.system('cls')
	print(TITLE+UI.getTab(STR_ABOUT_LEG_PATCH))
	print(UI.warning(STR_INFO_LEG_PATCH))
	print(UI.getTab(STR_LEG_PATCH))
	
	print(' '+UI.highlight('First dump')+':\n')
	with open(file, 'rb') as f:
		data = f.read()
		f_info = SFlash.getInfoForLegitSwitch(f)
		UI.showTable({
			'File': os.path.basename(file),
			'Date': Utils.getFileTime(file)['date'],
			'Slot': 'A' if f_info['slot'] == b'\x00' else 'B',
			'SN': f_info['sn'],
			'Pattern': UI.highlight(Utils.hex(f_info['switch'],':')),
		})
		print()
	
	if not path or not os.path.isfile(path):
		c = input(' Select second dump [y]? or exit [ENTER] ')
		if c.lower() == 'y':
			path = Tools.screenFileSelect(file, False, True)
			return screenLegitimatePatch(file, path)
		else:
			return
	
	print(' '+UI.highlight('Second dump')+':\n')
	with open(path, 'rb') as f:
		s_info = SFlash.getInfoForLegitSwitch(f)
		UI.showTable({
			'File': os.path.basename(path),
			'Date': Utils.getFileTime(path)['date'],
			'Slot': 'A' if s_info['slot'] == b'\x00' else 'B',
			'SN': s_info['sn'],
			'Pattern': UI.highlight(Utils.hex(s_info['switch'],':')),
		})
		print()
	
	# Quick check
	if f_info['sn'] != s_info['sn']:
		print(' '+UI.warning(STR_CANT_USE+': ')+STR_DIFF_SN)
		input(STR_BACK)
		return
		
	if f_info['switch'] == s_info['switch']:
		print(' '+UI.warning(STR_CANT_USE+': ')+STR_SSP_EQUAL)
		input(STR_BACK)
		return
	
	ofile = Utils.getFilePathWoExt(file)+'_legit_patch.bin'
	Utils.savePatchData(ofile, data, [{'o':SFlash.NOR_AREAS['CORE_SWCH']['o'], 'd':s_info['switch']}])
	
	print(STR_PATCH_SAVED.format(ofile))
	
	c = input('\n'+UI.highlight(STR_FLASH_PATCHED))
	if c.lower() == 'y':
		return Tools.screenNorFlasher(ofile if ofile else file, '', 'write', 1)
	
	input(STR_BACK)



def screenDowngrade(file):
	os.system('cls')
	print(TITLE + UI.getTab(STR_COREOS_SWITCH))
	print(UI.warning(STR_DOWNGRADE))
	
	with open(file, 'r+b') as f:
		print('\n'+STR_CURRENT+SFlash.getSlotSwitchInfo(f))
		print(UI.getTab(STR_SWITCH_PATTERNS),end='')
		
		for i in range(1, len(SFlash.SWITCH_TYPES)):
			print('\n '+SFlash.SWITCH_TYPES[i]+'\n')
			for n in range(len(SFlash.SWITCH_BLOBS)):
				if SFlash.SWITCH_BLOBS[n]['t'] == i:
					print(' %2d: %s'%(n+1,Utils.hex(SFlash.SWITCH_BLOBS[n]['v'])))
		
		print(UI.DIVIDER)
		print(' 0:'+STR_GO_BACK)
		
		UI.showStatus()
		
		try: num = int(input(STR_CHOICE))
		except: num = -1
		
		if num == 0:
			return
		elif num < 0 or num > len(SFlash.SWITCH_BLOBS):
			UI.setStatus(STR_ERROR_CHOICE)
		else:
			pattern = SFlash.SWITCH_BLOBS[num-1]
			ofile = ''
			c = input('\n'+UI.highlight(STR_CONFIRM_SEPARATE))
			
			if c == 'y':
				ofile = os.path.splitext(file)[0]+'_slot_switch_'+str(num)+'.bin'
				f.seek(0,0)
				patch = [
					{'o':SFlash.NOR_AREAS['CORE_SWCH']['o'],	'd':bytes(pattern['v'])},
					{'o':SFlash.NOR_AREAS['UART']['o'],			'd':b'\x01'},
				]
				Utils.savePatchData(ofile, f.read(), patch)
				UI.setStatus(STR_PATCH_SAVED.format(ofile))
			else:
				SFlash.setNorData(f, 'CORE_SWCH', bytes(pattern['v']))
				UI.setStatus(STR_DOWNGRADE_UPD + SFlash.SWITCH_TYPES[pattern['t']] + ' [' + str(num)+']')
			
			c = input('\n'+UI.highlight(STR_FLASH_PATCHED))
			if c == 'y':
				return Tools.screenNorFlasher(ofile if ofile else file, '', 'write', 1)
	
	screenDowngrade(file)



def screenFlagsToggler(file):
	os.system('cls')
	print(TITLE+UI.getTab(STR_WARNING))
	
	print(UI.warning(STR_PATCHES))
	
	print(UI.getTab(STR_NOR_FLAGS))
	
	with open(file, 'rb') as f:
		
		patches = [
			{'k':'UART',		'v':[b'\x00',b'\x01'],			'd':[STR_OFF,STR_ON], 'b':True},
			{'k':'MEMTEST',		'v':[b'\x00',b'\x01'],			'd':[STR_OFF,STR_ON], 'b':True},
			{'k':'RNG_KEY',		'v':[b'\x00',b'\x01'],			'd':[STR_OFF,STR_ON], 'b':True},
			{'k':'BTNSWAP',		'v':[b'\x00',b'\x01'],			'd':['O - select','X - select']},
			{'k':'SLOW_HDD',	'v':[b'\xFF',b'\xFE'],			'd':[STR_OFF,STR_ON]},
			{'k':'MEM_BGM',		'v':[b'\xFE',b'\xFF'],			'd':['Large','Normal']},
			{'k':'SAFE_BOOT',	'v':[b'\xFF',b'\x01'],			'd':[STR_OFF,STR_ON]},
			{'k':'UPD_MODE',	'v':[b'\x00',b'\x10'],			'd':[STR_OFF,STR_ON]},
			{'k':'ARCADE',		'v':[b'\x00',b'\x01'],			'd':[STR_OFF,STR_ON]},
			{'k':'REG_REC',		'v':[b'\x00',b'\x01'],			'd':[STR_OFF,STR_ON]},
			{'k':'IDU',			'v':[b'\x00',b'\x01'],			'd':[STR_OFF,STR_ON]},
			{'k':'BOOT_MODE',	'v':[b'\xFE',b'\xFB',b'\xFF'],	'd':['Development','Assist','Release']},
			{'k':'MANU',		'v':[b'\x00'*32,b'\xFF'*32],	'd':[STR_OFF,STR_ON]},
		]
		
		for i in range(len(patches)):
			name = SFlash.getNorAreaName(patches[i]['k'])
			val = SFlash.getNorData(f, patches[i]['k'])
			str = '['+Utils.hex(val,'')[:32]+']'
			for k in range(len(patches[i]['v'])):
				if val == patches[i]['v'][k]:
					str = patches[i]['d'][k]
			print(' {:2d}: {:24s}: {}'.format(i+1, name, str))
	
	print(UI.DIVIDER)
	
	print(' c:'+STR_CLEAN_FLAGS)
	print(' 0:'+STR_GO_BACK)
	
	UI.showStatus()
	
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
		
		cur = SFlash.getNorData(f, patch['k'])
		for i in range(0,len(patch['v'])):
			if cur == patch['v'][i]:
				break
		i = 0 if (i + 1) >= len(patch['v']) else i + 1
		val = patch['v'][i]
		
		SFlash.setNorData(f, patch['k'],  patch['v'][i])
		if 'b' in patch and patch['b'] == True:
			# Set flag in backup area
			SFlash.setNorDataB(f, patch['k'], patch['v'][i])
	
	UI.setStatus(STR_SET_TO.format(SFlash.getNorAreaName(patch['k']),patch['d'][i]))



def screenSFlashTools(file):
	os.system('cls')
	print(TITLE+UI.getTab(STR_NOR_INFO))
	
	info = SFlash.getSFlashInfo(file)
	if info:
		UI.showTable(info)
	else:
		return Tools.screenFileSelect(file)
	
	print(UI.getTab(STR_ACTIONS))
	
	UI.showMenu(MENU_NOR_ACTIONS,1)
	print(UI.DIVIDER)
	UI.showMenu(MENU_EXTRA)
	
	UI.showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == '1':
	    screenFlagsToggler(file)
	elif choice == '2':
	    screenMemClock(file)
	elif choice == '3':
	    screenSamuBoot(file)
	elif choice == '4':
		screenDowngrade(file)
	elif choice == '5':
		screenLegitimatePatch(file)
	elif choice == '6':
		AdvSFlashTools.screenAdvSFlashTools(file)
	
	elif choice == 's':
	    return Tools.screenFileSelect(file)
	elif choice == 'f':
		return Tools.screenNorFlasher(file)
	elif choice == 'm':
	    return Tools.screenMainMenu()
	
	screenSFlashTools(file)
