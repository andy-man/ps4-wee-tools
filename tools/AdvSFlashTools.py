#==============================================================
# PS4 Nor Tools
# part of ps4 wee tools project
#==============================================================
import os
from lang._i18n_ import *
import utils.utils as Utils
import utils.sflash as SFlash
import utils.slb2 as Slb2
import utils.encdec as Encdec
import tools.Tools as Tools



def screenPartitionRecovery(file, partition = ''):
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_ABOUT_PART_RECOVERY))
	print(UI.warning(STR_INFO_PART_A_R))
	print()
	print(UI.warning(STR_INFO_FW_LINK))
	
	part_list = ['s0_emc_ipl_a', 's0_emc_ipl_b', 's0_eap_kbl', 's0_wifi']
	
	if partition in part_list:
		
		with open(file, 'rb') as f:
			fw = SFlash.getNorFW(f)
			slot = 'A' if SFlash.getNorData(f, 'ACT_SLOT')[0] == 0x00 else 'B'
			data = SFlash.getNorPartition(f, partition)
		
		print(UI.getTab(STR_PART_ANALYZE))
		print(' '+UI.highlight(partition)+'\n')
		print(UI.green(STR_FW_VER%(fw['c'], slot))+'\n')
		
		fw_folder = os.path.join(Utils.ROOT_PATH, 'fws')
		sub_folder = ''
		
		if partition.count('emc_ipl'):
			sub_folder = 'emc'
		elif partition.count('eap_kbl'):
			sub_folder = 'eap'
		elif partition.count('wifi'):
			sub_folder = 'torus'
		
		if sub_folder:
			file_list = Utils.getFilesList(os.path.join(fw_folder, sub_folder),'2bls')
		
		expert_mode = False
		if len(file_list):
			
			items = Utils.compareDataWithFiles(data, file_list, 1, True)
			items_count = len(items) if len(items) < 10 else 10
			
			UI.clearInput()
			expert_mode = input('\n'+UI.highlight(STR_EXPERT_MODE+STR_Y_OR_CANCEL)).lower()
			
			if expert_mode == 'y':
				UI.clearInput()
				print(UI.warning(STR_SELECT_MOST_FILE)+'\n')
				
				for k in range(items_count):
					path = items[k]['path']
					rel_path = (os.path.sep).join(path.split(os.path.sep)[-3:])
					percent = int(items[k]['eq'] * 100) / 100
					print(' %d: %s | %.2f%%'%(k, rel_path, percent))
		else:
			print(UI.warning(STR_NO_FW_FILES%fw_folder))
			input(STR_BACK)
			return screenPartitionRecovery(file)
		
		if expert_mode != 'y':
			n = 0
		else:
			try: n = int(input(STR_CHOICE))
			except: n = -1
		
		if n >= 0 and n < items_count:
			
			out_file = Utils.getFilePathWoExt(file, True)+'_patch_'+partition+'.bin'
			data = Utils.getFileContents(file)
			pdata = Utils.getFileContents(items[n]['path'])
			
			Utils.savePatchData(out_file, data, [{'o':SFlash.SFLASH_PARTITIONS[partition]['o'], 'd':pdata}])
			
			UI.setStatus(STR_SAVED_TO%out_file)
		else:
			UI.setStatus(STR_ERROR_INPUT)
		
		return screenPartitionRecovery(file)
	
	print(UI.getTab(STR_PART_LIST))
	
	UI.showMenu(part_list,1)
	print(UI.DIVIDER)
	print(' 0:'+STR_GO_BACK)
	UI.showStatus()
	
	try: n = int(input(STR_CHOICE))
	except: n = -1
	
	if n == 0:
		return
	if n > 0 and n <= len(part_list):
		return screenPartitionRecovery(file, part_list[n-1])
	else:
		UI.setStatus(STR_ERROR_INPUT)
	
	screenPartitionRecovery(file, partition)



