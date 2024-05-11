#==============================================================
# PS4 Syscon Tools
# part of ps4 wee tools project
#==============================================================
import os
from lang._i18n_ import *
import utils.syscon as Syscon
import utils.utils as Utils
import tools.Tools as Tools
import tools.AdvSysconTools as AdvSCTools

def toggleDebug(file):
	with open(file, 'r+b') as f:
		
		cur = Syscon.getSysconData(f, 'DEBUG')[0]
		val = b'\x04' if cur == 0x84 or cur == 0x85 else b'\x85'
		
		Syscon.setSysconData(f, 'DEBUG',  val)
	
	UI.setStatus(STR_DEBUG+(STR_OFF if val == b'\x04' else STR_ON))



def printSnvsEntries(base,entries,start=''):
	
	for i,v in enumerate(entries):
		color = Clr.fg.d_grey
		if v[1] in Syscon.SC_TYPES_MODES:
			color = Clr.fg.green
		elif v[1] in Syscon.SC_TYPES_BOOT:
			color = Clr.fg.pink
		elif v[1] in Syscon.SC_TYPES_UPD:
			color = Clr.fg.cyan
		elif v[1] in Syscon.SC_TYPES_PRE0:
			color = Clr.fg.orange
		elif v[1] in Syscon.SC_TYPES_PRE2:
			color = Clr.fg.red
		
		num = '%03d'%(start + i) if start != '' else ''
		print(' {:5X} | '.format(base + (i * Syscon.NvsEntry.getEntrySize())) + color + Utils.hex(v)+Clr.reset + ' | '+num)



def screenViewSNVS(file, block = '', flat = False):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_NVS_ENTRIES%'SNVS'))
	
	with open(file, 'rb') as f:
		SNVS = Syscon.NVStorage(Syscon.SNVS_CONFIG, Syscon.getSysconData(f, 'SNVS'))
	
	blocks_count = Syscon.SNVS_CONFIG.getDataCount()-1
	count = Syscon.SNVS_CONFIG.getDataRecordsCount() if not flat else SNVS.cfg.getDataFlatLength() // Syscon.NvsEntry.getEntrySize()
	active = SNVS.active_entry.getLink()
	block = active if block == '' else block
	
	if flat:
		entries = SNVS.getFlatDataEntries(block)
		base = SNVS.getFlatDataOffset(block, True)
	else:
		entries = SNVS.getDataBlockEntries(block)
		base = SNVS.getDataBlockOffset(block, True)
	
	print((' Flat' if flat else '')+STR_SYSCON_BLOCK%(block, blocks_count, len(entries), count, active))
	printSnvsEntries(base, entries, 1)
	
	UI.showStatus()
	
	try:
		c = input(UI.DIVIDER+STR_SC_BLOCK_SELECT%blocks_count)
		
		if c == 'f':
			flat = False if flat else True
			return screenViewSNVS(file, block, flat)
		
		num = int(c)
		if num >= 0 and num <= blocks_count:
			block = num
		else:
			UI.setStatus(STR_ERROR_CHOICE)
	except:
		return
	
	screenViewSNVS(file, block)



