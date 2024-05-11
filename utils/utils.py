#==========================================================
# Common utils
# part of ps4 wee tools project
#==========================================================
import hashlib, os, sys, math, random, datetime
import lang._i18n_ as Lang

# Common consts

INFO_FILE_SFLASH	= '_sflash0_.txt'
INFO_FILE_2BLS		= '_2bls_.txt'
ROOT_PATH			= os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(__file__))

# Config stuff

class Config:

	cfg = {}
	file = ''
	path = ''
	
	def __init__(self, file='config.ini'):
		self.file = file
		self.path = os.path.realpath(file)
		self.load()

	def load(self, file = False):

		path = file if file else self.path

		if not os.path.isfile(path):
			self.cfg = {}
			return False
		
		with open(path, 'r') as f:
			lines = f.readlines()
		
		for line in lines:
			line = line.strip()
			if len(line) == 0:
				continue
			item = line.split('=')
			key = item[0].strip()
			val = '='.join(item[1:]) if len(item) >= 2 else ''
			if key: self.cfg[key] = val.strip()

		return len(self.cfg)

	def save(self, file = False):
		
		path = file if file else self.path

		try:
			with open(path, 'w') as f:
				for key in self.cfg:
					f.write(f'{key} = {self.cfg[key]}\n')
		except Exception as e:
			print('CFG Error:', e)
			return False

		return True
	
	def get(self, key, default=''):
		return self.cfg.get(key, default)
	
	def set(self, key, val):
		self.cfg[key] = val

APP_CONFIG = Config()

# Functions

def getEmcCmd(str):
	sum = 0
	for i in range(len(str)):
		sum += ord(str[i])
	return str + ':%02X'%(sum & 0xFF)


def ceil(a, b):
	return (a // b) + (1 if a % b else 0)


def checkCtrl(s, key):
	return ord(s) + 0x40 == ord(key)



def genRandBytes(size):
	return bytearray(random.getrandbits(8) for _ in range(size))



def getMemData(data, offset, lenght):
	if len(data) >= offset+lenght:
		return data[offset : offset+lenght]
	return b''



def getData(file, off, len):
	try:
		if isinstance(file, str):
			with open(file, 'rb') as f:
				f.seek(off)
				return f.read(len)
		else:
			file.seek(off)
			return file.read(len)
	except:
		return ''



def setData(file, off, val):
	try:
		if isinstance(file, str):
			with open(file, 'r+b') as f:
				f.seek(off)
				return f.write(val)
		else:
			file.seek(off)
			return file.write(val)
	except:
		return ''



def checkFileSize(file, size):
	if not file or not os.path.isfile(file):
		print(Lang.STR_FILE_NOT_EXISTS%file)
		input(Lang.STR_BACK)
		return False
	
	if os.stat(file).st_size != size:
		print(Lang.STR_INCORRECT_SIZE%file)
		input(Lang.STR_BACK)
		return False
	
	return True



def getFilePathWoExt(file, fix_spaces = False):
	folder = os.path.dirname(file)
	name = '.'.join(os.path.basename(file).split('.')[:-1])
	return folder + os.path.sep + (name.replace(' ','_') if fix_spaces else name)



def getFileMD5(file):
    f = open(file, 'rb')
    f.seek(0)
    with f:
        res = f.read()
        return hashlib.md5(res).hexdigest()



def getFilesList(path, ext = ''):
	flist = []
	for root, dirs, files in os.walk(path):
		for name in files:
			if ext:
				if name.lower().endswith(ext):
					flist.append(os.path.join(root, name))
			else:
				flist.append(os.path.join(root, name))
	
	return flist



def percent(part, whole):
	return 100 * float(part)/float(whole) if whole else 0



def compareData(d1, d2, step = 1):
	min = len(d1) if len(d1) < len(d2) else len(d2)
	ok = 0
	for i in range(0, min, step):
		if d1[i:i+step] == d2[i:i+step]:
			ok += 1
	return percent(ok, min // step)



def compareDataWithFiles(data, file_list, buf = 1, show_progress = False):
	
	items = []
	for i in range(len(file_list)):
		if show_progress:
			print('\r'+Lang.STR_PROGRESS%int(percent(i,len(file_list))),end='')
		with open(file_list[i], 'rb') as f:
			items.append({'path':file_list[i], 'eq':compareData(data, f.read(), buf)})
	
	items.sort(key=lambda k: k['eq'], reverse=True)
	
	return items



def getFileTime(path):
	ts = os.stat(path).st_mtime
	date = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
	return {'ts':ts, 'date':date}



def hex(buf,sep=' '):
	str = ""
	for c in buf:
		str += '{:02X}'.format(c)+sep
	return str[:len(str)-len(sep)]



def swapBytes(arr):
	res = [0]*len(arr)
	for i in range(0,len(arr),2):
		res[i] = arr[i+1]
		res[i+1] = arr[i]
	return bytes(res)



def getFileContents(path):
	with open(path, 'rb') as f:
		return f.read()



def savePatchData(path, data, patch = False):
	with open(path, 'wb') as f:
		f.write(data)
	if patch:
		patchFile(path, patch)



def patchFile(path, patch):
	with open(path, 'r+b') as f:
		for i in range(len(patch)):
			f.seek(patch[i]['o'],0)
			f.write(patch[i]['d'])



def entropy(file):
	
	with open(file, "rb") as f:
		data = f.read()
	
	vals = {byte: 0 for byte in range(2**8)}
	size = len(data)
	pp = size // 100
	
	for i in range(size):
		vals[data[i]] += 1
		if i % pp == 0:
			print('\r'+Lang.STR_PROGRESS%(i // pp),end='')
	
	probs = [val / size for val in vals.values()]
	entropy = -sum(prob * math.log2(prob) for prob in probs if prob > 0)
	
	return {'00':probs[0],'ff':probs[0xff],'ent':entropy}
