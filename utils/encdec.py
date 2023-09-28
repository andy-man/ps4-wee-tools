#==========================================================
# Encrypt / decrypt utils
# part of ps4 wee tools project
#==========================================================
import struct
import utils.utils as Utils
from lang._i18n_ import *
from Crypto.Cipher import AES
from Crypto.Hash import SHA, HMAC, SHA256

# EMC cfw key stuff

CIPHERKEYSEMC	= bytes.fromhex('5F74FE7790127FECF82CC6E6D91FA2D1') # FULL
CIPHERKEYSEAP	= bytes.fromhex('581A75D7E9C01F3C1BD7473DBD443B98')
HASHERKEYEMC	= bytes.fromhex('73FE06F3906B05ECB506DFB8691F9F54')
HASHERKEYEAP	= bytes.fromhex('824D9BB4DBA3209294C93976221249E4')
ZEROS128		= bytes.fromhex('00000000000000000000000000000000')

# HDD EAP key stuff

P_SEED_KEY		= bytes.fromhex('E973A44C578757A73492625D2CE2D76B')
P_SEED			= bytes.fromhex('DF0C2552DFC7F4F089B9D52DAA0E572A')
EAP_K1_SEED		= bytes.fromhex('7A49D928D2243C9C4D6E1EA8F5B4E229317E0DCAD2ABE5C56D2540572FB4B6E3')
EAP_K2_SEED		= bytes.fromhex('921CE9C8184C5DD476F4B5D3981F7E2F468193ED071E19FFFD66B693534689D6')

EAP_HDD_KEY_HEAD = b'SCE_EAP_HDD__KEY'
EAP_HDD_KEY_BODY = bytes.fromhex('BB6CD66DDC671FAC3664F7BF5049BAA8C4687904BC31CF4F2F4E9F89FA458793811745E7C7E80D460FAF2326550BD7E4D2A0A0D9729DE5D2117D70676F1D55748DC17CDF29C86A855F2AE9A1AD3E915F0000000000000000000000000000000000000000000000000000000000000000')
EAP_HDD_KEY_BLOB = EAP_HDD_KEY_HEAD + EAP_HDD_KEY_BODY

KEY_BLOB = {
	'enc': bytes.fromhex('E073B691E177D39642DF2E1D583D0E9A5A49EDF72BE9412E2B433E51490CE973234B84F49E949F03727331D5456F4598F2EDE6D0C11483B84CE3283243D0DE9DC379E915301A805DFAEB292B30374C9BF1C59041509BF11D215C35D5C08E3330807C8229C930FAB88672C4CF7DACA881C323D72346CA07921DB806FC242A2ED1'),
	'sig': bytes.fromhex('ED4F32C095847C6D3143EFFD61E7582F75F24465855C4E94DAF34885D8D03463'),
	'iv' : bytes.fromhex('3286EA97F3E92C434E1DC170C9289003'),
}

NEW_KEY_BLOB = {
	'enc': bytes.fromhex('CFFDCB6ECAE612B7A30A9EDBD8F77E261D629DE5E6CA3F22F439211AC033884F4B5D7D16D0A6F65D3173A2586CF819C7C6F437444C1D9499F6EBC4145E0BBAABC1DE7C63ED1F5A1E1946358C7F181B1FAB6DAB31195D8E611A1CB81B9ACF8B38FF21029FAB568C7A1BCC3E2FBEB25B13F1AFD6A3599EEF09EAEBE32684FDDA29'),
	'sig': bytes.fromhex('4798B78DD422601F26A32A1FEC5CAB8B256E50958E0B11A31D77DEE201D4D00E'),
	'iv' : bytes.fromhex('462500ECC487F0A8C2F39511E020CC59'),
}



def aes_decrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).decrypt(input)

def aes_encrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(input)

def aes_decrypt_ecb(key, data):
	return AES.new(key, AES.MODE_ECB).decrypt(data)

def aes_encrypt_ecb(key, data):
	return AES.new(key, AES.MODE_ECB).encrypt(data)

