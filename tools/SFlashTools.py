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



def screenSBpatcher(file, model = '', emc_ver = '', eap_ver = ''):
	
	# Read once
	
	with open(file,'rb') as f:
		active_slot = SFlash.getActiveSlot(f)
		fw = SFlash.getFWInfo(f, active_slot)
		sb = SFlash.getSouthBridge(f)

	while True:
	
		UI.clearScreen()
		print(TITLE + UI.getTab(STR_ABOUT_SB_PATCH))
		print(UI.warning(STR_INFO_SB_PATCH))
		print()
		print(UI.warning(STR_INFO_FW_LINK))
		
		print(UI.getTab(STR_SB_PATCHER))
		
		print(UI.highlight(STR_CURRENT))
		print()
		UI.showTable({
			'Southbridge'	: '%s [%s] [%02X:%02X]'%(sb['name'], sb['ic'], sb['code'][0], sb['code'][1]),
			'FW info'		: fw['c'] + ' ['+active_slot.upper()+']',
		})
		
		print()
		
		if model in SFlash.SOUTHBRIDGES:
			print(UI.highlight(STR_MODEL+': ') + '%s [%s] [%02X:%02X]'%(model['name'], model['ic'], model['code'][0], model['code'][1]))
		else:
			print(UI.highlight(STR_SELECT_MODEL)+'\n')
			sb_list = SFlash.SOUTHBRIDGES
			UI.showMenu(['%s [%02X:%02X] %s'%(sb_list[x]['ic'], sb_list[x]['code'][0], sb_list[x]['code'][1], sb_list[x]['name']) for x in range(len(sb_list))], 1)
			
			UI.showStatus()
			
			choice = input(STR_CHOICE)

			if choice == '':
				break

			try: n = int(choice)
			except: n = -1
			
			if n > 0 and n <= len(SFlash.SOUTHBRIDGES):
				model = SFlash.SOUTHBRIDGES[n-1]
			else:
				UI.setStatus(STR_ERROR_INPUT)
			
			continue
		
		print()
		
		expert_mode = False
		if not emc_ver:
			expert_mode = input(UI.highlight(STR_EXPERT_MODE+STR_Y_OR_CANCEL)).lower()
			UI.clearInput()
		
		# Quick mode
		if not emc_ver and expert_mode != 'y':
			emc_ver = SFlash.getDataByPartitionAndType('emc_ipl', model['code'][0], fw['c'])
			eap_ver = SFlash.getDataByPartitionAndType('eap_kbl', model['code'][1], fw['c'])
			
			if not emc_ver:
				print(UI.error(STR_ERR_NO_FW_FOUND%('EMC',fw['c'])))
			if not eap_ver:
				print(UI.error(STR_ERR_NO_FW_FOUND%('EAP',fw['c'])))
			
			if emc_ver and eap_ver:
				continue
			else:
				model, emc_ver, eap_ver = '','',''
				print(UI.highlight(STR_USE_EXPERT_M))
				input(STR_BACK)
				continue
		
		# Expert mode
		if emc_ver:
			print(UI.highlight(' EMC:') + ' %s - %s [%s]\n'%(emc_ver['fw'][0], emc_ver['fw'][-1], emc_ver['md5']))
		else:
			print(UI.highlight(STR_SELECT_FW_VER+' (emc):')+'\n')
			
			items = SFlash.getDataByPartitionAndType('emc_ipl', model['code'][0])
			for x in range(len(items)):
				str = ' %2d: %05s <> %05s [%s]'%(x+1, items[x]['fw'][0], items[x]['fw'][-1], items[x]['md5'])
				print(UI.highlight(str) if SFlash.isFwInList(fw['c'], items[x]['fw']) else str)
			
			print(UI.DIVIDER+' 0:'+STR_GO_BACK)
			UI.showStatus()

			try: n = int(input(STR_CHOICE))
			except: n = -1
			
			if n == 0:
				model, emc_ver, eap_ver = '','',''
				continue
			if n > 0 and n <= len(items):
				emc_ver = items[n-1]
			else:
				UI.setStatus(STR_ERROR_INPUT)
			
			continue
		
		if eap_ver:
			print(UI.highlight(' EAP:') + ' %s - %s [%s]\n'%(eap_ver['fw'][0], eap_ver['fw'][-1], eap_ver['md5']))
		else:
			print(UI.highlight(STR_SELECT_FW_VER+' (eap):')+'\n')
			
			items = SFlash.getDataByPartitionAndType('eap_kbl', model['code'][1])
			for x in range(len(items)):
				str = ' %2d: %05s <> %05s [%s]'%(x+1, items[x]['fw'][0], items[x]['fw'][-1], items[x]['md5'])
				print(UI.highlight(str) if SFlash.isFwInList(fw['c'], items[x]['fw']) else str)
			
			print(UI.DIVIDER+' 0:'+STR_GO_BACK)
			UI.showStatus()
			
			try: n = int(input(STR_CHOICE))
			except: n = -1
			
			if n == 0:
				emc_ver, eap_ver = '',''
				continue
			if n > 0 and n <= len(items):
				eap_ver = items[n-1]
			else:
				UI.setStatus(STR_ERROR_INPUT)
			
			continue
		
		# Process
		if emc_ver and eap_ver:
			emc_file = SFlash.getFwFilename(emc_ver, (os.path.sep).join([ Utils.ROOT_PATH, 'fws', 'emc', '%02X'%model['code'][0] ]))
			eap_file = SFlash.getFwFilename(eap_ver, (os.path.sep).join([ Utils.ROOT_PATH, 'fws', 'eap', '%02X'%model['code'][1] ]))
			
			if os.path.exists(emc_file) and os.path.exists(eap_file):
				out_file = Utils.getFilePathWoExt(file, True)+'_patch_sb_'+model['ic']+'.bin'
				Utils.savePatchData(out_file, Utils.getFileContents(file), [
					{'o':SFlash.SFLASH_PARTITIONS['s0_emc_ipl_'+active_slot.lower()]['o'], 'd':Utils.getFileContents(emc_file)},
					{'o':SFlash.SFLASH_PARTITIONS['s0_eap_kbl']['o'], 'd':Utils.getFileContents(eap_file)},
				])
				UI.setStatus(STR_SAVED_TO%out_file)
			else:
				status = ' '+Utils.ROOT_PATH+'\n'
				if not os.path.exists(emc_file): status += ' '+emc_file[len(Utils.ROOT_PATH):]+'\n'
				if not os.path.exists(eap_file): status += ' '+eap_file[len(Utils.ROOT_PATH):]+'\n'
				status += ' ' + STR_NOT_FOUND
				UI.setStatus(status)
		
		UI.showStatus()
		input(STR_BACK)
		break