def screenValidate(file):
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_SFLASH_VALIDATOR))
	
	with open(file,'rb') as f:
		
		data = f.read()
		
		model = SFlash.getModel(f)
		sku = SFlash.getNorData(f, 'SKU', True)
		fw = SFlash.getNorFW(f)['c']
		slot = SFlash.getActiveSlot(f)
		
		print(' %s / FW: %s [%s]\n'%(sku, fw, slot.upper()))
		
		# Magics
		magics = {}
		for k in SFlash.MAGICS:
			magics[k] = STR_OK if SFlash.checkMagic(data, k) else STR_DIFF
		
		print(UI.highlight(STR_MAGICS_CHECK)+'\n')
		UI.showTable(magics,10)
		print()
		
		# Partitions
		parts_info = {}
		for key in ['s0_emc_ipl_a', 's0_emc_ipl_b', 's0_eap_kbl', 's0_wifi']:
			md5 = SFlash.getNorPartitionMD5(f, key)
			data = SFlash.getDataByPartition(key)
			if md5 in data:
				if fw in data[md5]['fw']:
					parts_info[key] = STR_IS_PART_VALID%(md5, STR_OK, STR_OK)
				else:
					parts_info[key] = STR_IS_PART_VALID%(md5, STR_OK, data[md5]['fw'][0] if len(data[md5]['fw']) == 1 else (data[md5]['fw'][0]+' <-> '+data[md5]['fw'][-1]))
			else:
				parts_info[key] = STR_IS_PART_VALID%(md5, STR_FAIL, STR_FAIL)
		
		print(UI.highlight(STR_PARTITIONS_CHECK)+'\n')
		UI.showTable(parts_info,14)
		print()
		
		# EAP key
		
		magic = SFlash.getNorData(f, 'EAP_MGC')
		eap_key = SFlash.getNorData(f, 'EAP_KEY')
		
		print(UI.highlight(' '+STR_EAP_KEYS+'\n'))
		print(' Magic [%s] %s\n'%(Utils.hex(magic,''), STR_OK if magic == SFlash.SFLASH_AREAS['EAP_MGC']['n'] else STR_DIFF ))
		for i in range(0,len(eap_key),0x20):
			print(' '+Utils.hex(eap_key[i:i+0x20],''))
		
		if model not in [11, 10]:
			magic = SFlash.getNorDataB(f, 'EAP_MGC')
			eap_key_b = SFlash.getNorDataB(f, 'EAP_KEY')
			print()
			print(UI.highlight(' '+STR_EAP_KEYS+' ('+STR_BACKUP+')\n'))
			print(' Magic [%s] %s\n'%(Utils.hex(magic,''), STR_OK if magic == SFlash.SFLASH_AREAS['EAP_MGC']['n'] else STR_DIFF ))
			for i in range(0,len(eap_key_b),0x20):
				print(' '+Utils.hex(eap_key_b[i:i+0x20],''))
			
			print(UI.highlight('\n '+STR_EAP_KEYS+' ') + UI.green(STR_EQUAL) if eap_key == eap_key_b else STR_DIFF)
		
		print()
		
		# NVS
		print(UI.highlight(STR_VALIDATE_NVS_CHECK)+'\n')
		
		for k in ['NVS1', 'NVS2']:
			
			nvs = SFlash.getNorData(f, k)
			key = SFlash.getOffsetRange(k)
			
			print(' %s : %s [%s..%s]'%( key, SFlash.checkNVS(nvs, k), Utils.hex(nvs[0:10],''), Utils.hex(nvs[-10:],'') ) )
			
			if model not in [11, 10]:
				nvs_b = SFlash.getNorDataB(f, k)
				key_b = SFlash.getOffsetRange(k, True)
				
				print(' %s - %s'%(UI.dark(STR_BACKUP), UI.green(STR_EQUAL) if nvs == nvs_b else STR_DIFF))
				print(' %s : %s [%s..%s]'%( key_b, SFlash.checkNVS(nvs_b, k), Utils.hex(nvs_b[0:10],''), Utils.hex(nvs_b[-10:],'') ) )
			
			print()
	
	print(UI.highlight(STR_ENTROPY)+'\n')
	#stats = {'ent':0,'ff':0,'00':0}
	stats = Utils.entropy(file)
	print('\r',end='')
	
	info = {
		
		'Entropy'	: '%.5f'%(stats['ent']),
		'0xFF'		: '%.2f%%'%(stats['ff']*100),
		'0x00'		: '%.2f%%'%(stats['00']*100),
		'Other'		: '%.2f%%'%((1 - stats['ff'] - stats['00'])*100),
	}
	
	UI.showTable(info,10)
	
	input(STR_BACK)