def screenAutoPatchSNVS(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_APATCH_SVNS))
	
	with open(file, 'rb') as f:
		data = f.read()
		SNVS = Syscon.NVStorage(Syscon.SNVS_CONFIG, Syscon.getSysconData(f, 'SNVS'))
	
	entries = SNVS.getAllDataEntries()
	status = Syscon.isSysconPatchable(entries)
	
	upd_entry_size = len(Syscon.SC_TYPES_UPD)
	inds = Syscon.getEntriesByType(Syscon.SC_TYPES_UPD, entries)
	index = inds[-1] if len(inds) >= 1 else -1
	prev_index = inds[-2] if len(inds) >= 2 else -1
	
	last_fw = Syscon.getRecordPos(index, SNVS)
	prev_fw = Syscon.getRecordPos(prev_index, SNVS)
	
	info = {
		'General'			: 'Active[%d] OWC[%d]'%(SNVS.active_entry.getLink(), SNVS.getOWC()),
		'08-0B (prev)'		: STR_NOT_FOUND if prev_index < 0 else STR_SNVS_ENTRY_INFO%(prev_fw['block'], prev_fw['num'], prev_fw['offset']),
		'08-0B (last)'		: STR_NOT_FOUND if index < 0 else STR_SNVS_ENTRY_INFO%(last_fw['block'], last_fw['num'], last_fw['offset']),
		'Order of blocks'	: SNVS.getDataBlocksOrder(),
		'Status'			: MENU_SC_STATUSES[status],
	}
	
	UI.showTable(info, 20)
	print()
	
	if index < 0 or prev_index < 0:
		print(UI.warning(STR_UNPATCHABLE))
		input(STR_BACK)
		return
	
	recommend = ['D','A','C','B']
	print(UI.warning(STR_RECOMMEND%recommend[status]))
	if status == 0:
		print(UI.highlight(STR_SC_WARN_OVERWITTEN))
	print()
	
	options = MENU_PATCHES.copy()
	options[1] = options[1]%(len(entries) - index)
	options[2] = options[2]%(len(entries) - (prev_index + upd_entry_size))
	options[3] = options[3]%(len(entries) - (index + upd_entry_size))
	options[4] = UI.dark(options[4]%(0))

	UI.showMenu(options,1)
	UI.showStatus()
	
	out_file = Utils.getFilePathWoExt(file,True)
	choice = input(STR_CHOICE)
	
	try:
		c = int(choice)
	except:
		return
	
	ofile = ''
	snvs_data = False
	
	if c == 1:
		ofile = out_file+'_patch_A.bin'
		snvs_data = SNVS.getRebuilded([entries[i] for i in range(len(entries)) if i < index or i >= index+4])
	elif c == 2:
		ofile = out_file+'_patch_B.bin'
		snvs_data = SNVS.getRebuilded(entries[:index])
	elif c == 3:
		ofile = out_file+'_patch_C.bin'
		snvs_data = SNVS.getRebuilded(entries[:prev_index + upd_entry_size])
	elif c == 4:
		ofile = out_file+'_patch_D.bin'
		snvs_data = SNVS.getRebuilded(entries[:index + upd_entry_size])
		
	if ofile and snvs_data:
		Utils.savePatchData(ofile, data, [{'o':Syscon.SC_AREAS['SNVS']['o'], 'd':snvs_data}])
		UI.setStatus(STR_SAVED_TO%ofile)
	else:
		UI.setStatus(STR_ERROR_CHOICE)
	
	if c == 5:
		UI.setStatus(STR_NIY)
	
	screenAutoPatchSNVS(file)



def screenManualPatchSNVS(file, flat = False):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_ABOUT_MPATCH))
	
	print(STR_INFO_SC_MPATCH + '\n\n' + UI.warning(STR_IMMEDIATLY))
	
	print(UI.getTab(STR_MPATCH_SVNS))
	
	with open(file, 'r+b') as f:
		SNVS = Syscon.NVStorage(Syscon.SNVS_CONFIG, Syscon.getSysconData(f, 'SNVS'))
		entries = SNVS.getLastFlatEntries() if flat else SNVS.getLastDataEntries()
		
		block = SNVS.active_entry.getLink()
		records_count = 16 if len(entries) > 16 else len(entries)
		records = entries[-records_count:]
		
		offset = SNVS.getLastFlatDataOffset(True) if flat else SNVS.getLastDataBlockOffset(True)
		last_offset = offset + Syscon.NvsEntry.getEntrySize() * len(entries)
		
		print((' FlatData:' if flat else ' Entries:')+STR_LAST_SC_ENTRIES%(records_count, len(entries), block))
		print()
		
		printSnvsEntries(last_offset - Syscon.NvsEntry.getEntrySize() * records_count, records, len(entries)+ 1 - records_count)
		
		UI.showStatus()
		
		print(UI.DIVIDER)
		print(' f:'+STR_SC_TOGGLE_FLATDATA)
		print(' 0:'+STR_GO_BACK)
		
		c = input(STR_MPATCH_INPUT)
		if c.lower() == 'f':
			flat = False if flat else True
		try:
			num = int(c)
		except:
			return screenManualPatchSNVS(file, flat)
		
		if num == 0:
			UI.setStatus(STR_PATCH_CANCELED)
			return
		
		if num > 0 and (num < len(entries) or (flat and num == len(entries))):
			length = num * Syscon.NvsEntry.getEntrySize()
			Utils.setData(f, last_offset - length, b'\xFF'*length)
			UI.setStatus(STR_PATCH_SUCCESS%num+' [{:X} - {:X}]'.format(last_offset - length, last_offset))
		elif num == len(entries):
			if SNVS.getOWC() == 0:
				Utils.setData(f, SNVS.getLastVolumeEntryOffset(True), b'\xFF'*Syscon.NvsEntry.getEntryHeadSize())
				Utils.setData(f, SNVS.getLastDataBlockOffset(True) - SNVS.cfg.getDataFlatLength(), b'\xFF'*SNVS.cfg.getDataLength())
				UI.setStatus(STR_SC_BLOCK_CLEANED%block)
			else:
				UI.setStatus(STR_OWC_RESET_REQUIRED)
		elif num > len(entries):
			UI.setStatus(STR_TOO_MUCH%(num,len(entries)))
	
	screenManualPatchSNVS(file, flat)



