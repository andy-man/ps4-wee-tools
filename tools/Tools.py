#==============================================================
# Common Tools
# part of ps4 wee tools project
#==============================================================
import os, sys, time, datetime
from lang._i18n_ import *
from utils.serial import WeeSerial
from utils.spiway import SpiFlasher
import utils.utils as Utils
import utils.slb2 as Slb2
import utils.sflash as SFlash
import utils.syscon as Syscon
import utils.syscon_rw as SysconRW
import tools.SFlashTools as SFlashTools
import tools.SysconTools as SysconTools
import tools.AdvSFlashTools as AdvSFlashTools



def screenNorFlasher(path = '', port = '', act = '', mode = False):
	
	port = port if port else screenChoosePort()
	if not port:
		UI.setStatus(STR_NO_PORTS)
		return
	
	flasher = SpiFlasher(port)
	
	os.system('cls')
	print(TITLE+UI.getTab(STR_ABOUT_SPIWAY))
	print(UI.warning(STR_INFO_SPIWAY))
	print(UI.getTab(STR_SPIWAY))
	
	if flasher.err or flasher.sp.is_open == False:
		print(UI.warning(STR_PORT_UNAVAILABLE))
		print(UI.warning(flasher.err))
		input(STR_BACK)
		return
	
	ping = flasher.ping()
	ver_maj, ver_min = ping['VER']
	UI.showTable({
		'Version':'%d.%02d'%(ver_maj, ver_min),
		'Memory':'%d bytes'%ping['RAM'],
	})
	print()
	
	if ping['VER'] != flasher.VERSION:
		flasher.close()
		input(STR_BACK)
		return
	
	info = flasher.getChipInfo()
	
	if flasher.Config.IC_ID == 0:
		UI.showTable({
			'Device ID': '0x%02X'%flasher.Config.VENDOR_ID,
			'Vendor ID': '0x%04X'%flasher.Config.DEVICE_ID,
		})
		input(STR_BACK)
		return
	
	print(UI.highlight(STR_CHIP_CONFIG)+':\n')
	UI.showTable(info)
	print()
	
	# Show current file info
	if act != 'read' and path and os.path.isfile(path):
		print(UI.highlight(STR_FILE_INFO)+':\n')
		UI.showTable({
			'File':		os.path.basename(path),
			'MD5':		Utils.getFileMD5(path),
			'Size':		'%d MB'%(os.stat(path).st_size // (1024**2)),
		})
		print(end=('\n' if act else ''))
	
	# Perform action
	
	cfg = flasher.Config
	
	if act:
		print(' '+UI.highlight(MENU_SPW_ACTS[act] if act in MENU_SPW_ACTS else STR_UNKNOWN)+'\n')
		block, count = chooseBNC(mode, cfg.BLOCK_SIZE)
	
	if act == 'read':
		sfx = '_full' if block == 0 and count == 0 else '_b%d-%d'%(block,block+count)
		path = 'dump_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + sfx + '.bin'
		data = flasher.readChip(block, count)
		print()
		if data:
			with open(path, "wb") as file:
				file.seek(cfg.TOTAL_SIZE - 1)
				file.write(b'\x00')
				file.seek(cfg.BLOCK_SIZE * block)
				file.write(data)
		else:
			path = ''
	
	elif act == 'write':
		if path and os.path.isfile(path):
			with open(path,"rb") as file:
				file.seek(cfg.BLOCK_SIZE * block)
				data = file.read(cfg.BLOCK_SIZE * (count if count > 0 else cfg.BLOCK_COUNT))
				flasher.writeChip(data, False, block, count)
				print()
		else:
			UI.setStatus(STR_FILE_NOT_EXISTS.format(path))
	
	elif act == 'verify':
		if path and os.path.isfile(path):
			with open(path,"rb") as file:
				file.seek(cfg.BLOCK_SIZE * block)
				data = file.read(cfg.BLOCK_SIZE * (count if count else cfg.BLOCK_COUNT))
				vdata = flasher.readChip(block, count)
				print('\n'+STR_VERIFY+': '+(STR_OK if data == vdata else STR_FAIL)+'\n')
		else:
			UI.setStatus(STR_FILE_NOT_EXISTS.format(path))
	
	elif act == 'erase':
		flasher.eraseChip(block, count)
		print()
	
	if act:
		print(STR_DONE)
	
	flasher.close()
	
	# Show file info after read action
	if act == 'read' and path and os.path.isfile(path):
		print('\n'+UI.highlight(STR_FILE_INFO)+':\n')
		UI.showTable({
			'File': os.path.basename(path),
			'MD5': Utils.getFileMD5(path),
			'Size': '%d MB'%(os.stat(path).st_size // (1024*1024)),
		})
	
	# Action done
	
	print(UI.getTab(STR_ACTIONS))
	UI.showTableEx(UI.getMenu(MENU_SPIWAY,1), 3, 17)
	print(UI.DIVIDER)
	UI.showMenu(MENU_EXTRA_FLASHER)
	
	UI.showStatus()
	
	act = ''
	mode = False
	
	choice = input(STR_CHOICE)
	
	if choice == '0':
		return
	elif choice in ['1','2','3']:
		act = 'read'
		mode = int(choice) - 1
	elif choice in ['4','5','6']:
		act = 'write'
		mode = int(choice) - 4
	elif choice in ['7','8','9']:
		act = 'verify'
		mode = int(choice) - 7
	elif choice in ['10','11','12']:
		act = 'erase'
		mode = int(choice) - 10
		
	elif choice == 's':
	    path = screenFileSelect(path, False, True)
	elif choice == 'f':
		if path and os.path.isfile(path):
			return SFlashTools.screenSFlashTools(path)
		else:
			UI.setStatus(STR_FILE_NOT_EXISTS.format(path))
	elif choice == 'm':
	    return screenMainMenu()
	
	screenNorFlasher(path, port, act, mode)



def glitchAndReadSyscon(sp, file):
	
	if not sp.is_open:
		sp.open()
		if not sp.is_open:
			print(UI.error(STR_PORT_CLOSED))
			return
	
	print(STR_WAITING+'\n')
	time.sleep(2)
	
	sp.write(b'\x00')
	
	wait = True
	start_time = time.time()
	
	while wait:
		resp = sp.read(1)
		
		if resp == b'\xEE':
			print('\n'+UI.warning(STR_CHIP_NOT_RESPOND))
		
		if resp == b'\x00':
			print(UI.cyan(' [GLITCH]'))
		
		if resp == b'\x91':
			print(UI.green(' [OCD CMD] connect'))
			while True:
				resp = sp.read(1)
				if resp == b'\x94':
					print(UI.green(' [OCD CMD] exec'))
					wait = False
					sp.read(1)
					break
	
	with open(file, 'wb') as f:
		counter = 0
		print()
		while True:
			data = sp.read(Syscon.BLOCK_SIZE)
			counter += Syscon.BLOCK_SIZE;
			
			f.write(data)
			
			print(UI.highlight(' Progress: {}KB / {}KB'.format(os.stat(file).st_size // 2**10, Syscon.DUMP_SIZE // 2**10))+'\r',end='')
			sys.stdout.flush()
			
			if counter >= Syscon.DUMP_SIZE:
				sp.close()
				break
	
	return time.time() - start_time



def screenSysconReader(port = '', file = ''):
	
	port = port if port else screenChoosePort()
	if not port:
		UI.setStatus(STR_NO_PORTS)
		return
	
	os.system('cls')
	print(TITLE+UI.getTab(STR_ABOUT_SC_GLITCH))
	print(UI.warning(STR_INFO_SC_GLITCH))
	print(UI.getTab(STR_SC_READER))
	
	try:
		serial = WeeSerial(port, {'baudrate':115200, 'timeout':3})
		print(' '+UI.green(serial.getPortInfo())+'\n')
		
		COUNT = int(input(STR_HOW_MUCH_DUMPS))
		COUNT = COUNT if COUNT <= 10 else 10
	except:
		COUNT = 2
	
	if not serial.sp or not serial.sp.is_open:
		print(UI.error(STR_PORT_UNAVAILABLE))
		input(STR_BACK)
		return
	
	file = file if os.path.isfile(file) else os.path.join(os.getcwd(), 'syscon')
	p_md5 = False
	equal = True
	
	print()
	
	for n in range(COUNT):
		print(UI.warning(STR_READING_DUMP_N.format(n+1)))
		ofile = file + '{:02}.bin'.format(n+1)
		
		sec = glitchAndReadSyscon(serial.sp, ofile)
		
		md5 = Utils.getFileMD5(ofile)
		if p_md5 != False and p_md5 != md5:
			equal = False
		p_md5 = md5
		
		UI.showTable({'Elapsed time':STR_SECONDS.format(sec), 'File MD5':md5})
		
		print('\n'+UI.highlight(STR_SAVED_TO.format(ofile)))
		print(UI.DIVIDER)
	
	if equal:
		print(UI.green(STR_FILES_MATCH))
		c = input(UI.highlight(STR_OPEN_IN_SCTOOL))
		if c == 'y':
			SysconTools.screenSysconTools(ofile)
		else:
			UI.clearInput()
	else:
		print(UI.error(STR_FILES_MISMATCH))
	
	print(STR_DONE)
	input(STR_BACK)



def screenSysconFlasher(file = '', port = '', action = ''):
	UI.setStatus(' Syscon Flasher:'+STR_NIY)
	return



def screenSerialMonitor(port = '', emc_mode = False):
	
	port = port if port else screenChoosePort()
	if not port:
		UI.setStatus(STR_NO_PORTS)
		return
	
	serial = WeeSerial(port)
	
	os.system('cls')
	print(TITLE + UI.getTab(STR_INFO))
	print(' '+UI.green(serial.getPortInfo()))
	print('\n'+UI.warning(STR_INFO_MONITOR))
	
	print(UI.getTab(STR_SERIAL_MONITOR))
	
	if serial.err or serial.sp.is_open == False:
		print(UI.warning(STR_PORT_UNAVAILABLE))
		print(UI.warning(serial.err))
		input(STR_BACK)
		return
	
	serial.startMonitor()
	#serial.testPatterns('../uart.txt')
	while serial.sp.is_open and serial.alive:
		txt = input()
		if not len(txt):
			continue
		elif Utils.checkCtrl(txt[0],'R'):
			serial.sp.close()
			os.system('cls')
			time.sleep(0.1) # port open/close need some delay
			return screenSerialMonitor(port)
		elif Utils.checkCtrl(txt[0],'Q'):
			serial.sp.close()
			UI.clearInput()
			print('\n' + UI.highlight(STR_STOP_MONITORING))
			break
		elif Utils.checkCtrl(txt[0],'E'):
			UI.clearInput()
			emc_mode = False if emc_mode else True
			print('\n' + UI.highlight(STR_EMC_CMD_MODE.format(STR_ON if emc_mode else STR_OFF)))
			continue
		elif emc_mode:
			txt = Utils.getEmcCmd(txt)
			UI.clearInput()
			print(txt)
			
		serial.sendText(txt)
	if serial.err:
		print(' '+UI.error(serial.err))
	input(STR_BACK)



def screenChoosePort():
	os.system('cls')
	print(TITLE + UI.getTab(STR_PORTS_LIST))
	
	ports = WeeSerial.getPortList()
	
	for i in range(len(ports)):
		port = ports[i]
		print(' % 2s: %s - %s'%(i+1, port['port'], port['desc']))
    
	if not len(ports):
		print(UI.warning(STR_NO_PORTS))
		input(STR_BACK)
		return ''
    
	UI.showStatus()
	
	try:
		c = input(STR_CHOICE)
		
		if c == '':
			return
		
		c = int(c)
		
		if c > 0 and c <= len(ports):
			return ports[c-1]['port']
		else:
			UI.setStatus(STR_ERROR_INPUT)
	except:
		UI.setStatus(STR_ERROR_INPUT)
	
	return screenChoosePort()



def screenMainMenu():
	os.system('cls')
	print(TITLE + UI.getTab(STR_MAIN_MENU))
	
	UI.showMenu(MENU_TOOL_SELECTION,1)
	
	UI.showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == '1':
		screenFileSelect()
	elif choice == '2':
		screenSerialMonitor()
	elif choice == '3':
		screenNorFlasher()
	elif choice == '4':
		screenSysconFlasher()
	elif choice == '5':
		screenSysconReader()
	elif choice == '6':
		return quit()
	else:
		UI.setStatus(STR_ERROR_CHOICE)
		
	screenMainMenu()



def screenFileSelect(path = '', all = False, ret = False):
	os.system('cls')
	print(TITLE + UI.getTab(STR_FILE_LIST+' '+('[all]' if all else '[bin, pup]')))
	
	path = path if os.path.exists(path) else os.getcwd()
	path = path if os.path.isdir(path) else os.path.dirname(path)
	
	print(Clr.fg.l_grey+(' %s\n'%path)+Clr.reset)
	
	list = [os.path.dirname(path)]
	print('  0: '+os.sep+'..')
	
	dirs = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
	files = [x for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x))]
	
	dirs.sort()
	files.sort()
	
	for d in dirs:
		list.append(os.path.join(path, d))
		print((' %2d: '+os.sep+'%s'+os.sep)%(len(list)-1,d))
	
	for f in files:
		if all or f.lower().endswith('.bin') or f.lower().endswith('.pup'):
			list.append(os.path.join(path, f))
			print(' %2d: %s'%(len(list)-1,f))
	
	print(UI.DIVIDER)
	UI.showMenu(MENU_FILE_SELECTION)
	UI.showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == 'a':
		all = False if all else True
	elif choice == 'f':
		AdvSFlashTools.screenBuildNorDump(path)
	elif choice == 'b':
		screenBuild2BLS(path)
	elif choice == 'c':
		file_list = [os.path.join(path, x) for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x)) and x.lower().endswith('.bin')]
		file_list.sort()
		screenCompareFiles(file_list)
	elif choice == 'm':
		return screenMainMenu()
	elif choice != '':
		try:
			ind = int(choice)
			if ind >= 0 and ind < len(list):
				path = list[ind]
				if not os.path.isdir(path):
					if ret:
						return path
					else:
						launchTool(path)
			else:
				UI.setStatus(STR_ERROR_CHOICE)
		except Exception as error:
			UI.setStatus(' %s'%error)
	
	screenFileSelect(path, all)



def screenCompareFiles(list):
	os.system('cls')
	print(TITLE + UI.getTab(STR_COMPARE))
	
	if len(list) == 0:
		print(STR_EMPTY_FILE_LIST)
		input(STR_BACK)
		return
	
	res = True
	c_md5 = False
	for i, file in enumerate(list):
		if not file or not os.path.isfile(file):
			print((STR_FILE_NOT_EXISTS).format(file))
			continue
		else:
			md5 = Utils.getFileMD5(file)
			c_md5 = md5 if not c_md5 else c_md5
			if c_md5 != md5:
				res = False
			print((' [{}] {}').format(md5,  os.path.basename(file)))
	
	print(UI.DIVIDER)
	print(STR_COMPARE_RESULT.format((STR_FILES_MATCH if res else STR_FILES_MISMATCH), res))
	input(STR_BACK)
	
	screenFileSelect()



def screenUnpack2BLS(path):
	os.system('cls')
	print(TITLE + UI.getTab(STR_UNPACK_2BLS))
	
	with open(path,'rb') as f:
		data = f.read()
	
	fname = os.path.splitext(os.path.basename(path))[0]
	folder = os.path.join(os.path.dirname(path), fname+'_2bls')	
	
	info = Slb2.getGet2BLSInfo(data)
	
	print(UI.highlight(' Header'))
	head = '\n'.join(UI.getTable(info['header'], 16))
	txt_info = 'Header:\n\n' + head + '\n'
	print(head)
	
	if not os.path.isdir(folder):
		os.makedirs(folder)
	
	entries = info['entries']
	txt_info += 'Entries:\n\n'
	
	for key in entries:
		entry = entries[key]
		
		print(UI.highlight('\n Entry %s'%key))
		e_info = '\n'.join(UI.getTable(entry,16))
		txt_info += e_info + '\n'
		print(e_info)
		
		with open(os.path.join(folder, entry['name']),'wb') as out:
			out.write(data[entry['offset']:entry['offset'] + entry['size']])
	
	with open(os.path.join(folder, Utils.INFO_FILE_2BLS),'w') as txt:
		txt.write(txt_info)
	
	print('\n'+STR_SAVED_TO.format(folder))
	
	input(STR_BACK)



def screenBuild2BLS(path):
	os.system('cls')
	print(TITLE + UI.getTab(STR_2BLS_BUILDER))
	
	name = os.path.basename(path).replace('_2bls','')+ '.2bls'
	file = os.path.join(os.path.dirname(path),name)
	
	files = [os.path.join(path,x) for x in os.listdir(path) if os.path.isfile(os.path.join(path, x)) and x != Utils.INFO_FILE_2BLS]
	
	if len(files) == 0:
		print(STR_EMPTY_FILE_LIST)
		input(STR_BACK)
		return
	
	data = Slb2.build2BLS(files)
	
	with open(file, 'wb') as out:
		out.write(data)
	
	info = Slb2.getGet2BLSInfo(data)
	
	print(UI.highlight(' Header'))
	UI.showTable(info['header'])
	
	entries = info['entries']
	for key in entries:
		entry = entries[key]
		
		print(UI.highlight('\n Entry %s'%key))
		UI.showTable(entry)
	
	
	print('\n'+STR_SAVED_TO.format(file))
	
	input(STR_BACK)



def screenHelp():
	os.system('cls')
	print(TITLE + UI.getTab(STR_HELP))
	print(STR_APP_HELP)
	
	UI.showStatus()
	
	input(STR_BACK)



def chooseBNC(mode = 0, block_size = 0):
	
	block = 0
	count = 0
	
	if mode == 1:
		areas = [
			{'n':'PS4 Full dump',		'o':0,											'l':SFlash.DUMP_SIZE},
			{'n':'PS4 Base Info',		'o':SFlash.NOR_PARTITIONS['s0_header']['o'],	'l':SFlash.NOR_PARTITIONS['s0_blank']['o']},
			{'n':'PS4 Flags (NVS)',		'o':SFlash.NOR_PARTITIONS['s0_nvs']['o'],		'l':SFlash.NOR_PARTITIONS['s0_nvs']['l']},
			{'n':'PS4 CoreOS switch',	'o':SFlash.NOR_AREAS['CORE_SWCH']['o'],			'l':SFlash.NOR_AREAS['CORE_SWCH']['l']},
		]
		for i in range(len(areas)):
			areas[i]['b'] = areas[i]['o'] // block_size
			areas[i]['c'] = areas[i]['l'] // block_size + (1 if areas[i]['l'] % block_size else 0)
		
		UI.showMenu(['[%03d %03d] %s'%(areas[i]['b'], areas[i]['c'], areas[i]['n']) for i in range(len(areas))])
		num = input(UI.DIVIDER+STR_CHOOSE_AREA)
		print()
		try:
			num = int(num)
			if num < len(areas):
				block = areas[num]['b']
				count = areas[num]['c']
		except:
			num = 0
	
	if mode == 2:
		str = input(STR_INPUT_BLOCK)
		print()
		try:
			num = str.split()
			block = int(num[0])
			count = int(num[1]) if len(num) > 1 else 1
		except:
			count = 1
	
	return [block, count]



def launchTool(path):
	
	if not os.path.exists(path):
		return 0
	
	if os.path.isdir(path):
		if os.path.exists(os.path.join(path, Utils.INFO_FILE_SFLASH)):
			return AdvSFlashTools.screenBuildNorDump(path)
		elif os.path.exists(os.path.join(path, Utils.INFO_FILE_2BLS)):
			return screenBuild2BLS(path)
		else:
			#TODO: maybe open SPIway?
			UI.setStatus(STR_UNK_CONTENT + ' {}'.format(path))
			return 0
	
	f_size = os.stat(path).st_size
	with open(path,'rb') as f:
		header = f.read(0x10)
	
	if f_size == SFlash.DUMP_SIZE:
		return SFlashTools.screenSFlashTools(path)
	elif f_size == Syscon.DUMP_SIZE:
		return SysconTools.screenSysconTools(path)
	elif header[0:len(Slb2.SLB2_HEADER)] == Slb2.SLB2_HEADER:
		return screenUnpack2BLS(path)
	else:
		UI.setStatus(STR_UNK_FILE_TYPE + ' {}'.format(path))