def screenNvsRecovery(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_ABOUT_NVS))
	
	print(UI.warning(STR_INFO_NVS + '\n' + STR_IMMEDIATLY))
	
	print(UI.getTab(STR_NVS_AREAS))
	print(UI.highlight(STR_FILENAME)+os.path.basename(file)+'\n')
	
	NVS_MENU = []
	
	with open(file,'r+b') as f:
		
		model = SFlash.getModel(f)
		sku = SFlash.getNorData(f, 'SKU', True)
		fw = SFlash.getNorFW(f)['c']
		slot = SFlash.getActiveSlot(f)
		
		print(' %s / FW: %s [%s]\n'%(sku, fw, slot.upper()))
		
		for k in ['NVS1', 'NVS2']:
			
			print(' '+UI.highlight(k)+'\n')
			
			nvs = SFlash.getNorData(f, k)
			key = SFlash.getOffsetRange(k)
			
			print(' %s : %s [%s..%s]'%( key, SFlash.checkNVS(nvs, k), Utils.hex(nvs[0:10],''), Utils.hex(nvs[-10:],'') ) )
			
			if model not in [11, 10]:
				nvs_b = SFlash.getNorDataB(f, k)
				key_b = SFlash.getOffsetRange(k, True)
				
				NVS_MENU.append(MENU_NVS_COPY[0]%(k, key,key_b))
				NVS_MENU.append(MENU_NVS_COPY[1]%(k, key,key_b))
				
				print(' %s - %s'%(UI.dark(STR_BACKUP), UI.green(STR_EQUAL) if nvs == nvs_b else STR_DIFF))
				print(' %s : %s [%s..%s]'%( key_b, SFlash.checkNVS(nvs_b, k), Utils.hex(nvs_b[0:10],''), Utils.hex(nvs_b[-10:],'') ) )
			
			print()
		
		UI.showStatus()
		
		print(UI.DIVIDER)
		if model in [11, 10]:
			print(UI.warning(STR_ACTION_NA%('(10xx/11xx)')))
		else:
			UI.showMenu(NVS_MENU,1)
		
		print(UI.DIVIDER)
		UI.showMenu([STR_GO_BACK])
		
		choice = input(STR_CHOICE)
		
		try:
			c = int(choice)
			c = c if model not in [11, 10] or c == 0 else -1
		except:
			c = -1
		
		if c == 0:
			return
		elif c == 1:
			data = SFlash.getNorDataB(f, 'NVS1')
			SFlash.setNorData(f, 'NVS1', data)
		elif c == 2:
			data = SFlash.getNorData(f, 'NVS1')
			SFlash.setNorDataB(f, 'NVS1', data)
		elif c == 3:
			data = SFlash.getNorDataB(f, 'NVS2')
			SFlash.setNorData(f, 'NVS2', data)
		elif c == 4:
			data = SFlash.getNorData(f, 'NVS2')
			SFlash.setNorDataB(f, 'NVS2', data)
		
		if c >= 1 and c <= len(NVS_MENU):
			UI.setStatus(STR_PERFORMED+NVS_MENU[c-1])
	
	screenNvsRecovery(file)



