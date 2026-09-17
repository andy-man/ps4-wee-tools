#==========================================================
# Common utils
# part of ps4 wee tools project
#==========================================================
import hashlib, os, sys, math, random, datetime, winsound, re
import lang.lang as Lang #cross reference

# Common consts

INFO_FILE_SFLASH	= '_sflash0_.txt'
INFO_FILE_2BLS		= '_2bls_.txt'
ROOT_PATH			= os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH			= os.path.join(ROOT_PATH, 'config.ini')

# Config stuff

class Config:

	cfg = {}
	file = ''
	path = ''
	
	def __init__(self, file=''):
		self.file = file if file else CONFIG_PATH
		self.path = os.path.realpath(self.file)
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
			print(Lang.STR_CFG_ERROR, e)
			return False

		return True
	
	def get(self, key, default=''):
		return self.cfg.get(key, default)
	
	def set(self, key, val):
		self.cfg[key] = val

APP_CONFIG = Config()

# Colors stuff

# Windows' terminal doesn't support colors before win 10

USE_COLORS = APP_CONFIG.get('colors', False if sys.platform[:3] == 'win' and sys.getwindowsversion().major < 10 else True)

class Clr:

	reset			='\033[0m'	if USE_COLORS else ''
	bold			='\033[01m'	if USE_COLORS else ''
	disable			='\033[02m'	if USE_COLORS else ''
	underline		='\033[04m'	if USE_COLORS else ''
	reverse			='\033[07m'	if USE_COLORS else ''
	invisible		='\033[08m'	if USE_COLORS else ''
	strike			='\033[09m'	if USE_COLORS else ''
	
	class fg:

		black		='\033[30m'	if USE_COLORS else ''
		red			='\033[31m'	if USE_COLORS else ''
		green		='\033[32m'	if USE_COLORS else ''
		orange		='\033[33m'	if USE_COLORS else ''
		blue		='\033[34m'	if USE_COLORS else ''
		purple		='\033[35m'	if USE_COLORS else ''
		cyan		='\033[36m'	if USE_COLORS else ''
		l_grey		='\033[37m'	if USE_COLORS else ''
		d_grey		='\033[90m'	if USE_COLORS else ''
		l_red		='\033[91m'	if USE_COLORS else ''
		l_green		='\033[92m'	if USE_COLORS else ''
		yellow		='\033[93m'	if USE_COLORS else ''
		l_blue		='\033[94m'	if USE_COLORS else ''
		pink		='\033[95m'	if USE_COLORS else ''
		l_cyan		='\033[96m'	if USE_COLORS else ''
	
	class bg:

		black		='\033[40m'	if USE_COLORS else ''
		red			='\033[41m'	if USE_COLORS else ''
		green		='\033[42m'	if USE_COLORS else ''
		orange		='\033[43m'	if USE_COLORS else ''
		blue		='\033[44m'	if USE_COLORS else ''
		purple		='\033[45m'	if USE_COLORS else ''
		cyan		='\033[46m'	if USE_COLORS else ''
		l_grey		='\033[47m'	if USE_COLORS else ''


# Beeps

class Beep:

	IS_ACTIVE = APP_CONFIG.get('sound', False)
	
	@classmethod
	def success(cls):
		if not cls.IS_ACTIVE: return
		winsound.Beep(1000, 200)
	
	@classmethod
	def warning(cls):
		if not cls.IS_ACTIVE: return
		for _ in range(3): winsound.Beep(400, 100)
	
	@classmethod
	def error(cls):
		if not cls.IS_ACTIVE: return
		for _ in range(2): winsound.Beep(200, 200)


# UI stuff

