#==============================================================
# PS4 Nor Tools
# part of ps4 wee tools project
#==============================================================
import os
from lang._i18n_ import *
from utils.nor import *
import data.data as Data
import utils.slb2 as Slb2
import utils.encdec as Encdec
import tools.Tools as Tools
import tools.NorTools as NorTools



def screenAdvNorTools(file):
	os.system('cls')
	print(TITLE+getTab(STR_ADDITIONAL))
	
	with open(file, 'rb') as f:
		sn = getNorData(f, 'SN').decode('utf-8','ignore')
	
	folder = os.path.dirname(file) + os.sep + sn
	
	getMenu(MENU_ADDTIONAL,1)
	
	showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == '':
		return
	elif choice == '1':
		screenExtractNorDump(file)
	elif choice == '2':
		screenBuildNorDump(folder)
	elif choice == '3':
		screenEapKeyRecovery(file)
	elif choice == '4':
		screenHddKey(file)
	elif choice == '5':
		screenValidate(file)
	elif choice == '6':
		screenEmcCFW(file)
	
	screenAdvNorTools(file)



def screenValidate(file):
	os.system('cls')
	print(TITLE + getTab(STR_NOR_VALIDATOR))
	
	
	with open(file,'rb') as f:
		
		fw = getNorFW(f)['c']
		slot = 'A' if getNorData(f, 'ACT_SLOT')[0] == 0x00 else 'B'
		
		magics = {
			'header'	: STR_OK if checkNorPartMagic(f, 's0_header') else STR_DIFF,
			'MBR1'		: STR_OK if checkNorPartMagic(f, 's0_MBR1') else STR_DIFF,
			'MBR2'		: STR_OK if checkNorPartMagic(f, 's0_MBR2') else STR_DIFF,
		}
		
		parts_info = {
			'emc_ipl_a'	: {'md5':getNorPartitionMD5(f, 's0_emc_ipl_a'), 'var':Data.EMC_IPL_MD5},
			'emc_ipl_b'	: {'md5':getNorPartitionMD5(f, 's0_emc_ipl_b'), 'var':Data.EMC_IPL_MD5},
			'eap_kbl'	: {'md5':getNorPartitionMD5(f, 's0_eap_kbl'), 'var':Data.EAP_KBL_MD5},
			'wifi'		: {'md5':getNorPartitionMD5(f, 's0_wifi'), 'var':Data.TORUS_FW_MD5},
		}
	
	print(STR_FW_VERSION.format(fw,slot)+'\n')
	
	print(highlight(STR_MAGICS_CHECK)+'\n')
	showTable(magics,10)
	print()
	
	print(highlight(STR_PARTITIONS_CHECK)+'\n')
	
	for k in parts_info:
		md5 = parts_info[k]['md5']
		var = parts_info[k]['var']
		if md5 in var:
			if fw in var[md5]['fw']:
				parts_info[k] = STR_IS_PART_VALID.format(md5, STR_OK, STR_OK)
			else:
				parts_info[k] = STR_IS_PART_VALID.format(md5, STR_OK, var[md5]['fw'][0] if len(var[md5]['fw']) == 1 else (var[md5]['fw'][0]+' <-> '+var[md5]['fw'][-1]))
		else:
			parts_info[k] = STR_IS_PART_VALID.format(md5, STR_FAIL, STR_FAIL)
	
	showTable(parts_info,10)
	print()
	
	print(highlight(STR_ENTROPY)+'\n')
	#stats = {'ent':0, 'ff':0, '00':0}
	stats = entropy(file)
	print('\r',end='')
	
	info = {
		
		'Entropy'	: '{:.5f}'.format(stats['ent']),
		'0xFF'		: '{:.2f}%'.format(stats['ff']*100),
		'0x00'		: '{:.2f}%'.format(stats['00']*100),
		'Other'		: '{:.2f}%'.format((1 - stats['ff'] - stats['00'])*100),
	}
	
	
	showTable(info,10)
	
	input(STR_BACK)