def screenEapKeyRecovery(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_ABOUT_EAPKEYS))
	
	print(UI.warning(STR_INFO_EAPKEYS + '\n' + STR_IMMEDIATLY))
	
	print(UI.getTab(STR_EAP_KEYS))
	print(STR_FILENAME+file+'\n')
	
	with open(file,'r+b') as f:
		
		magic_a = SFlash.getNorData(f, 'EAP_MGC')
		key_a = SFlash.getNorData(f, 'EAP_KEY')
		
		magic_b = SFlash.getNorDataB(f, 'EAP_MGC')
		key_b = SFlash.getNorDataB(f, 'EAP_KEY')
		
		print(UI.highlight(' Key A\n'))
		print(' Magic [%s] %s\n'%(Utils.hex(magic_a,''), STR_OK if magic_a == SFlash.SFLASH_AREAS['EAP_MGC']['n'] else STR_DIFF ))
		
		for i in range(0,len(key_a),0x20):
			print(' '+Utils.hex(key_a[i:i+0x20],''))
		
		print()
		
		print(UI.highlight(' Key B\n'))
		print(' Magic [%s] %s\n'%(Utils.hex(magic_b,''), STR_OK if magic_b == SFlash.SFLASH_AREAS['EAP_MGC']['n'] else STR_DIFF ))
		
		for i in range(0,len(key_b),0x20):
			print(' '+Utils.hex(key_b[i:i+0x20],''))
		
		UI.showStatus()
		
		print(UI.DIVIDER)
		UI.showMenu(MENU_EAP_KEYS,1)
		print('\n'+UI.dark(STR_EXPERIMENTAL))
		print(UI.DIVIDER)
		UI.showMenu([STR_GO_BACK])
		
		choice = input(STR_CHOICE)
		
		try:
			c = int(choice)
		except:
			c = -1
		
		if c == 0:
			return
		elif c == 1:
			SFlash.setNorData(f, 'EAP_KEY', key_b)
		elif c == 2:
			SFlash.setNorDataB(f, 'EAP_KEY', key_a)
		elif c == 3:
			SFlash.setNorData(f, 'EAP_MGC', SFlash.SFLASH_AREAS['EAP_MGC']['n'])
		elif c == 4:
			SFlash.setNorDataB(f, 'EAP_MGC', SFlash.SFLASH_AREAS['EAP_MGC']['n'])
		elif c == 5:
			key = Utils.genRandBytes(0x40)
			SFlash.setNorData(f, 'EAP_KEY', key + b'\xFF'*0x20)
			SFlash.setNorDataB(f, 'EAP_KEY', key + b'\xFF'*0x20)
		elif c == 6:
			key = Utils.genRandBytes(0x60)
			SFlash.setNorData(f, 'EAP_KEY', key)
			SFlash.setNorDataB(f, 'EAP_KEY', key)
		elif c == 7:
			SFlash.setNorDataB(f, 'EAP_MGC', b'\xFF'*SFlash.SFLASH_AREAS['EAP_MGC']['l'])
			SFlash.setNorDataB(f, 'EAP_KEY', b'\xFF'*SFlash.SFLASH_AREAS['EAP_KEY']['l'])
		
		if c >= 1 and c <= len(MENU_EAP_KEYS):
			UI.setStatus(STR_PERFORMED+MENU_EAP_KEYS[c-1])
	
	screenEapKeyRecovery(file)