def screenSysconTools(file):
	
	MENU_SC_ACTIONS[4-1] = UI.dark(MENU_SC_ACTIONS[4-1])
	
	while True:
	
		UI.clearScreen()
		print(TITLE+UI.getTab(STR_SYSCON_INFO))
		
		info = getSysconInfo(file)
		if not info:
			return Tools.screenFileSelect(file)
		
		UI.showTable(info)
		
		print(UI.getTab(STR_ACTIONS))
		UI.showMenu(MENU_SC_ACTIONS,1)
		print(UI.DIVIDER)
		UI.showMenu(MENU_EXTRA)
		
		UI.showStatus()
		
		choice = input(STR_CHOICE)
		
		if choice == 's':
			Tools.screenFileSelect(file)
			break
		elif choice == 'f':
			Tools.screenSysconFlasher(file)
			break
		elif choice == 'r':
			file = renameToCanonnical(file)
			continue
		elif choice == 'q':
			break

		if choice == '1':
			toggleDebug(file)
		elif choice == '2':
			screenAutoPatchSNVS(file)
		elif choice == '3':
			screenViewSNVS(file)
		elif choice == '4':
			UI.setStatus(STR_NIY)
		elif choice == '5':
			screenManualPatchSNVS(file)
		elif choice == '6':
			AdvSCTools.screenAdvSysconTools(file)
		else:
			UI.setStatus(STR_ERROR_CHOICE)

# Functions

def getSysconInfo(file):
	if not Utils.checkFileSize(file, Syscon.DUMP_SIZE):
		return False
	
	with open(file, 'rb') as f:
		magic = Syscon.checkSysconData(f, ['MAGIC_1','MAGIC_2','MAGIC_3'])
		debug = Syscon.getSysconData(f, 'DEBUG')[0]
		debug = STR_ON if debug == 0x84 or debug == 0x85 else STR_OFF
		ver = Syscon.getSysconData(f, 'VERSION')
		SNVS = Syscon.NVStorage(Syscon.SNVS_CONFIG, Syscon.getSysconData(f, 'SNVS'))
		records = SNVS.getAllDataEntries()
		fw_info = Syscon.checkSysconFW(f)
		snvs_info = 'Vol[%d] Data[%d] Counter[0x%X] OWC[%d]'%(
			SNVS.active_volume,
			SNVS.active_entry.getLink(),
			SNVS.active_entry.getCounter(),
			SNVS.getOWC(),
		)
		
		info = {
			'FILE'			: os.path.basename(file),
			'MD5'			: Utils.getFileMD5(file),
			'Magic'			: STR_OK if magic else STR_FAIL,
			'Debug'			: debug,
			'FW'			: 'v%X.%02X'%(ver[0],ver[2]),
			'FW MD5'		: '%s - %s'%(fw_info['md5'], (STR_OK+' ['+fw_info['fw']+']') if fw_info['fw'] else STR_FAIL),
			'SNVS'			: snvs_info,
			'Entries'		: STR_SNVS_ENTRIES%(len(SNVS.getLastDataEntries()), SNVS.getLastDataBlockOffset(True)),
			'Status'		: MENU_SC_STATUSES[Syscon.isSysconPatchable(records)],
		}
	
	return info



def renameToCanonnical(file):
	fpath = os.path.realpath(file)
	new_name = Syscon.getCanonicalName(file)
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