def emc_decrypt_header(hdr):
    return hdr[:0x30] + aes_decrypt_cbc(CIPHERKEYSEMC, ZEROS128, hdr[0x30:0x80])
    
def emc_encrypt_header(hdr):
    return hdr[:0x30] + aes_encrypt_cbc(CIPHERKEYSEMC, ZEROS128, hdr[0x30:0x80])
    
def eap_decrypt_header(hdr):
    return hdr[:0x30] + aes_decrypt_cbc(CIPHERKEYSEAP, ZEROS128, hdr[0x30:0x80])
    
def eap_encrypt_header(hdr):
    return hdr[:0x30] + aes_encrypt_cbc(CIPHERKEYSEAP, ZEROS128, hdr[0x30:0x80])

def hmac_sha256(key, data):
	return HMAC.new(key=key, msg=data, digestmod=SHA256).digest()



def checkType(type):
	
	print(' Type'.ljust(16)+': 0x',end='')
	if type == b'\x48':
		print('%s [EMC]'%Utils.hex(type))
		type = 'emc'
	elif type == b'\x68':
		print('%s [EAP]'%Utils.hex(type))
		type = 'eap'
	else:
		print('%s [UNK]'%Utils.hex(type))
		type = b''
	
	return type


def decrypt(data):
	
	pad = 16
	
	type = checkType(data[7:8])
	if not type:
		return type
	
	hdr = emc_decrypt_header(data[:0x80]) if type == 'emc' else eap_decrypt_header(data[:0x80])
	
	body_aes_key  = hdr[0x30:0x40]
	body_hmac_key = hdr[0x40:0x50]
	body_hmac = hdr[0x50:0x64]
	zeroes = hdr[0x64:0x6C]
	
	print(' ZERO'.ljust(pad)+': %s'%Utils.hex(zeroes,''))
	
	header_hmac = hdr[0x6C:0x80]
	body_len = struct.unpack('<L', hdr[0xc:0x10])[0]
	
	print(' Body'.ljust(pad)+': %d bytes'%body_len)
	
	ehdr = hdr[:0x6C]
	ebody = data[0x80:0x80 + body_len]
	bhmac = HMAC.new(body_hmac_key, ebody, SHA)
	hhmac = HMAC.new(HASHERKEYEMC, ehdr, SHA) if type == 'emc' else HMAC.new(HASHERKEYEAP, ehdr, SHA)
	body = aes_decrypt_cbc(body_aes_key, ZEROS128, ebody)
	
	hhmac = hhmac.hexdigest().upper()
	bhmac = bhmac.hexdigest().upper()
	print(' HHMAC'.ljust(pad)+': %s %s'%(hhmac, STR_OK if hhmac == Utils.hex(header_hmac,'') else STR_FAIL))
	print(' BHMAC'.ljust(pad)+': %s %s'%(bhmac, STR_OK if bhmac == Utils.hex(body_hmac,'') else STR_FAIL))
	
	return hdr + body



def encrypt(data):
	
	pad = 16
	
	type = checkType(data[7:8])
	if not type:
		return type
	
	body_len = struct.unpack('<L', data[0xc:0x10])[0]
	body = data[0x80:0x80+body_len]
	body_aes_key  = data[0x30:0x40]
	
	ebody = aes_encrypt_cbc(body_aes_key, ZEROS128, body)
	body_hmac_key = data[0x40:0x50]
	bhmac = HMAC.new(body_hmac_key, ebody, SHA)
	
	print(' Body'.ljust(pad)+': %d bytes'%body_len)
	
	hdr = (data[0:0x50] + bytes.fromhex(bhmac.hexdigest()) + data[0x64:0x6C])
	hhmac = HMAC.new(HASHERKEYEMC, hdr, SHA) if type == 'emc' else HMAC.new(HASHERKEYEAP, hdr, SHA)
	hdr = (hdr + bytes.fromhex(hhmac.hexdigest()))
	hdr = emc_encrypt_header(hdr) if type == 'emc' else eap_encrypt_header(hdr)
	
	print(' HHMAC'.ljust(pad)+': %s'%hhmac.hexdigest().upper())
	print(' BHMAC'.ljust(pad)+': %s'%bhmac.hexdigest().upper())
	
	return hdr + ebody