def screenEmcCFW(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_ABOUT_EMC_CFW))
	print(UI.warning(STR_INFO_EMC_CFW))
	
	print(UI.getTab(STR_EMC_CFW))
	
	with open(file, 'rb') as f:
		data = f.read()
		sku = SFlash.getNorData(f, 'SKU', True)
		model = SFlash.getModel(f)
		slot = SFlash.getActiveSlot(f).upper()
		
		print(' SKU: %s / Slot: %s'%(sku, slot))
		
		if not model in [11, 10]:
			print(STR_EMC_CFW_WARN)
			input(STR_BACK)
			return
		
		b = False
		if slot == 'B':
			b = input(STR_INPUT_USE_SLOTB+STR_Y_OR_CANCEL).lower()
			UI.clearInput()
		
		emc_part_name = 's0_emc_ipl_' + ('b' if b == 'y' else 'a')
		emc_part = SFlash.getNorPartition(f, emc_part_name)
	
	folder = os.path.dirname(file)
	filename = os.path.splitext(os.path.basename(file))[0]
	
	
	emc_fw = b''
	fw_offset = 0
	fw_size = 0
	
	entries = Slb2.getGet2BLSInfo(emc_part)['entries']
	
	for key in entries:
		entry = entries[key]
		if entry['name'] == 'C0000001':
			fw_offset = entry['offset']
			fw_size = entry['size']
			emc_fw = emc_part[fw_offset:fw_offset+fw_size]
			break
	
	if len(emc_fw) == 0:
		print(STR_EMC_NOT_FOUND)
		input(STR_BACK)
		return
	
	save_all = True if input(STR_INPUT_SAVE_IM+STR_Y_OR_CANCEL).lower() == 'y' else False
	UI.clearInput()
	
	# Decrypting current emc fw
	print('\n'+UI.highlight(STR_DECRYPTING)+'\n')
	
	decrypted_fw = Encdec.decrypt(emc_fw)
	
	if save_all:
		out_file = os.path.join(folder,'emc_fw_orig.bin')
		Utils.savePatchData(out_file, decrypted_fw)
		print('\n'+UI.green(STR_SAVED_TO%out_file))
	
	# Patching (2 patches)
	print('\n'+UI.highlight(STR_PATCHING)+' [God Mode]\n')
	
	p1 = [b"\x03\x00\xFD\x00", b"\x0F\x00\xFD\x00"]
	patched_fw = decrypted_fw.replace(p1[0], p1[1])
	print(' %s => %s'%(Utils.hex(p1[0],''),Utils.hex(p1[1],'')))
	
	p2 = [b"\x07\x00\xFD\x00", b"\x0F\x00\xFD\x00"]
	patched_fw = patched_fw.replace(p2[0], p2[1])
	print(' %s => %s'%(Utils.hex(p2[0],''),Utils.hex(p2[1],'')))
	
	if save_all:
		out_file = os.path.join(folder,'emc_cfw.bin')
		Utils.savePatchData(out_file, patched_fw)
		print('\n'+UI.green(STR_SAVED_TO%out_file))
	
	# Encrypt and save patched data
	print('\n'+UI.highlight(STR_ENCRYPTING)+'\n')
	
	encrypted_fw = Encdec.encrypt(patched_fw)
	
	if save_all:
		out_file = os.path.join(folder,'emc_cfw_enc.bin')
		Utils.savePatchData(out_file, encrypted_fw)
		print('\n'+UI.green(STR_SAVED_TO%out_file))
	
	if fw_size != len(encrypted_fw):
		print('\n'+UI.warning(STR_SIZES_MISMATCH))
	
	out_file = os.path.join(folder,filename+'_emc_cfw.bin')
	Utils.savePatchData(out_file, data, [{'o':fw_offset + SFlash.SFLASH_PARTITIONS[emc_part_name]['o'],'d':encrypted_fw}])
	print('\n'+UI.highlight(STR_SAVED_TO%out_file))
	
	input(STR_BACK)



def screenHddKey(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_ABOUT_EAP))
	print(UI.warning(STR_INFO_HDD_EAP))
	
	mode = input('\n'+STR_USE_NEWBLOBS+STR_Y_OR_CANCEL).lower()
	UI.clearInput(2)
	
	print(UI.getTab(STR_HDD_KEY))
	
	with open(file,'rb') as f:
		smi = int.from_bytes(SFlash.getNorData(f, 'SMI'), "little")
		
		magic = SFlash.getNorData(f, 'EAP_MGC')
		key = SFlash.getNorData(f, 'EAP_KEY')
	
	print(' RAW hdd key\n')
	for i in range(0,len(key),0x20):
		print(' '+Utils.hex(key[i:i+0x20],''))
	
	print(UI.highlight('\n Key magic - ')+'%s\n'%(STR_OK if magic == SFlash.SFLASH_AREAS['EAP_MGC']['n'] else STR_DIFF))
	
	keys = Encdec.hddEapKey(key, smi, True if mode == 'y' else False)
	print()
	if keys == -1:
		print(STR_ABORT)
		input(STR_BACK)
	
	out = os.path.dirname(file) + os.sep + 'keys.bin'
	with open(out, 'wb') as k:
		k.write(keys['data'])
		k.write(keys['tweak'])
	
	print(UI.highlight(STR_SAVED_TO%out))
	
	input(STR_BACK)



