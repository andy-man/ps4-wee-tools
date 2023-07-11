LINE_WIDTH = 70

# Helping UI stuff

class Clr:
    reset			='\033[0m'
    bold			='\033[01m'
    disable			='\033[02m'
    underline		='\033[04m'
    reverse			='\033[07m'
    invisible		='\033[08m'
    strike			='\033[09m'
    class fg:
        black		='\033[30m'
        red			='\033[31m'
        green		='\033[32m'
        orange		='\033[33m'
        blue		='\033[34m'
        purple		='\033[35m'
        cyan		='\033[36m'
        l_grey		='\033[37m'
        d_grey		='\033[90m'
        l_red		='\033[91m'
        l_green		='\033[92m'
        yellow		='\033[93m'
        l_blue		='\033[94m'
        pink		='\033[95m'
        l_cyan		='\033[96m'
    class bg:
        black		='\033[40m'
        red			='\033[41m'
        green		='\033[42m'
        orange		='\033[43m'
        blue		='\033[44m'
        purple		='\033[45m'
        cyan		='\033[46m'
        l_grey		='\033[47m'


def getTab(str):
	return Clr.fg.yellow+'  _'+('_'*len(str))+'_\n'+('_/ '+str+' \_').ljust(LINE_WIDTH, '_')+'\n'+Clr.reset

def showTable(data, pad=16):
	for key in data:
		print(' {} : {}'.format(key.ljust(pad,' '),data[key]))

def getMenu(menu, start=0):
	for n, text in enumerate(menu):
		print(' '+str(n+start)+': '+text)


STATUS = ''
S_COLOR = ''

def setStatus(v,clr=Clr.fg.yellow):
	global STATUS, S_COLOR
	STATUS = v
	S_COLOR = clr

def showStatus():
	global STATUS, S_COLOR
	if STATUS:
		print(DIVIDER_DASH+S_COLOR+STATUS+Clr.reset)
		STATUS = ''

# Messages

DIVIDER = Clr.fg.yellow+'_'*LINE_WIDTH+Clr.reset+'\n'
DIVIDER_DASH = Clr.fg.yellow+'-'*LINE_WIDTH+Clr.reset+'\n'
DIVIDER_BOLD = '='*LINE_WIDTH+'\n'

TITLE = DIVIDER_BOLD+' PS4 ~WEE~ TOOLS v0.7 '+('by Andy_maN').rjust(LINE_WIDTH-23)+'\n'+DIVIDER_BOLD

TAB_FILE_LIST = getTab('Files list')
TAB_NOR_INFO = getTab('NOR dump info')
TAB_ADDITIONAL = getTab('Additional tools')
TAB_SYSCON_INFO = getTab('Syscon dump info')
TAB_COMPARE = getTab('Compare')
TAB_HELP = getTab('Help')
TAB_ACTIONS = getTab('Actions')
TAB_DOWNGRADE = getTab('Downgrade patterns')
TAB_MEMCLOCK = getTab('Memory clock')
TAB_SAMU_BOOT = getTab('SAMU boot')
TAB_SYSFLAGS = getTab('System flags')
TAB_LAST_SVNS = getTab('Last SNVS entries')
TAB_APATCH_SVNS = getTab('SNVS auto patching')
TAB_MPATCH_SVNS = getTab('SNVS manual patcher')
TAB_ENTROPY = getTab('Entropy statistics')
TAB_NOR_FLAGS = getTab('NOR flags')
TAB_NOR_EXTRACT = getTab('NOR extractor')
TAB_NOR_BUILD = getTab('NOR builder')
TAB_HDD_KEY = getTab('HDD eap key')

MENU_ADDTIONAL = [
	'Extract NOR\'s partitions',
	'Build dump from extracted files',
	'Get HDD EAP keys [keys.bin]',
	'Entropy stats',
]

MENU_NOR_ACTIONS = [
	'Select another file',
	'Flags (UART, RNG, Memtest, etc)',
	'Memory clocking (GDDR5)',
	'SAMU boot flag',
	'Downgrade - CoreOS slot switching',
	'Additional tools',
	'Exit'
]

MENU_SC_ACTIONS = [
	'Select another file',
	'Toggle Debug',
	'Show active SNVS block',
	'Auto SNVS patch',
	'Manual SNVS patch',
	'Exit'
]

MENU_PATCHES = [
	'Method A - last 08-0B will be cleaned (4 records)',
	'Method B - last 08-0B and below will be cleaned ({} records)',
	'Method C - last 08-0B will be replaced with previous',
	'Method D - fix counters (f.e. after method C)',
]

MSG_NO_FOLDER = ' Folder {} doesn\'t exists'
MSG_EXTRACTING = ' Extracting sflash0 to {} folder'
MSG_FILES_CHECK = ' Checking files'
MSG_BUILDING = ' Building file {}'

MSG_DONE = Clr.fg.yellow+' All done'+Clr.reset
MSG_NO_INFO = '- No info -'
MSG_OFF = 'Off'
MSG_ON = 'On'

MSG_WAIT = ' Please wait...'
MSG_YES = 'Yes'
MSG_NO = 'No'
MSG_PROBABLY = 'Probably'
MSG_NOT_SURE = 'not sure'
MSG_SET_TO = ' {} was set to [{}]'

MSG_NOT_FOUND = Clr.fg.red+'not found'+Clr.reset
MSG_BAD_SIZE = Clr.fg.orange+'bad size'+Clr.reset
MSG_OK = Clr.fg.green+'OK'+Clr.reset
MSG_ABORT = Clr.fg.red+' Action was aborted'+Clr.reset

MSG_NIY = ' Function is not implemented yet'
MSG_CLEAN_FLAGS = ' Clean all system flags'
MSG_UNK_FILE_TYPE = ' Unknown file type'
MSG_UART = ' UART is set to '
MSG_DEBUG = ' Sycon debug is set to '

