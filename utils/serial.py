#==========================================================
# serial lib
# part of ps4 wee tools project
#==========================================================
import serial, threading, sys, time
from lang._i18n_ import *
from serial.tools import list_ports



class WeeSerial:
	
	patterns = {
		'error'		: Clr.fg.red,
		'warn'		: Clr.fg.orange,
		'release'	: Clr.fg.green,
		'network'	: Clr.fg.blue,
		'samu'		: Clr.fg.cyan,
		'standby'	: Clr.bg.purple,
	}
	
	cfg = {
		'baudrate'		: 115200,
		'bytesize'		: 8,
		'parity'		: 'N',
		'stopbits'		: 1,
		'xonxoff'		: 0,
		'rtscts'		: 0,
		'dsrdtr'		: 0,
		'timeout'		: 300,
		'write_timeout'	: 120,
	}
	
	ENCODING	= 'utf-8'
	EOL			= b'\n\r'
	SHOWCODES	= False
	LOG			= False
	
	TX			= 0
	RX			= 0
	
	sp			= False
	alive		= False
	err			= ''
	
	def __init__(self, port, cfg = {}):
		
		for k in self.cfg:
			if k in cfg:
				self.cfg[k] = cfg[k]
		
		try:
			self.sp = serial.Serial()
			self.sp.apply_settings(self.cfg)
			self.sp.port = port
			
			self.sp.open()
			self.sp.flushInput()
			self.sp.flushOutput()
			
		except Exception as e:
			err = str(e)
			self.error(str(e))
    
	def __del__(self):
		if self.sp and self.sp.is_open:
			self.sp.close()
    
	def error(self, msg):
		self.printf(UI.error(' '+msg+'\n\n'))
	
	def printf(self, str, erase = False):
		print(('\r ' if erase else '') + str, end='')
		sys.stdout.flush()
    
	def getPortList():
		ports = []
		for port, desc, hwid in sorted(list_ports.comports()):
			ports.append({'port':port, 'desc':desc, 'hwid':hwid})
		return ports
    
	def getPortInfo(self):
		if self.err:
			return self.err
		return '%s %d %d %s %d (%s)'%(self.sp.port, self.sp.baudrate, self.sp.bytesize, self.sp.parity, self.sp.stopbits, 'open' if self.sp.is_open else 'closed')
    
	def printline(self, line):
		patterns = self.patterns
		for k in patterns:
			if k in line.lower():
				line = patterns[k] + line + Clr.reset
				break
		self.printf(line)
	
	def getLines(self, buf):
		txt = ''
		lines = []
		prev_c = b''
		
		for c in buf:
			if c in self.EOL:
				if prev_c in self.EOL and c != prev_c:
					txt = ''
				else:
					lines.append(txt+'\n')
					txt = ''
			elif c >= 0x20:
				txt += chr(c)
			elif self.SHOWCODES:
				txt += UI.highlight(':%02X')%(c)
			
			prev_c = c
		
		if len(txt):
			lines.append(txt)
		
		return lines
	
	def monitor(self):
		
		self.RX = 0
		self.TX = 0
		start = time.time()
		
		while self.sp.is_open and self.alive:
			try:
				self.RX += self.sp.in_waiting
				if self.sp.in_waiting > 0:
					buf = self.sp.read(self.sp.in_waiting)
					if self.LOG:
						with open(self.LOG, 'ab') as log:
							log.write(buf)
					for line in self.getLines(buf):
						self.printline(line)
				
				time.sleep(0.1)
				
				UI.setTitle(STR_MONITOR_STATUS%(self.RX, self.TX, time.time() - start))
			
			except Exception as e:
				self.err = str(e)
				self.alive = False
				break
		
		UI.setTitle()
    
	def startMonitor(self):
		if not self.sp:
			return -1
		self.alive = True
		threading.Thread(target=self.monitor, args=(), daemon=True).start()
	
	def stopMonitor(self):
		self.alive = False
	
	def getSP(self, key = ''):
		if not self.sp:
			return -1
		return self.sp[key] if key and key in self.sp else self.sp
	
	def sendText(self, txt, EOL = b'\n\r'):
		txt = (txt).encode(self.ENCODING,'ignore') + EOL
		if self.LOG:
			with open(self.LOG, 'ab') as log:
				log.write(txt)
		return self.send(txt)
    
	def send(self, bytes):
		try:
			self.sp.write(bytes)
			self.TX += len(bytes)
		except Exception as e:
			self.error(str(e))
	
	def close(self):
		if not self.sp is None:
			self.sp.close()
	
	# Private
	
	def __write(self, s):
		try:
			if isinstance(s, int):
				s = s.to_bytes(1,'big')
			elif isinstance(s,tuple) or isinstance(s,list):
				s = bytes(s)
			
			self.BUFFER += s
			
			while len(self.BUFFER) > self.BUFFER_SIZE:
				self.sp.write(self.BUFFER[:self.BUFFER_SIZE])
				self.BUFFER = self.BUFFER[self.BUFFER_SIZE:]
		
		except Exception as e:
			self.error(str(e))
	
	def __flush(self):
		try:
			if len(self.BUFFER):
				self.sp.write(self.BUFFER)
				self.sp.flush()
				self.BUFFER = b''
			
		except Exception as e:
			self.error(str(e))
	
	def __read(self, size):
		self.__flush()
		try:
			data = self.sp.read(size)
			return data
			
		except Exception as e:
			self.error(str(e))
			return b''
	
	def __clean(self):
		if not self.sp.is_open:
			return False
		self.sp.flushInput()
		self.sp.flushOutput()
	
	# Helpers
	
	def testPatterns(self, path):
		if os.path.isfile(path):
			with open(path, 'r') as file:
				lines = file.readlines()
				for line in lines:
					self.printline(line)