def screenExtractNorDump(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_SFLASH_EXTRACT))
	
	with open(file, 'rb') as f:
		
		sn = SFlash.getNorData(f, 'SN', True)
		folder = os.path.dirname(file) + os.sep + sn + os.sep
		
		if not os.path.exists(folder):
			os.makedirs(folder)
		
		info = ''
		data = SFlash.getSFlashInfo(file)
		for key in data:
			info += '%s : %s\n'%(key.ljust(12,' '),data[key])
		info += '\n'
		
		print(STR_EXTRACTING%sn+'\n')
		
		i = 0
		for k in SFlash.SFLASH_PARTITIONS:
			p = SFlash.SFLASH_PARTITIONS[k]
			i += 1
			print(' %2d: %16s > %s'%(i, k, p['n']))
			info += '%2d: %16s > %s\n'%(i, k, p['n'])
			
			with open(folder + p['n'], 'wb') as out:
				out.write(SFlash.getNorPartition(f, k))
		
		with open(folder + Utils.INFO_FILE_SFLASH, 'w') as txt:
			txt.write(info)
		
		print('\n'+STR_SAVED_TO%folder)
	
	print('\n'+STR_DONE)
	
	input(STR_BACK)



def screenBuildNorDump(folder):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_SFLASH_BUILD))
	
	if not os.path.exists(folder):
		print(STR_NO_FOLDER%folder+'\n\n'+STR_ABORT)
		input(STR_BACK)
		return
	
	print(STR_FILES_CHECK.format(folder)+'\n')
	
	found = 0
	
	i = 0
	for k in SFlash.SFLASH_PARTITIONS:
		p = SFlash.SFLASH_PARTITIONS[k]
		i += 1
		status = STR_OK
		
		file = folder+os.sep+p['n']
		if not os.path.exists(file):
			status = STR_NOT_FOUND
		elif os.stat(file).st_size != p['l']:
			status = STR_BAD_SIZE
		else:
			found += 1
		
		print(' %2d: %20s - %s'%(i, p['n'], status))
	
	print()
	
	if found == len(SFlash.SFLASH_PARTITIONS):
		
		"""
		sn = '0'*17
		with open(folder+os.sep+SFlash.SFLASH_PARTITIONS['s0_nvs']['n'],'rb') as nvs:
			nvs.seek(0x4030)
			sn = nvs.read(17)
		"""
		
		fname = os.path.join(folder, 'sflash0.bin')
		
		print(STR_BUILDING%fname)
		
		out = open(fname,"wb")
		
		for k in SFlash.SFLASH_PARTITIONS:
			file = folder+os.sep+SFlash.SFLASH_PARTITIONS[k]['n']
			with open(file, 'rb') as f:
				out.write(f.read())
		
		out.close()
		
		print('\n'+STR_DONE)
	else:
		print(STR_ABORT)
	
	input(STR_BACK)



def screenAdvSFlashTools(file):
	
	with open(file, 'rb') as f:
		sn = SFlash.getNorData(f, 'SN', True)
	
	folder = os.path.dirname(file) + os.sep + sn

	while True:

		UI.clearScreen()
		print(TITLE+UI.getTab(STR_ADDITIONAL))
		
		UI.showMenu(MENU_SFLASH_ADV_ACTIONS,1)
		
		UI.showStatus()
		
		choice = input(STR_CHOICE)
		
		if choice == '':
			return
		elif choice == '1':
			screenExtractNorDump(file)
		elif choice == '2':
			screenBuildNorDump(folder)
		elif choice == '3':
			screenNvsRecovery(file)
		elif choice == '4':
			screenEapKeyRecovery(file)
		elif choice == '5':
			screenHddKey(file)
		elif choice == '6':
			screenEmcCFW(file)
		elif choice == '7':
			screenValidate(file)
		elif choice == '8':
			screenPartitionRecovery(file)
		
