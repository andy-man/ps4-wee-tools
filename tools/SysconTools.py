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
		color = Clr.fg.d_grey
		if v[1] in SC_TYPES_MODES:
			color = Clr.fg.green
		if v[1] in SC_TYPES_FSM:
			color = Clr.fg.purple
		elif v[1] in SC_TYPES_UPD:
			color = Clr.fg.cyan
		elif v[1] in SC_TYPES_PRE0:
			color = Clr.fg.orange
		elif v[1] in SC_TYPES_PRE2:
			color = Clr.fg.red
		print(' {:5X} | '.format(base + (i * NvsEntry.getEntrySize())) + color + getHex(v)+Clr.reset)



def screenViewSNVS(file, block = ''):
	os.system('cls')
	print(TITLE+getTab(STR_SVNS_ENTRIES))
	
	with open(file, 'rb') as f:
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
	
	blocks_count = SNVS_CONFIG.getDataCount()-1
	records_count = SNVS_CONFIG.getDataRecordsCount()
	active = SNVS.active_entry.getLink()
	block = active if block == '' else block
	
	entries = SNVS.getDataBlockEntries(block)
	base = SNVS.getDataBlockOffset(block, True)
	
	print(STR_SYSCON_BLOCK.format(block, blocks_count, len(entries), records_count, active))
	printSnvsEntries(base, entries)
	
	showStatus()
	
	try:
		num = int(input(DIVIDER+STR_SC_BLOCK_SELECT.format(blocks_count)))
		if num >= 0 and num <= blocks_count:
			block = num
		else:
			setStatus(STR_ERROR_CHOICE)
	except:
		return
	
	screenViewSNVS(file, block)



def screenAutoPatchSNVS(file):
	os.system('cls')
	print(TITLE+getTab(STR_APATCH_SVNS))
	
	with open(file, 'rb') as f:
		data = f.read()
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
	
	# search in last block if not found use previous
	entries = SNVS.getLastDataEntries()
	
	index = getLast_080B_Index(entries)
	prev_index = getLast_080B_Index(entries[:index])
	
	base = SNVS.getLastDataBlockOffset(True)
	last = NvsEntry(entries[-1])
	
	cur_o = index * NvsEntry.getEntrySize() + base
	pre_o = prev_index * NvsEntry.getEntrySize() + base
	
	status = isSysconPatchable(entries)
	if index < 0 or prev_index < 0 or status == 0:
		print(STR_UNPATCHABLE.format(len(entries),last.getCounter(),last.getIndex(), index, prev_index ))
		input(STR_BACK)
		return
	
	out_file = getFilePathWoExt(file,True)
	
	options = MENU_PATCHES
	options[1] = options[1].format(len(entries) - index)
	options[4] = options[4].format(len(entries) - prev_index)
	
	print(highlight(STR_PATCH_INDEXES.format(cur_o, pre_o)))
	
	print(' Status: '+MENU_SC_STATUSES[status])
	recommend = ['-','A','D','B']
	print(warning(STR_RECOMMEND.format(recommend[status]))+'\n')
	
	getMenu(options,1)
	showStatus()
	
	choice = input(STR_CHOICE)
	
	try:
		c = int(choice)
	except:
		return
	
	ofile = ''
	
	if c == 1:
		ofile = out_file+'_patch_A.bin'
		savePatchData(ofile, data, [{'o':cur_o,'d':b'\xFF'*NvsEntry.getEntrySize()*4}])
	elif c == 2:
		ofile = out_file+'_patch_B.bin'
		savePatchData(ofile, data, [{'o':cur_o,'d':b'\xFF'*NvsEntry.getEntrySize()*(len(entries) - index)}])
	elif c == 3:
		ofile = out_file+'_patch_C.bin'
		savePatchData(ofile, data, [{'o':cur_o,'d':data[pre_o:pre_o + NvsEntry.getEntrySize()*4]}])
	elif c == 4:
		ofile = out_file+'_patch_D.bin'
		offset = pre_o + 4*NvsEntry.getEntrySize(); size = NvsEntry.getEntrySize()*(len(entries) - prev_index - 4)
		savePatchData(ofile, data, [{'o':offset, 'd':b'\xFF'*size}])
	elif c == 5:
		ofile = out_file+'_counters_fix.bin'
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
		savePatchData(ofile, data, [{'o':base,'d':new_entries}])
	
	if ofile:
		setStatus(STR_SAVED_TO.format(ofile))
	else:
		setStatus(STR_ERROR_CHOICE)
	
	screenAutoPatchSNVS(file)



