#==========================================================
# serial lib
# part of ps4 wee tools project
#==========================================================
import serial, threading, sys
from lang._i18n_ import *
from serial.tools import list_ports



class WeeSerial:
	
	patterns = {
		'error'		: Clr.fg.red,
		'warn'		: Clr.fg.orange,
		'release'	: Clr.fg.green,
		'network'	: Clr.fg.cyan,
		'samu'		: Clr.fg.blue,
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
	
	enc		= 'utf-8'
	sp		= False
	alive	= False
	buf		= b''
	err		= ''
	
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
			
			self.buf = ''
		except Exception as e:
			err = str(e)
    
	def __del__(self):
		if self.sp and self.sp.is_open:
			self.sp.close()
    
	def error(self, msg):
		print(' '+msg)
	
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
    
	def monitor(self):
		pattern = self.patterns
		while self.sp.is_open and self.alive:
			try:
				line = self.sp.readline()
				line = line.decode(self.enc,'ignore')
				for k in pattern:
					if k in line.lower():
						line = pattern[k] + line + Clr.reset
						break
				self.printf(line)
			except Exception as e:
				self.err = str(e)
				self.alive = False
				break
    
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
		return self.send((txt).encode(self.enc,'ignore') + EOL)
    
	def send(self, bytes):
		try:
			self.sp.write(bytes)
		except Exception as e:
			self.error(str(e))
	
	# SPI flasher
	
	def write(self, s):
		if isinstance(s, int):
			s = chr(s)
		elif isinstance(s,tuple) or isinstance(s,list):
			s = ''.join([chr(c) for c in s])
		self.buf += s
		while len(self.buf) > self.BUFSIZE:
			self.sp.write(self.buf[:self.BUFSIZE])
			self.buf = self.buf[self.BUFSIZE:]
	
	def flush(self):
		if len(self.buf):
			self.sp.write(self.buf)
			self.sp.flush()
			self.buf = ''
	
	def read(self, size):
		self.flush()
		data = self.sp.read(size)
		return data
	
	def readbyte(self):
		return ord(self.read(1))
	
	def close(self):
		self.printf('Closing serial port')
		if self.sp is None:
			self.printf('Device already closed')
		else:
			self.sp.close()
			self.printf('Done')