def screenEapKeyRecovery(file):
	os.system('cls')
	print(TITLE+getTab(STR_WARNING))
	
	print(warning(STR_IMMEDIATLY))
	
	print(getTab(STR_EAP_KEYS))
	print(STR_FILENAME+file+'\n')
	
	with open(file,'r+b') as f:
		
		magic_a = getNorData(f, 'EAP_MGC')
		key_a = getNorData(f, 'EAP_KEY')
		
		magic_b = getNorDataB(f, 'EAP_MGC')
		key_b = getNorDataB(f, 'EAP_KEY')
		
		print(highlight(' Key A\n'))
		print(' Magic [%s] %s\n'%(getHex(magic_a,''), STR_OK if magic_a == NOR_AREAS['EAP_MGC']['n'] else STR_DIFF ))
		
		for i in range(0,len(key_a),0x20):
			print(' '+getHex(key_a[i:i+0x20],''))
		
		print()
		
		print(highlight(' Key B\n'))
		print(' Magic [%s] %s\n'%(getHex(magic_b,''), STR_OK if magic_b == NOR_AREAS['EAP_MGC']['n'] else STR_DIFF ))
		
		for i in range(0,len(key_b),0x20):
			print(' '+getHex(key_b[i:i+0x20],''))
		
		showStatus()
		
		print(DIVIDER)
		getMenu(MENU_EAP_KEYS,1)
		getMenu([STR_CANCEL])
		print('\n'+dark(STR_EXPERIMENTAL))
		
		choice = input(STR_CHOICE)
		
		try:
			c = int(choice)
		except:
			c = -1
		
		if c == 0:
			return
		elif c == 1:
			setNorData(f, 'EAP_KEY', key_b)
		elif c == 2:
			setNorDataB(f, 'EAP_KEY', key_a)
		elif c == 3:
			setNorData(f, 'EAP_MGC', NOR_AREAS['EAP_MGC']['n'])
		elif c == 4:
			setNorDataB(f, 'EAP_MGC', NOR_AREAS['EAP_MGC']['n'])
		elif c == 5:
			key = genRandBytes(0x40)
			setNorData(f, 'EAP_KEY', key + b'\xFF'*0x20)
			setNorDataB(f, 'EAP_KEY', key + b'\xFF'*0x20)
		elif c == 6:
			key = genRandBytes(0x60)
			setNorData(f, 'EAP_KEY', key)
			setNorDataB(f, 'EAP_KEY', key)
		elif c == 7:
			setNorDataB(f, 'EAP_MGC', b'\xFF'*NOR_AREAS['EAP_MGC']['l'])
			setNorDataB(f, 'EAP_KEY', b'\xFF'*NOR_AREAS['EAP_KEY']['l'])
		
		if c >= 1 and c <= len(MENU_EAP_KEYS):
			setStatus(STR_PERFORMED+MENU_EAP_KEYS[c-1])
	
	screenEapKeyRecovery(file)



def screenEmcCFW(file):
	os.system('cls')
	print(TITLE+getTab(STR_ABOUT_EMC_CFW))
	print(warning(STR_INFO_EMC_CFW))
	
	print(getTab(STR_EMC_CFW))
	
	with open(file, 'rb') as f:
		data = f.read()
		sku = getNorData(f, 'SKU')
		print(' SKU '+sku.decode('utf-8','ignore'))
		
		if sku[4:6] != b'11' and sku[4:6] != b'10':
			print(STR_EMC_CFW_WARN)
			input(STR_BACK)
			return
		
		emc_part = getNorPartition(f, 's0_emc_ipl_a')
	
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
	
	save_all = True if input(STR_INPUT_SAVE_IM) == 'y' else False
	clearInput()
	
	# Decrypting current emc fw
	print('\n'+highlight(STR_DECRYPTING)+'\n')
	
	decrypted_fw = Encdec.decrypt(emc_fw)
	
	if save_all:
		out_file = os.path.join(folder,'emc_fw_orig.bin')
		savePatchData(out_file, decrypted_fw)
		print('\n'+green(STR_SAVED_TO.format(out_file)))
	
	# Patching (2 patches)
	print('\n'+highlight(STR_PATCHING)+' [God Mode]\n')
	
	p1 = [b"\x03\x00\xFD\x00", b"\x0F\x00\xFD\x00"]
	patched_fw = decrypted_fw.replace(p1[0], p1[1])
	print(' %s => %s'%(getHex(p1[0],''),getHex(p1[1],'')))
	
	p2 = [b"\x07\x00\xFD\x00", b"\x0F\x00\xFD\x00"]
	patched_fw = patched_fw.replace(p2[0], p2[1])
	print(' %s => %s'%(getHex(p2[0],''),getHex(p2[1],'')))
	
	if save_all:
		out_file = os.path.join(folder,'emc_cfw.bin')
		savePatchData(out_file, patched_fw)
		print('\n'+green(STR_SAVED_TO.format(out_file)))
	
	# Encrypt and save patched data
	print('\n'+highlight(STR_ENCRYPTING)+'\n')
	
	encrypted_fw = Encdec.encrypt(patched_fw)
	
	if save_all:
		out_file = os.path.join(folder,'emc_cfw_enc.bin')
		savePatchData(out_file, encrypted_fw)
		print('\n'+green(STR_SAVED_TO.format(out_file)))
	
	if fw_size != len(encrypted_fw):
		print('\n'+warning(STR_SIZES_MISMATCH))
	
	out_file = os.path.join(folder,filename+'_emc_cfw.bin')
	savePatchData(out_file, data, [{'o':fw_offset + NOR_PARTITIONS['s0_emc_ipl_a']['o'],'d':encrypted_fw}])
	print('\n'+highlight(STR_SAVED_TO.format(out_file)))
	
	input(STR_BACK)