MSG_DIFF_SLOT_VALUES = ' Values in slots are different!'
MSG_SYSFLAGS_CLEAN = ' Sys flags were cleared. Tip: turn on UART'
MSG_SAMU_UPD = ' SAMU flag was set to '
MSG_DOWNGRADE_UPD = ' Downgrade was set to: '
MSG_SNVS_ENTRIES = '{} records found at 0x{:5X}'
MSG_LAST_DATA = ' Last {} records of {}: '
MSG_MEMCLOCK_SET = ' GDDR5 frequency was set to {:d}MHz [0x{:02X}]'

MSG_PATCH_CANCELED = ' Patch was canceled'
MSG_PATCH_SUCCESS = ' Successfully removed {} entries'
MSG_PATCH_SAVED = ' Patch was saved to {}'
MSG_PATCH_INDEXES = ' Last 08-0B at 0x{:04X} | Previous at 0x{:04X}\n'

MSG_MPATCH_INPUT = DIVIDER + ' How many records to clean (from end): '
MSG_CHOICE = DIVIDER + ' Make choice: '
MSG_BACK = DIVIDER + ' Press [ENTER] to go back'
MSG_MEMCLOCK_INPUT = DIVIDER + ' Setup frequency [400 - 2000] / [0 set default (0xFF)] MHz '
MSG_SAMU_INPUT = DIVIDER + ' Setup SAMU [0 - 255] / [default is 255 (0xFF)] '

MSG_INCORRECT_SIZE	= ' {} - incorrect dump size!'
MSG_FILE_NOT_EXISTS	= ' File {} doesn\'t exist!'
MSG_ERROR_INPUT		= ' Incorrect input'
MSG_ERROR_DEF_VAL	= ' Setting default values'
MSG_ERROR_CHOICE	= ' Invalid choice'
MSG_OUT_OF_RANGE	= ' Value is out of range!'
MSG_FILES_MATCH		= ' Files are equal'
MSG_FILES_MISMATCH	= ' Files mismatch'

MSG_USE_NEWBLOBS = ' Use new key blobs? [y] '
MSG_CONFIRM = DIVIDER + ' Input [y] to continue: '
MSG_CURRENT = ' Current: '
MSG_GO_BACK = ' Go back'

MSG_UNPATCHABLE = Clr.fg.orange+' Can\'t proceed!\n'\
' Last SNVS record #{} counter [0x{:02X}] type [0x{:02X}]\n'\
' Last 08-0B index = {} / Previous 08-0B index = {}'+Clr.reset

MSG_OVERCLOCKING = getTab('Warning')+\
'\n'+Clr.fg.orange+\
' Dangerous operation! \n'\
' Most GDDR5 runs at 6000-8000 MHz. GDDR5 is quad pumped [x4]\n'\
' GDDR5 at 8000 MHz technically runs at 2000 MHz\n'\
' If you have problems, lower frequency to 1000 MHz\n'\
'\n'\
' Effective GDDR5 clock is 1350 MHz\n'\
' The frequency is selected experimentally\n'\
' - Too high value can lead to LOADBIOS -8 or DCT [*] error\n'\
' - Too low value leads to AMDINIT error \n'+Clr.reset

MSG_PATCHES = getTab('Warning')+\
'\n'+Clr.fg.orange+\
' Be careful: All patches are applied immediatly to file! \n'\
' Will switch value between available values for chosen option \n'+Clr.reset

MSG_DOWNGRADE = getTab('Warning')+\
'\n'+Clr.fg.orange+\
' Dangerous operation! \n'\
' Slot switching is used for FW revert (downgrade).\n'+\
' It also fixes "loadbios" error.\n'\
' Make sure you have backup of stock NOR dump.\n'\
' Syscon patching required! Otherwise you\'ll get "loadbios" error.\n'\
' Console will not boot normally.\n'+Clr.reset

MSG_080B = Clr.fg.cyan+'"08-0B"'+Clr.reset
MSG_0C0F = Clr.fg.orange+'"0C-0F"'+Clr.reset
MSG_2023 = Clr.fg.red+'"20-23"'+Clr.reset

MSG_INFO_SC_MPATCH = getTab('Manual patch instructions')+\
'\n'\
' Every record has 16 bytes length. First byte is always "A5"\n'\
' The second byte is record "type" usualy in range [08-30] (hex)\n'\
' Firmware update takes 4 records with types '+MSG_080B+'\n'\
' To cancel last fw update we need to clean these 4 records (fill 0xFF)\n'\
' If there are '+MSG_0C0F+','+MSG_2023+' types after '+MSG_080B+' patch is impossible\n'\
' backup slot is already erased, you\'ll got checkUpdVersion error\n'

MSG_INFO_HDD_EAP = getTab('About EAP keys')+\
'\n'\
' These keys allows you to explore PS4 HDD files with PC\n'+\
' You can find additional info by visiting:\n'+\
' '+Clr.underline+Clr.fg.cyan+'https://www.psdevwiki.com/ps4/Mounting_HDD_in_Linux'+Clr.reset

MSG_HELP = getTab('Help')+\
'\n'\
' Usage: '+Clr.bold+'ps4-wee-tools <file1> <file2> ... \n'+Clr.reset+\
'  - One <file>: auto detects file type and loads appropriate tool\n'\
'  - Multi <files>: compare mode (with MD5 info)\n'\
'  - help: show this help screen\n'\
'\n'\
' File selection works only for *.bin files within app\'s directory\n'\
'\n'\
' Home: '+Clr.underline+Clr.fg.cyan+'https://github.com/andy-man/ps4-wee-tools'+Clr.reset