def screenWFpatcher(file, model = '', ver = ''):
	
	# Read once
	
	with open(file,'rb') as f:
		active_slot = SFlash.getActiveSlot(f)
		fw = SFlash.getFWInfo(f, active_slot)
		torus = SFlash.getTorusInfo(f)
	
	while True:

		UI.clearScreen()
		print(TITLE + UI.getTab(STR_ABOUT_TORUS_PATCH))
		print(UI.warning(STR_INFO_TORUS_PATCH))
		print()
		print(UI.warning(STR_INFO_FW_LINK))
		
		print(UI.getTab(STR_WIFI_PATCHER))
		
		print(UI.highlight(STR_CURRENT))
		print()
		
		UI.showTable({
			'Torus (WiFi+BT)'	: '%s - %s [0x%02X]'%(torus['v'], torus['name'], torus['code']),
			'FW info'			: fw['c'] + ' ['+active_slot.upper()+']',
		})
		print()
		
		if model in SFlash.TORUS_VERS:
			print(UI.highlight(STR_MODEL+': ') + '%s - %s [%02X]'%(model['v'], model['name'], model['code']))
		else:
			print(UI.highlight(STR_SELECT_MODEL)+'\n')
			tor_models = SFlash.TORUS_VERS
			UI.showMenu(['%s - %s [0x%02X] %s'%(tor_models[x]['v'], tor_models[x]['name'][:15], tor_models[x]['code'], ', '.join(tor_models[x]['ic'])) for x in range(len(SFlash.TORUS_VERS))], 1)
			
			UI.showStatus()
			
			choice = input(STR_CHOICE)

			if choice == '':
				break

			try: n = int(choice)
			except: n = -1

			if n > 0 and n <= len(SFlash.TORUS_VERS):
				model = SFlash.TORUS_VERS[n-1]
			else:
				UI.setStatus(STR_ERROR_INPUT)
			
			continue
		
		print()
		
		# Quick mode
		expert_mode = False
		if not ver:
			expert_mode = input(UI.highlight(STR_EXPERT_MODE+STR_Y_OR_CANCEL)).lower()
			UI.clearInput()
		
		if not ver and expert_mode != 'y':
			ver = SFlash.getDataByPartitionAndType('wifi', model['code'], fw['c'])
			
			if not ver:
				print(UI.error(STR_ERR_NO_FW_FOUND%('TORUS',fw['c'])))
				print(UI.highlight(STR_USE_EXPERT_M))
				input(STR_BACK)
				model, ver = '',''
			
			continue
		
		# Expert mode
		if ver:
			print(UI.highlight(' TORUS: ') + '%s - %s [%s]\n'%(ver['fw'][0], ver['fw'][-1], ver['md5']))
			
			fw_file = SFlash.getFwFilename(ver, (os.path.sep).join([ Utils.ROOT_PATH, 'fws', 'torus', '%02X'%model['code'] ]))

			if os.path.exists(fw_file):
				out_file = Utils.getFilePathWoExt(file, True)+'_patch_torus_'+'%02X'%model['code']+'.bin'
				Utils.savePatchData(out_file, Utils.getFileContents(file), [{'o':SFlash.SFLASH_PARTITIONS['s0_wifi']['o'], 'd':Utils.getFileContents(fw_file)}])
				UI.setStatus(STR_SAVED_TO%out_file)
			else:
				UI.setStatus(' %s - %s'%(fw_file, STR_NOT_FOUND))
		else:
			print(UI.highlight(STR_SELECT_FW_VER)+':\n')
			
			items = SFlash.getDataByPartitionAndType('wifi', model['code'])
			for x in range(len(items)):
				str = ' %2d: %05s <> %05s [%s]'%(x+1, items[x]['fw'][0], items[x]['fw'][-1], items[x]['md5'])
				print(UI.highlight(str) if SFlash.isFwInList(fw['c'], items[x]['fw']) else str)
			
			print(UI.DIVIDER+' 0:'+STR_GO_BACK)
			UI.showStatus()
			
			try: n = int(input(STR_CHOICE))
			except: n = -1
			
			if n == 0:
				return screenWFpatcher(file)
			if n > 0 and n <= len(items):
				ver = items[n-1]
			else:
				UI.setStatus(STR_ERROR_INPUT)
			
			continue
		
		UI.showStatus()
		input(STR_BACK)
		break
	
	return



