#==========================================================
# 2BLS utils
# part of ps4 wee tools project
#==========================================================
import os, ctypes



SLB2_HEADER = b'SLB2'
SLB2_BLOCK_SIZE = 0x200



class SLB2Header(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("magic",		ctypes.c_char * 4),		# "SLB2"
        ("version",		ctypes.c_uint32),		# ex: 1
        ("flags",		ctypes.c_uint32),		# ex: 0
        ("entries",		ctypes.c_uint32),
        ("blocks",		ctypes.c_uint32),
        ("reserved",	ctypes.c_uint32 * 3), 	# padding for alignment
    ]

class SLB2Entry(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("start",		ctypes.c_uint32),
        ("size",		ctypes.c_uint32),
        ("reserved",	ctypes.c_uint8 * 8), 	# padding for alignment
        ("name",		ctypes.c_char * 32)
    ]



def align(size, block):
	return size + (0 if size % block == 0 else block - (size % block))



def getGet2BLSInfo(data):
	e = {}
	h = {}
	
	header = SLB2Header.from_buffer_copy(data)
	
	h['magic']		= header.magic.decode('utf-8')
	h['version']	= header.version
	h['entries']	= header.entries
	h['blocks']		= header.blocks
	h['data']		= len(data)
	h['size']		= header.blocks * SLB2_BLOCK_SIZE
	
	for i in range(header.entries):
		offset = ctypes.sizeof(SLB2Header) + ctypes.sizeof(SLB2Entry) * i
		entry = SLB2Entry.from_buffer_copy(data[offset:offset + ctypes.sizeof(SLB2Entry)])
		
		e[i] = {
			'name':		entry.name.decode('utf-8'),
			'start':	entry.start,
			'offset':	entry.start * SLB2_BLOCK_SIZE,
			'size':		entry.size,
		}
	
	return {'header':h, 'entries':e}



def build2BLS(files):
	
	if len(files) == 0:
		return -1
	
	data = b''
	entries = b''
	
	hsize = ctypes.sizeof(SLB2Header) + ctypes.sizeof(SLB2Entry) * len(files)
	h_size = align(hsize, SLB2_BLOCK_SIZE)
	h_blocks = h_size // SLB2_BLOCK_SIZE
	
	last_block = h_blocks
	
	for i in range(len(files)):
		
		fname = os.path.basename(files[i])
		fsize = os.path.getsize(files[i])
		f_size = align(fsize,SLB2_BLOCK_SIZE)
		f_blocks = f_size // SLB2_BLOCK_SIZE
		f_padding = f_size - fsize
		
		entry = SLB2Entry(start=last_block, size=fsize, name=bytes(fname, 'ascii'))
		entries += bytes(entry)
		
		last_block += f_blocks
		
		with open(files[i],'rb') as f:
			data += f.read()
		
		if f_padding > 0:
			data += b'\x00'*f_padding
	
	e_padding = h_size - (ctypes.sizeof(SLB2Header) + len(entries))
	if e_padding > 0:
		entries += b'\x00'*e_padding
	
	header = SLB2Header()
	
	header.magic = SLB2_HEADER
	header.version = 1
	header.flags = 0
	header.entries = len(files)
	header.blocks = last_block
	
	return bytes(header) + entries + data
	