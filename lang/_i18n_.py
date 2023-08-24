#==========================================================
# UI internationalization
# part of ps4 wee tools project
#==========================================================
import sys, os

APP_VERSION = '0.8.6'

# Colors stuff

use_clr = True
# win terminal doesn't support colors before win 10
if sys.platform[:3] == 'win' and sys.getwindowsversion().major < 10:
	use_clr = False

class Clr:
	reset			='\033[0m'	if use_clr else ''
	bold			='\033[01m'	if use_clr else ''
	disable			='\033[02m'	if use_clr else ''
	underline		='\033[04m'	if use_clr else ''
	reverse			='\033[07m'	if use_clr else ''
	invisible		='\033[08m'	if use_clr else ''
	strike			='\033[09m'	if use_clr else ''
	class fg:
		black		='\033[30m'	if use_clr else ''
		red			='\033[31m'	if use_clr else ''
		green		='\033[32m'	if use_clr else ''
		orange		='\033[33m'	if use_clr else ''
		blue		='\033[34m'	if use_clr else ''
		purple		='\033[35m'	if use_clr else ''
		cyan		='\033[36m'	if use_clr else ''
		l_grey		='\033[37m'	if use_clr else ''
		d_grey		='\033[90m'	if use_clr else ''
		l_red		='\033[91m'	if use_clr else ''
		l_green		='\033[92m'	if use_clr else ''
		yellow		='\033[93m'	if use_clr else ''
		l_blue		='\033[94m'	if use_clr else ''
		pink		='\033[95m'	if use_clr else ''
		l_cyan		='\033[96m'	if use_clr else ''
	class bg:
		black		='\033[40m'	if use_clr else ''
		red			='\033[41m'	if use_clr else ''
		green		='\033[42m'	if use_clr else ''
		orange		='\033[43m'	if use_clr else ''
		blue		='\033[44m'	if use_clr else ''
		purple		='\033[45m'	if use_clr else ''
		cyan		='\033[46m'	if use_clr else ''
		l_grey		='\033[47m'	if use_clr else ''

# UI stuff

class UI:
	
	LINE_WIDTH		= 70
	
	STATUS_TXT		= ''
	STATUS_CLR		= ''
	
	DIVIDER			= Clr.fg.yellow + '_'*LINE_WIDTH + Clr.reset + '\n'
	DIVIDER_DASH	= Clr.fg.yellow + '-'*LINE_WIDTH + Clr.reset + '\n'
	DIVIDER_BOLD	= '='*LINE_WIDTH + '\n'
	
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
	
	def green(str):
		return Clr.fg.green + str + Clr.reset
	
	# Funcs
	
	def clearInput(n = 1):
		for i in range(n):
			print('\033[1A' + '\033[K', end='')
	
	def setTitle(str):
		if sys.platform[:3] == 'win':
			os.system('title '+str)
	
	def getTab(str):
		return Clr.fg.yellow+'  _'+('_'*len(str))+'_\n'+('_/ '+str+' \_').ljust(UI.LINE_WIDTH, '_')+'\n'+Clr.reset
	
	def getTable(data, pad=16):
		return UI.showTable(data, pad, True)
	
	def showTable(data, pad=16, echo = True):
		table= ''
		for key in data:
			if data[key] == '':
				continue
			table += ' {} : {}\n'.format(('%s'%key).ljust(pad,' '),data[key])
		if echo:
			print(table,end='')
		else:
			return table
	
	def showMenu(menu, start=0):
		if type(menu) is dict:
			for n in menu:
				print(' %s: %s'%(n,menu[n]))
		else:
			for n, text in enumerate(menu):
				print(' '+str(n+start)+': '+text)
	
	def setStatus(v, clr = Clr.fg.yellow):
		UI.STATUS_TXT = v
		UI.STATUS_CLR = clr
	
	def showStatus():
		if UI.STATUS_TXT:
			print(UI.DIVIDER_DASH + UI.STATUS_CLR + UI.STATUS_TXT + Clr.reset)
			UI.STATUS_TXT = ''

# Common strings (used in lang files)

STR_080B = Clr.fg.cyan+'"08-0B"'+Clr.reset
STR_0C0F = Clr.fg.orange+'"0C-0F"'+Clr.reset
STR_2023 = Clr.fg.red+'"20-23"'+Clr.reset

from lang.en import *

APP_NAME = ' PS4 ~WEE~ TOOLS v' + APP_VERSION
TITLE = UI.DIVIDER_BOLD + APP_NAME+('by Andy_maN').rjust(UI.LINE_WIDTH-len(APP_NAME)-1)+'\n' + UI.DIVIDER_BOLD

# Fill strings

STR_MPATCH_INPUT	= UI.DIVIDER + STR_MPATCH_INPUT
STR_CHOICE			= UI.DIVIDER + STR_CHOICE
STR_BACK			= UI.DIVIDER + STR_BACK
STR_MEMCLOCK_INPUT	= UI.DIVIDER + STR_MEMCLOCK_INPUT
STR_SAMU_INPUT		= UI.DIVIDER + STR_SAMU_INPUT
STR_CONFIRM			= UI.DIVIDER + STR_CONFIRM

STR_APP_HELP		= STR_APP_HELP + UI.link('https://github.com/andy-man/ps4-wee-tools')
STR_INFO_HDD_EAP	= STR_INFO_HDD_EAP + UI.link('https://www.psdevwiki.com/ps4/Mounting_HDD_in_Linux')
STR_INFO_EMC_CFW	= STR_INFO_EMC_CFW + UI.link('https://www.psdevwiki.com/ps4/Southbridge')

STR_INFO_SC_MPATCH	= STR_INFO_SC_MPATCH.format(STR_080B, STR_0C0F, STR_2023, STR_080B)

# Colorize strings

STR_DONE			= Clr.fg.yellow+ STR_DONE + Clr.reset
STR_NOT_FOUND		= Clr.fg.red + STR_NOT_FOUND + Clr.reset
STR_BAD_SIZE		= Clr.fg.orange + STR_BAD_SIZE + Clr.reset
STR_DIFF			= Clr.fg.orange + STR_DIFF + Clr.reset
STR_FAIL			= Clr.fg.red + STR_FAIL + Clr.reset
STR_OK				= Clr.fg.green + STR_OK + Clr.reset
STR_ABORT			= Clr.fg.red + STR_ABORT + Clr.reset