def screenHddKey(file):
	os.system('cls')
	print(TITLE+getTab(STR_ABOUT_EAP))
	print(warning(STR_INFO_HDD_EAP))
	
	mode = input('\n'+STR_USE_NEWBLOBS)
	clearInput(2)
	
	print(getTab(STR_HDD_KEY))
	
	with open(file,'rb') as f:
		smi = int.from_bytes(getNorData(f, 'SMI'), "big")
		
		magic = getNorData(f, 'EAP_MGC')
		key = getNorData(f, 'EAP_KEY')
	
	print(' RAW hdd key\n')
	for i in range(0,len(key),0x20):
		print(' '+getHex(key[i:i+0x20],''))
	
	print(highlight('\n Key magic - ')+'%s\n'%(STR_OK if magic == NOR_AREAS['EAP_MGC']['n'] else STR_DIFF))
	
	keys = Encdec.hddEapKey(key, smi, True if mode == 'y' else False)
	print()
	if keys == -1:
		print(STR_ABORT)
		input(STR_BACK)
	
	out = os.path.dirname(file) + os.sep + 'keys.bin'
	with open(out, 'wb') as k:
		k.write(keys['data'])
		k.write(keys['tweak'])
	
	print(highlight(STR_SAVED_TO.format(out)))
	
	input(STR_BACK)



def screenExtractNorDump(file):
	os.system('cls')
	print(TITLE+getTab(STR_NOR_EXTRACT))
	
	with open(file, 'rb') as f:
		
		sn = getNorData(f, 'SN').decode('utf-8','ignore')
		folder = os.path.dirname(file) + os.sep + sn + os.sep
		
		if not os.path.exists(folder):
			os.makedirs(folder)
		
		info = ''
		data = NorTools.getNorInfo(file)
		for key in data:
			info += '{} : {}\n'.format(key.ljust(12,' '),data[key])
		info += '\n'
		
		print(STR_EXTRACTING.format(sn)+'\n')
		
		i = 0
		for k in NOR_PARTITIONS:
			p = NOR_PARTITIONS[k]
			i += 1
			print(' {:2d}: {:16s} > {}'.format(i, k, p['n']))
			info += '{:2d}: {:16s} > {}\n'.format(i, k, p['n'])
			
			with open(folder + p['n'],'wb') as out:
				out.write(getData(f, p['o'], p['l']))
		
		with open(folder + INFO_FILE_NOR, 'w') as txt:
			txt.write(info)
		
		print('\n'+STR_SAVED_TO.format(folder))
	
	print('\n'+STR_DONE)
	
	input(STR_BACK)



def screenBuildNorDump(folder):
	os.system('cls')
	print(TITLE+getTab(STR_NOR_BUILD))
	
	if not os.path.exists(folder):
		print(STR_NO_FOLDER.format(folder)+'\n\n'+STR_ABORT)
		input(STR_BACK)
		return
	
	print(STR_FILES_CHECK.format(folder)+'\n')
	
	found = 0
	
	i = 0
	for k in NOR_PARTITIONS:
		p = NOR_PARTITIONS[k]
		i += 1
		status = STR_OK
		
		file = folder+os.sep+p['n']
		if not os.path.exists(file):
			status = STR_NOT_FOUND
		elif os.stat(file).st_size != p['l']:
			status = STR_BAD_SIZE
		else:
			found += 1
		
		print(' {:2d}: {:20s} - {}'.format(i, p['n'], status))
	
	print()
	
	if found == len(NOR_PARTITIONS):
		
		"""
		sn = '0'*17
		with open(folder+os.sep+NOR_PARTITIONS['s0_nvs']['n'],'rb') as nvs:
			nvs.seek(0x4030)
			sn = nvs.read(17)
		"""
		
		fname = os.path.join(folder, 'sflash0.bin')
		
		print(STR_BUILDING.format(fname))
		
		out = open(fname,"wb")
		
		for k in NOR_PARTITIONS:
			file = folder+os.sep+NOR_PARTITIONS[k]['n']
			with open(file, 'rb') as f:
				out.write(f.read())
		
		out.close()
		
		print('\n'+STR_DONE)
	else:
		print(STR_ABORT)
	
	input(STR_BACK)