def screenManualPatchSNVS(file):
	os.system('cls')
	print(TITLE+getTab(STR_ABOUT_MPATCH))
	
	print(STR_INFO_SC_MPATCH)
	
	print(getTab(STR_MPATCH_SVNS))
	
	with open(file, 'r+b') as f:
		SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
		entries = SNVS.getLastDataEntries()
		
		block = SNVS.active_entry.getLink()
		records_count = 16 if len(entries) > 16 else len(entries)
		print(STR_LAST_SC_ENTRIES.format(records_count, len(entries), block))
		print()
		
		
		last_offset = SNVS.getLastDataBlockOffset(True) + NvsEntry.getEntrySize() * len(entries)
		printSnvsEntries(last_offset - NvsEntry.getEntrySize() * records_count, entries[-records_count:])
		
		showStatus()
		
		print(DIVIDER+'\n 0:'+STR_GO_BACK)
		
		try:
			num = int(input(STR_MPATCH_INPUT))
		except:
			return screenManualPatchSNVS(file)
		
		if num > 0 and num < len(entries):
			length = num*NvsEntry.getEntrySize()
			setData(f, last_offset - length, b'\xFF'*length)
			setStatus(STR_PATCH_SUCCESS.format(num)+' [{:X} - {:X}]'.format(last_offset - length, last_offset))
		elif num == len(entries):
			if SNVS.getOWC() == 0:
				setData(f, SNVS.getLastVolumeEntryOffset(True), b'\xFF'*NvsEntry.getEntryHeadSize())
				setData(f, SNVS.getLastDataBlockOffset(True) - SNVS.cfg.getDataFlatLength(), b'\xFF'*SNVS.cfg.getDataLength())
				setStatus(STR_SC_BLOCK_CLEANED.format(block))
			else:
				setStatus(STR_REBUILD_REQUIRED)
		elif num > len(entries):
			setStatus(STR_TOO_MUCH.format(num,len(entries)))
		elif num == 0:
			setStatus(STR_PATCH_CANCELED)
			return
	
	screenManualPatchSNVS(file)



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
		screenViewSNVS(file)
	elif choice == '3':
		screenAutoPatchSNVS(file)
	elif choice == '4':
		screenManualPatchSNVS(file)
	elif choice == '5':
		
		with open(file, 'rb') as f:
			data = f.read()
			SNVS = NVStorage(SNVS_CONFIG, getSysconData(f, 'SNVS'))
			snvs_data = SNVS.getRebuilded()
		
		ofile = getFilePathWoExt(file,True) + '_rebuild.bin'
		
		with open(ofile, 'wb') as f:
			 f.write(data)
			 setSysconData(f, 'SNVS', snvs_data)
		
		setStatus(STR_SAVED_TO.format(ofile))
	elif choice == '6':
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
		snvs_info = 'Vol[{:d}] Data[{:d}] Counter[0x{:X}] OWC[{}]'.format(
			SNVS.active_volume,
			SNVS.active_entry.getLink(),
			SNVS.active_entry.getCounter(),
			SNVS.getOWC(),
		)
		
		info = {
			'FILE'			: os.path.basename(file),
			'MD5'			: getFileMD5(file),
			'Magic'			: ('True' if magic else 'False'),
			'Debug'			: debug,
			'Version'		: '{:X}.{:X}'.format(ver[0],ver[2]),
			'SNVS'			: snvs_info,
			'Entries'		: STR_SNVS_ENTRIES.format(len(SNVS.getLastDataEntries()), SNVS.getLastDataBlockOffset(True)),
			'Status'		: MENU_SC_STATUSES[isSysconPatchable(entries)],
		}
	
	return info