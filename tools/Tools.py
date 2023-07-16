#==============================================================
# Common Tools
# part of ps4 wee tools project
#==============================================================
import os, sys

from lang._i18n_ import *
import utils.utils as Utils
import tools.NorTools as NorTools
import tools.SysconTools as SysconTools


def launchTool(fname):
	
	if os.path.isdir(fname):
		return NorTools.screenBuildNorDump(fname)
	
	f_size = os.stat(fname).st_size
	
	if f_size == NorTools.NOR_DUMP_SIZE:
		return NorTools.screenNorTools(fname)
	elif f_size == SysconTools.SYSCON_DUMP_SIZE:
		return SysconTools.screenSysconTools(fname)
	else:
		setStatus(STR_UNK_FILE_TYPE + ' {}'.format(fname))
		return screenFileSelect()



def screenFileSelect(fname = ''):
	
	if len(fname) and os.path.exists(fname):
		return launchTool(fname)
	
	os.system('cls')
	print(TITLE + getTab(STR_FILE_LIST))
	
	files = []
	for f in os.listdir(os.getcwd()):
		if f.lower().endswith('.bin'):
			files.append(f)
			print(' '+str(len(files))+': '+f)
	
	if len(files) == 0:
		return screenHelp()
	
	showStatus()
	
	try:
		choice = int(input(STR_CHOICE))
		if 1 <= choice <= len(files):
			launchTool(os.getcwd() + os.sep + files[choice - 1])
		else:
			setStatus(STR_ERROR_CHOICE)
	except:
		setStatus(STR_ERROR_INPUT)
	
	screenFileSelect()



def screenCompareFiles(list):
	os.system('cls')
	print(TITLE + getTab(STR_COMPARE))
	
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



def screenHelp():
	os.system('cls')
	print(TITLE + getTab(STR_HELP) + STR_APP_HELP)
	
	showStatus()
	
	input(STR_BACK)