class UI:
	
	LINE_WIDTH		= 70
	
	STATUS_TXT		= ''
	STATUS_CLR		= ''
	
	DIVIDER			= Clr.fg.yellow + '_'*LINE_WIDTH + Clr.reset + '\n'
	DIVIDER_DASH	= Clr.fg.yellow + '-'*LINE_WIDTH + Clr.reset + '\n'
	DIVIDER_BOLD	= '='*LINE_WIDTH + '\n'
	
	def clearScreen():
		os.system('cls' if sys.platform[:3] == 'win' else 'clear')
	
	# Colors
	
	def link(str):
		return Clr.underline + Clr.fg.cyan + str + Clr.reset
	
	def cyan(str):
		return Clr.fg.cyan + str + Clr.reset
	
	def highlight(str):
		return Clr.fg.yellow + str + Clr.reset
	
	def error(str):
		return Clr.fg.red + str + Clr.reset
	
	def warning(str):
		return Clr.fg.orange + str + Clr.reset
	
	def dark(str):
		return Clr.fg.d_grey + str + Clr.reset
	
	def grey(str):
		return Clr.fg.l_grey + str + Clr.reset
	
	def green(str):
		return Clr.fg.green + str + Clr.reset
	
	def pink(str):
		return Clr.fg.pink + str + Clr.reset

	def purple(str):
		return Clr.fg.purple + str + Clr.reset
	
	# Funcs

	_ANSI = re.compile(r'\033\[[0-9;]*m')

	@staticmethod
	def sp(s):
		"""Leading space on each line; skip if the visible text already starts with one."""
		if s is None:
			return s
		s = s if isinstance(s, str) else str(s)
		def indent_line(line):
			plain = UI._ANSI.sub('', line)
			if plain == '' or plain.startswith(' '):
				return line
			m = re.match(r'^((?:\033\[[0-9;]*m)*)', line)
			prefix = m.group(1) if m else ''
			return prefix + ' ' + line[len(prefix):]
		return '\n'.join(indent_line(p) for p in s.split('\n'))

	@classmethod
	def sp_print(cls, *args, **kwargs):
		if args:
			args = (cls.sp(args[0]),) + args[1:]
		print(*args, **kwargs)
	
	def clearInput(n = 1):
		for i in range(n):
			print('\033[1A' + '\033[K', end='')
	
	def setTitle(str = ''):
		if sys.platform[:3] == 'win':
			os.system('title ' + (str if str else Lang.APP_NAME.strip()))
	
	@classmethod
	def getTab(cls, str):
		return Clr.fg.yellow+'  _'+('_'*len(str))+'_\n'+('_/ '+str+' \\_').ljust(cls.LINE_WIDTH, '_')+'\n'+Clr.reset
	
	def getTable(data, pad=16):
		table = []
		
		for key in data:
			if data[key] == '':
				continue
			table.append(' {} : {}'.format(('%s'%key).ljust(pad,' '),data[key]))
		
		return table
	
	@classmethod
	def showTable(cls, data, pad=16):
		table = cls.getTable(data, pad)
		print('\n'.join(table))
	
	@classmethod
	def showTableEx(cls, data, cols = 2, width = False):
		width = width if width else cls.LINE_WIDTH // cols
		rows = (len(data) // cols) + (1 if len(data) % cols else 0)
		lines = [''] * rows
		for i in range(len(data)):
			lines[i % rows] += data[i].ljust(width, ' ')
		print('\n'.join(lines))
	
	def getMenu(menu, start=0):
		lines = []
		
		if type(menu) is dict:
			for n in menu:
				lines.append(' %s: %s'%(n,menu[n]))
		else:
			for n, text in enumerate(menu):
				lines.append(' '+str(n+start)+': '+text)
		
		return lines
	
	@classmethod
	def showMenu(cls, menu, start=0):
		lines = cls.getMenu(menu, start)
		print('\n'.join(lines))
	
	@classmethod
	def setStatus(cls, v, clr = Clr.fg.yellow):
		cls.STATUS_TXT = v
		cls.STATUS_CLR = clr
	
	@classmethod
	def showStatus(cls):
		if cls.STATUS_TXT:
			print(cls.DIVIDER_DASH + cls.STATUS_CLR + cls.STATUS_TXT + Clr.reset)
			cls.STATUS_TXT = ''

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
