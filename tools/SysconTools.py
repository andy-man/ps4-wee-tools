#==============================================================
# PS4 Syscon Tools
# part of ps4 wee tools project
#==============================================================
import os
from lang._i18n_ import *
from utils.utils import *
from utils.syscon import *
import tools.Tools as Tools

def toggleDebug(file):
	with open(file, 'r+b') as f:
		
		cur = getSysconData(f, 'DEBUG')[0]
		val = b'\x04' if cur == 0x84 or cur == 0x85 else b'\x85'
		
		setSysconData(f, 'DEBUG',  val)
	
	setStatus(STR_DEBUG+(STR_OFF if val == b'\x04' else STR_ON))



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



def screenActiveSNVS(file, block = False):
	os.system('cls')
	print(TITLE+getTab(STR_LAST_SVNS))
	

	
	with open(file, 'rb') as f:
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
	
	entries = SNVS.getLastDataEntries() if block == False else SNVS.getDataBlockEntries(block)
	base = SNVS.getLastDataBlockOffset(True) if block == False else SNVS.getDataBlockOffset(block, True)
	
	active = SNVS.active_entry.getLink()
	print(' Active {} current {}\n'.format(active, block if block else active))
	printSnvsEntries(base, entries)
	
	#input(STR_BACK)
	try:
		num = int(input(DIVIDER+' Select data block [0-7]'))
		if num >= 0 and num <= 7:
			block = num
	except:
		return
	
	screenActiveSNVS(file, block)



def screenAutoPatchSNVS(file):
	os.system('cls')
	print(TITLE+getTab(STR_APATCH_SVNS))
	
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
		print(STR_UNPATCHABLE.format(len(entries),last.getCounter(),last.getIndex(), index, prev_index ))
		input(STR_BACK)
		return
	
	out_file = os.path.basename(file).replace(" ", "_").rsplit('.', maxsplit=1)[0]
	
	options = MENU_PATCHES
	options[1] = options[1].format(len(entries) - index)
	
	print(Clr.fg.cyan+STR_PATCH_INDEXES.format(cur_o, pre_o)+Clr.reset)
	getMenu(options,1)
	showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == '':
	    return
	elif choice == '1':
		ofile = out_file+'_patch_A.bin'
		savePatchData(ofile, data, [{'o':cur_o,'d':b'\xFF'*NvsEntry.getEntrySize()*4}]);
		setStatus(STR_PATCH_SAVED.format(ofile))
	elif choice == '2':
		ofile = out_file+'_patch_B.bin'
		savePatchData(ofile, data, [{'o':cur_o,'d':b'\xFF'*NvsEntry.getEntrySize()*(len(entries) - index)}]);
		setStatus(STR_PATCH_SAVED.format(ofile))
	elif choice == '3':
		ofile = out_file+'_patch_C.bin'
		savePatchData(ofile, data, [{'o':cur_o,'d':data[pre_o:pre_o + NvsEntry.getEntrySize()*4]}]);
		setStatus(STR_PATCH_SAVED.format(ofile))
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
		setStatus(STR_PATCH_SAVED.format(ofile))
	else:
		setStatus(STR_ERROR_CHOICE)
	
	screenAutoPatchSNVS(file)



def screenManualPatchSNVS(file):
	os.system('cls')
	print(TITLE+STR_INFO_SC_MPATCH+getTab(STR_MPATCH_SVNS))
	
	with open(file, 'r+b') as f:
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
		entries = SNVS.getLastDataEntries()
		
		records_count = 16 if len(entries) > 16 else len(entries)
		print(STR_LAST_DATA.format(records_count, len(entries)))
		print()
		
		base = SNVS.getLastDataBlockOffset(True) + NvsEntry.getEntrySize() * (len(entries) - records_count)
		printSnvsEntries(base, entries[-records_count:])
		
		try:
			num = int(input(STR_MPATCH_INPUT))
		except:
			return
		
		if num > 0 and num < len(entries):
			length = num*NvsEntry.getEntrySize()
			offset += NvsEntry.getEntrySize() - length
			setData(f, offset, b'\xFF'*length)
			setStatus(STR_PATCH_SUCCESS.format(num)+' [{:X} - {:X}]'.format(offset,offset + length))
		else:
			setStatus(STR_PATCH_CANCELED)



def screenSysconTools(file):
	os.system('cls')
	print(TITLE+getTab(STR_SYSCON_INFO))
	
	info = getSysconInfo(file)
	if not info:
		return Tools.screenFileSelect(file)
	
	showTable(info)
	
	print(getTab(STR_ACTIONS))
	getMenu(MENU_SC_ACTIONS)
	
	showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == '0':
	    return Tools.screenFileSelect(file)
	elif choice == '1':
		toggleDebug(file)
	elif choice == '2':
		screenActiveSNVS(file)
	elif choice == '3':
		screenAutoPatchSNVS(file)
	elif choice == '4':
		screenManualPatchSNVS(file)
	elif choice == '5':
	    quit()
	
	screenSysconTools(file)



def getSysconInfo(file):
	if not checkFileSize(file, SYSCON_DUMP_SIZE):
		return False
	
	with open(file, 'rb') as f:
		magic = checkSysconData(f, 'MAGIC_1') and checkSysconData(f, 'MAGIC_2') and checkSysconData(f, 'MAGIC_3')
		debug = getSysconData(f, 'DEBUG')[0]
		debug = STR_ON if debug == 0x84 or debug == 0x85 else STR_OFF
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
			'Entries'		: STR_SNVS_ENTRIES.format(len(SNVS.getLastDataEntries()), SNVS.getLastDataBlockOffset(True)),
			'Patchable'		: STR_NO if isSysconPatchable(entries) == 0 else STR_PROBABLY
		}
	
	return info