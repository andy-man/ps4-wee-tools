#==============================================================
# Common Tools
# part of ps4 wee tools project
#==============================================================
import os, sys

from lang._i18n_ import *
import utils.utils as Utils
import utils.slb2 as Slb2
import tools.NorTools as NorTools
import tools.SysconTools as SysconTools



def launchTool(path):
	
	if not os.path.exists(path):
		return 0
	
	if os.path.isdir(path):
		if os.path.exists(os.path.join(path, Utils.INFO_FILE_NOR)):
			return NorTools.screenBuildNorDump(path)
		elif os.path.exists(os.path.join(path, Utils.INFO_FILE_2BLS)):
			return screenBuild2BLS(path)
		else:
			setStatus(STR_UNK_CONTENT + ' {}'.format(path))
			return 0
	
	f_size = os.stat(path).st_size
	with open(path,'rb') as f:
		header = f.read(0x10)
	
	if f_size == NorTools.NOR_DUMP_SIZE:
		return NorTools.screenNorTools(path)
	elif f_size == SysconTools.SYSCON_DUMP_SIZE:
		return SysconTools.screenSysconTools(path)
	elif header[0:len(Slb2.SLB2_HEADER)] == Slb2.SLB2_HEADER:
		return screenUnpack2BLS(path)
	else:
		setStatus(STR_UNK_FILE_TYPE + ' {}'.format(path))



def screenFileSelect(path = '', all = False):
	os.system('cls')
	print(TITLE + getTab(STR_FILE_LIST+' '+('[all]' if all else '[bin, pup]')))
	
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
	
	print(DIVIDER)
	getMenu(MENU_FILE_SELECTION)
	showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == 'a':
		all = False if all else True
	elif choice == 'f':
		NorTools.screenBuildNorDump(path)
	elif choice == 's':
		screenBuild2BLS(path)
	elif choice == 'c':
		file_list = [os.path.join(path, x) for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x)) and f.lower().endswith('.bin')]
		file_list.sort()
		screenCompareFiles(file_list)
	elif choice == 'e':
		return quit()
	elif choice != '':
		try:
			ind = int(choice)
			if ind >= 0 and ind < len(list):
				path = list[ind]
				if not os.path.isdir(path):
					launchTool(path)
			else:
				setStatus(STR_ERROR_CHOICE)
		except Exception as error:
			setStatus(' %s'%error)
	
	screenFileSelect(path, all)



def screenCompareFiles(list):
	os.system('cls')
	print(TITLE + getTab(STR_COMPARE))
	
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
	
	print(DIVIDER)
	print(STR_COMPARE_RESULT.format((STR_FILES_MATCH if res else STR_FILES_MISMATCH), res))
	input(STR_BACK)
	
	screenFileSelect()



def screenUnpack2BLS(path):
	os.system('cls')
	print(TITLE + getTab(STR_UNPACK_2BLS))
	
	with open(path,'rb') as f:
		data = f.read()
	
	fname = os.path.splitext(os.path.basename(path))[0]
	folder = os.path.join(os.path.dirname(path), fname+'_2bls')	
	
	info = Slb2.getGet2BLSInfo(data)
	
	print(highlight(' Header'))
	head = showTable(info['header'],16,False)
	txt_info = 'Header:\n\n' + head + '\n'
	print(head,end='')
	
	if not os.path.isdir(folder):
		os.makedirs(folder)
	
	entries = info['entries']
	txt_info += 'Entries:\n\n'
	
	for key in entries:
		entry = entries[key]
		
		print(highlight('\n Entry %s'%key))
		e_info = showTable(entry,16,False)
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
	print(TITLE + getTab(STR_2BLS_BUILDER))
	
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
	
	print(highlight(' Header'))
	showTable(info['header'])
	
	entries = info['entries']
	for key in entries:
		entry = entries[key]
		
		print(highlight('\n Entry %s'%key))
		showTable(entry)
	
	
	print('\n'+STR_SAVED_TO.format(file))
	
	input(STR_BACK)



def screenHelp():
	os.system('cls')
	print(TITLE + getTab(STR_HELP) + STR_APP_HELP)
	
	showStatus()
	
	input(STR_BACK)