def screenSysFlags(file):
	UI.clearScreen()
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
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_WARNING))
	
	print(UI.warning(STR_OVERCLOCKING))
	
	print(UI.getTab(STR_MEMCLOCK))
	
	with open(file, 'r+b') as f:
		
		clocks = SFlash.getMemClock(f)
		
		print(STR_CURRENT+('0x%02X %dMHz | 0x%02X %dMHz')%(clocks[0],clocks[1],clocks[2],clocks[3]))
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
		
		UI.setStatus(STR_MEMCLOCK_SET%(frq,raw))



def screenSamuBoot(file):
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_SAMU_BOOT))
	
	with open(file, 'r+b') as f:
		
		cur = SFlash.getNorData(f, 'SAMUBOOT')[0]
		print(STR_CURRENT+('%d [0x%02X]')%(cur,cur))
		
		try:
			frq = int(input(STR_SAMU_INPUT))
		except:
			return
		
		if frq < 0 or frq > 255:
			frq = 255
		
		SFlash.setNorData(f, 'SAMUBOOT',  frq.to_bytes(1, 'big'))
		SFlash.setNorDataB(f, 'SAMUBOOT', frq.to_bytes(1, 'big'))
	
	UI.setStatus(STR_SAMU_UPD+('%d [0x%02X]')%(frq,frq))



