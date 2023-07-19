import struct
from Crypto.Cipher import AES
from Crypto.Hash import SHA, HMAC
from utils.utils import getHex as hx


CIPHERKEYSEMC	= bytes.fromhex('5F74FE7790127FECF82CC6E6D91FA2D1') # FULL
CIPHERKEYSEAP	= bytes.fromhex('581A75D7E9C01F3C1BD7473DBD443B98')
HASHERKEYEMC	= bytes.fromhex('73FE06F3906B05ECB506DFB8691F9F54')
HASHERKEYEAP	= bytes.fromhex('824D9BB4DBA3209294C93976221249E4')
ZEROS128		= bytes.fromhex('00000000000000000000000000000000')



def aes_decrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).decrypt(input)
    
def aes_encrypt_cbc(key, iv, input):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(input)

def emc_decrypt_header(hdr):
    return hdr[:0x30] + aes_decrypt_cbc(CIPHERKEYSEMC, ZEROS128, hdr[0x30:0x80])
    
def emc_encrypt_header(hdr):
    return hdr[:0x30] + aes_encrypt_cbc(CIPHERKEYSEMC, ZEROS128, hdr[0x30:0x80])
    
def eap_decrypt_header(hdr):
    return hdr[:0x30] + aes_decrypt_cbc(CIPHERKEYSEAP, ZEROS128, hdr[0x30:0x80])
    
def eap_encrypt_header(hdr):
    return hdr[:0x30] + aes_encrypt_cbc(CIPHERKEYSEAP, ZEROS128, hdr[0x30:0x80])



def decrypt(data):
	#data = f.read(0x80)
	pad = 16
	type = data[7:8]
	
	print(' Type'.ljust(pad)+': 0x',end='')
	if type == b'\x48':
		print('%s [EMC]'%hx(type))
		type = 'emc'
	elif type == b'\x68':
		print('%s [EAP]'%hx(type))
		type = 'eap'
	else:
		print('%s [UNK]'%hx(type))
		return b''
	
	hdr = emc_decrypt_header(data[:0x80]) if type == 'emc' else eap_decrypt_header(data[:0x80])
	
	body_aes_key  = hdr[0x30:0x40]
	body_hmac_key = hdr[0x40:0x50]
	body_hmac = hdr[0x50:0x64]
	zeroes = hdr[0x64:0x6C]
	
	print(' ZERO'.ljust(pad)+': %s'%hx(zeroes,''))
	
	header_hmac = hdr[0x6C:0x80]
	body_len = struct.unpack('<L', hdr[0xc:0x10])[0]
	
	print(' Body'.ljust(pad)+': %d bytes'%body_len)
	
	ehdr = hdr[:0x6C]
	ebody = data[0x80:0x80 + body_len]
	bhmac = HMAC.new(body_hmac_key, ebody, SHA)
	hhmac = HMAC.new(HASHERKEYEMC, ehdr, SHA) if type == 'emc' else HMAC.new(HASHERKEYEAP, ehdr, SHA)
	body = aes_decrypt_cbc(body_aes_key, ZEROS128, ebody)
	
	print(' HHMAC'.ljust(pad)+': %s'%hhmac.hexdigest())
	print(' BHMAC'.ljust(pad)+': %s'%bhmac.hexdigest())
	
	print(' Header HMAC'.ljust(pad)+': %s'%hx(header_hmac,''))
	print(' Body HMAC'.ljust(pad)+': %s'%hx(body_hmac,''))
	
	return hdr + body



def encrypt(data):
	
	type = data[7:8]
	pad = 16
	
	print(' Type'.ljust(pad)+': 0x',end='')
	if type == b'\x48':
		print('%s [EMC]'%hx(type))
		type = 'emc'
	elif type == b'\x68':
		print('%s [EAP]'%hx(type))
		type = 'eap'
	else:
		print('%s [UNK]'%hx(type))
		return b''
	
	body_len = struct.unpack('<L', data[0xc:0x10])[0]
	body = data[0x80:0x80+body_len]
	body_aes_key  = data[0x30:0x40]
	
	ebody = aes_encrypt_cbc(body_aes_key, ZEROS128, body)
	body_hmac_key = data[0x40:0x50]
	bhmac = HMAC.new(body_hmac_key, ebody, SHA)
	
	hdr = (data[0:0x50] + bytes.fromhex(bhmac.hexdigest()) + data[0x64:0x6C])
	hhmac = HMAC.new(HASHERKEYEMC, hdr, SHA) if type == 'emc' else HMAC.new(HASHERKEYEAP, hdr, SHA)
	hdr = (hdr + bytes.fromhex(hhmac.hexdigest()))
	hdr = emc_encrypt_header(hdr) if type == 'emc' else eap_encrypt_header(hdr)
	
	print(' HHMAC'.ljust(pad)+': %s'%hhmac.hexdigest())
	print(' BHMAC'.ljust(pad)+': %s'%bhmac.hexdigest())
	
	return hdr + ebody