def hddEapKey(eap_key, smi, use_new_blob=False):
	
	info = {
		'Use new keys':STR_YES if use_new_blob else STR_NO,
		'SMI':	"0x%X"%smi
	}
	
	# generate portability key
	p_key = aes_encrypt_ecb(P_SEED_KEY, P_SEED)
	# generate eap_hdd_keys from seeds
	eap_hdd_key_blob_key1 = aes_encrypt_ecb(p_key, EAP_K1_SEED)
	eap_hdd_key_blob_key2 = aes_encrypt_ecb(p_key, EAP_K2_SEED)
	
	# length check
	
	eap_hdd_wrapped_key = eap_key[:0x40] if eap_key[0x40:0x50] == b'\xFF' * 16 else eap_key[:0x60]
	
	info['Key length'] = '0x%X'%len(eap_hdd_wrapped_key)
	
	# verify and decrypt eap key blob
	eap_hdd_key_blob_enc = NEW_KEY_BLOB['enc'] if use_new_blob else KEY_BLOB['enc']
	eap_hdd_key_blob_sig = NEW_KEY_BLOB['sig'] if use_new_blob else KEY_BLOB['sig']
	eap_hdd_key_blob_iv  = NEW_KEY_BLOB['iv'] if use_new_blob else KEY_BLOB['iv']
	
	selected_key = eap_hdd_key_blob_key1
	computed_signature = hmac_sha256(selected_key[0x10:0x20], eap_hdd_key_blob_enc)
	
	info['Signature'] = STR_OK
	if computed_signature != eap_hdd_key_blob_sig:
		info['Signature'] = STR_FAIL
		selected_key = eap_hdd_key_blob_key2
		computed_signature = hmac_sha256(selected_key[0x10:0x20], eap_hdd_key_blob_enc)
		if computed_signature != eap_hdd_key_blob_sig:
			showTable(info)
			return -1
	
	eap_hdd_key_blob = aes_decrypt_cbc(selected_key[0x00:0x10], eap_hdd_key_blob_iv, eap_hdd_key_blob_enc)
	info['Key check'] = STR_OK
	if not eap_hdd_key_blob.startswith(EAP_HDD_KEY_HEAD):
		info['Key check'] = STR_FAIL
		showTable(info)
		return -1
	
	eap_hdd_key_blob = EAP_HDD_KEY_BLOB
	
	key = eap_hdd_key_blob[0x60:0x70] if use_new_blob else eap_hdd_key_blob[0x50:0x60]
	eap_hdd_unwrapped_key = aes_decrypt_cbc(key, b'\x00' * 0x10, eap_hdd_wrapped_key[:0x40])
	
	offset = 0x10 if (smi == 0xFFFFFFFF or smi < 0x4000000) else 0x20
	eap_hdd_unwrapped_key_dec = aes_decrypt_cbc(eap_hdd_key_blob[offset:offset + 0x10], b'\x00' * 0x10, eap_hdd_unwrapped_key)
	
	if eap_hdd_unwrapped_key_dec[0x10:0x20] != b'\x00' * 0x10:
		eap_hdd_unwrapped_key_dec = aes_decrypt_cbc(eap_hdd_key_blob[offset:offset + 0x10], b'\x00' * 0x10, eap_hdd_wrapped_key[:0x10])
	
	key_data = eap_hdd_key_blob[0x40:0x50] if use_new_blob else eap_hdd_key_blob[0x30:0x40]
	eap_partition_key = hmac_sha256(eap_hdd_unwrapped_key_dec[:0x10], key_data)
	
	tweak_key = eap_partition_key[0x00:0x10]
	data_key = eap_partition_key[0x10:0x20]
	
	info['XTS data key'] = Utils.hex(data_key,'')
	info['XTS tweak key'] = Utils.hex(tweak_key,'')
	
	UI.showTable(info)
	
	return {'tweak':tweak_key,'data':data_key}