def screenLegitimatePatch(file, path = ''):
	
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_ABOUT_LEG_PATCH))
	print(UI.warning(STR_INFO_LEG_PATCH))
	print(UI.getTab(STR_LEG_PATCH))
	
	print(' '+UI.highlight(STR_LP_FIRST_DUMP)+':\n')
	with open(file, 'rb') as f:
		data = f.read()
		f_info = SFlash.getInfoForLegitSwitch(f)
		UI.showTable({
			'File'		: os.path.basename(file),
			'Date'		: Utils.getFileTime(file)['date'],
			'Slot'		: 'A' if f_info['slot'] == b'\x00' else 'B',
			'SN'		: f_info['sn'],
			'Pattern'	: UI.highlight(Utils.hex(f_info['switch'],':')),
		})
		print()
	
	if not path or not os.path.isfile(path):
		c = input(STR_INPUT_SEL_DUMP+STR_Y_OR_CANCEL)
		if c.lower() == 'y':
			path = Tools.screenFileSelect(file, False, True)
			return screenLegitimatePatch(file, path)
		else:
			return
	
	print(' '+UI.highlight(STR_LP_SECOND_DUMP)+':\n')
	with open(path, 'rb') as f:
		s_info = SFlash.getInfoForLegitSwitch(f)
		UI.showTable({
			'File'		: os.path.basename(path),
			'Date'		: Utils.getFileTime(path)['date'],
			'Slot'		: 'A' if s_info['slot'] == b'\x00' else 'B',
			'SN'		: s_info['sn'],
			'Pattern'	: UI.highlight(Utils.hex(s_info['switch'],':')),
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
	Utils.savePatchData(ofile, data, [
		{'o':SFlash.SFLASH_AREAS['CORE_SWCH']['o'],					'd':s_info['switch']},
		{'o':SFlash.SFLASH_AREAS['UART']['o'],							'd':b'\x01'},
		{'o':SFlash.SFLASH_AREAS['UART']['o']+SFlash.BACKUP_OFFSET,	'd':b'\x01'},
	])
	
	print(STR_PATCH_SAVED%ofile)
	
	c = input('\n'+UI.highlight(STR_FLASH_FILE+STR_Y_OR_CANCEL)).lower()
	if c == 'y':
		return Tools.screenNorFlasher(ofile if ofile else file, '', 'write', 1)
	
	input(STR_BACK)



def screenDowngrade(file):
	UI.clearScreen()
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
			c = input('\n'+UI.highlight(STR_CONFIRM_SEPARATE+STR_Y_OR_CANCEL)).lower()
			
			if c == 'y':
				ofile = os.path.splitext(file)[0]+'_slot_switch_'+str(num)+'.bin'
				f.seek(0,0)
				patch = [
					{'o':SFlash.SFLASH_AREAS['CORE_SWCH']['o'],					'd':bytes(pattern['v'])},
					{'o':SFlash.SFLASH_AREAS['UART']['o'],							'd':b'\x01'},
					{'o':SFlash.SFLASH_AREAS['UART']['o']+SFlash.BACKUP_OFFSET,	'd':b'\x01'},
				]
				Utils.savePatchData(ofile, f.read(), patch)
				UI.setStatus(STR_PATCH_SAVED%ofile)
			else:
				SFlash.setNorData(f, 'CORE_SWCH', bytes(pattern['v']))
				UI.setStatus(STR_DOWNGRADE_UPD + SFlash.SWITCH_TYPES[pattern['t']] + ' [' + str(num)+']')
			
			c = input('\n'+UI.highlight(STR_FLASH_FILE+STR_Y_OR_CANCEL)).lower()
			if c == 'y':
				return Tools.screenNorFlasher(ofile if ofile else file, '', 'write', 1)
	
	screenDowngrade(file)



def screenFlagsToggler(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_WARNING))
	
	print(UI.warning(STR_PATCHES))
	
	print(UI.getTab(STR_SFLASH_FLAGS))
	
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
			{'k':'ACT_SLOT',	'v':[b'\x00',b'\x80'],			'd':['A','B']},
			{'k':'RESOLUTION',	'v':[b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x13'],	'd':['Reset', '1080i', '720p', '1080p', '4K', '4K HDR', 'Auto']},
		]
		
		for i in range(len(patches)):
			name = SFlash.getNorAreaName(patches[i]['k'])
			val = SFlash.getNorData(f, patches[i]['k'])
			str = '['+Utils.hex(val,'')[:32]+']'
			for k in range(len(patches[i]['v'])):
				if val == patches[i]['v'][k]:
					str = patches[i]['d'][k]
			print(' %2d: %-24s : %s'%(i+1, name, str))
	
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
		patch = patches[num-1]
		k = toggleFlag(file, patch)
		if patch['k'] == 'RESOLUTION':
			SFlash.setNorData(file, 'RES_RESET', b'\x01' if patch['v'][k] == b'\x00' else b'\x00')
	
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
	
	UI.setStatus(STR_SET_TO%(SFlash.getNorAreaName(patch['k']),patch['d'][i]))
	
	return i



def screenPartitionsInfo(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_PARTS_INFO))
	
	with open(file,'rb') as f:
		data = SFlash.getPartitionsInfo(f)
		slot = 'A' if data['slot'] == b'\x00' else 'B'
		print(STR_ACT_SLOT%(slot, data['slot'][0]))
		print()
		for i in range(len(data['parts'])):
			p = data['parts'][i]
			print(UI.highlight(' #%d %s'%(i+1, p['name'])))
			UI.showTable({
				'Offset':'%8d [0x%x]'%(p['offset'],p['offset']),
				'Size':'%8d [0x%x]'%(p['size'],p['size']),
				'Type':'%8d [0x%x]'%(p['type'],p['type']),
			})
			print()
	
	choice = input(STR_CHOICE)



def screenSFlashTools(file):
		
	while True:
			
		UI.clearScreen()
		print(TITLE+UI.getTab(STR_SFLASH_INFO))
		
		info = SFlash.getSFlashInfo(file)
		if info:
			UI.showTable(info)
		else:
			return Tools.screenFileSelect(file)
		
		print(UI.getTab(STR_ACTIONS))
		
		UI.showMenu(MENU_SFLASH_ACTIONS,1)
		print(UI.DIVIDER)
		UI.showMenu(MENU_EXTRA)
		
		UI.showStatus()
		
		choice = input(STR_CHOICE)
	
		if choice == 's':
			Tools.screenFileSelect(file)
			break
		elif choice == 'f':
			Tools.screenNorFlasher(file)
			break
		elif choice == 'r':
			file = renameToCanonnical(file)
			continue
		elif choice == 'q':
			break

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
			screenSBpatcher(file)
		elif choice == '7':
			screenWFpatcher(file)
		elif choice == '8':
			AdvSFlashTools.screenAdvSFlashTools(file)
	
		

def renameToCanonnical(file):
	fpath = os.path.realpath(file)
	new_name = SFlash.getCanonicalName(file)
	if new_name:
		new_fpath = os.path.join(os.path.dirname(fpath), new_name + '.bin')
		if not os.path.exists(new_fpath):
			os.rename(fpath, new_fpath)
			file = new_fpath
			UI.setStatus(STR_RENAMED%new_name)
			return new_fpath
		else:
			UI.setStatus(STR_FILE_EXISTS)
	return file
