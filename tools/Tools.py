#==============================================================
# Common Tools
# part of ps4 wee tools project
#==============================================================
import os, sys, time
from lang._i18n_ import *
from utils.serial import WeeSerial
import utils.utils as Utils
import utils.slb2 as Slb2
import utils.sflash as SFlash
import utils.syscon as Syscon
import utils.syscon_rw as SysconRW
import tools.SFlashTools as SFlashTools
import tools.SysconTools as SysconTools
import tools.AdvSFlashTools as AdvSFlashTools



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
		
		UI.showTable({'Elapsed time':'{:0.0f} seconds'.format(sec), 'File MD5':md5})
		
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



def screenSysconFlasher(file = ''):
	UI.setStatus(' Syscon Flasher:'+STR_NIY)
	return



def screenNorFlasher(file = ''):
	UI.setStatus(' sFlash Reader:'+STR_NIY)
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



def launchTool(path):
	
	if not os.path.exists(path):
		return 0
	
	if os.path.isdir(path):
		if os.path.exists(os.path.join(path, Utils.INFO_FILE_SFLASH)):
			return AdvSFlashTools.screenBuildNorDump(path)
		elif os.path.exists(os.path.join(path, Utils.INFO_FILE_2BLS)):
			return screenBuild2BLS(path)
		else:
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



def screenFileSelect(path = '', all = False):
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
		file_list = [os.path.join(path, x) for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x)) and f.lower().endswith('.bin')]
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
	head = UI.getTable(info['header'], 16)
	txt_info = 'Header:\n\n' + head + '\n'
	print(head,end='')
	
	if not os.path.isdir(folder):
		os.makedirs(folder)
	
	entries = info['entries']
	txt_info += 'Entries:\n\n'
	
	for key in entries:
		entry = entries[key]
		
		print(UI.highlight('\n Entry %s'%key))
		e_info = UI.getTable(entry,16)
		txt_info += e_info + '\n'
		print(e_info,end='')
		
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

