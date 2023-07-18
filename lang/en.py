#==========================================================
# Default language [EN]
# part of ps4 wee tools project
#==========================================================

MENU_FILE_SELECTION = {
	'a':'Show all files / Toggle filters [bin,pup]',
	'f':'Build sflash0 dump',
	's':'Build SBL2/PUP',
	'c':'Compare bin files in current folder',
	'e':'Exit',
}

MENU_ADDTIONAL = [
	'Extract NOR\'s partitions',
	'Build dump from extracted files',
	'Get HDD EAP keys [keys.bin]',
	'Base validation and entropy stats',
	'Create EMC cfw (only for Fat 1xxx/11xx)',
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

STR_FILE_LIST			= 'Files list'
STR_NOR_INFO			= 'NOR dump info'
STR_ADDITIONAL			= 'Additional tools'
STR_SYSCON_INFO			= 'Syscon dump info'
STR_COMPARE				= 'Compare'
STR_HELP				= 'Help'
STR_ACTIONS				= 'Actions'
STR_DOWNGRADE			= 'Downgrade patterns'
STR_MEMCLOCK			= 'Memory clock'
STR_SAMU_BOOT			= 'SAMU boot'
STR_SYSFLAGS			= 'System flags'
STR_LAST_SVNS			= 'Last SNVS entries'
STR_APATCH_SVNS			= 'SNVS auto patching'
STR_MPATCH_SVNS			= 'SNVS manual patcher'
STR_NOR_VALIDATOR		= 'NOR validator'
STR_NOR_FLAGS			= 'NOR flags'
STR_NOR_EXTRACT			= 'NOR extractor'
STR_NOR_BUILD			= 'NOR builder'
STR_HDD_KEY				= 'HDD eap key'
STR_SLB2_BUILDER		= 'SLB2 builder'
STR_UNPACK_SLB2			= 'SLB2 unpacker'
STR_EMC_CFW				= 'EMC CFW (Aeolia)'

STR_EMPTY_FILE_LIST		= ' File list is empty'
STR_NO_FOLDER			= ' Folder {} doesn\'t exists'
STR_EXTRACTING			= ' Extracting sflash0 to {} folder'
STR_FILES_CHECK			= ' Checking files'
STR_BUILDING			= ' Building file {}'

STR_DONE				= ' All done'
STR_NO_INFO				= '- No info -'
STR_OFF					= 'Off'
STR_ON					= 'On'
STR_PROGRESS			= ' Progress {:2d}% '
STR_WARNING				= 'Warning'
STR_HELP				= 'Help'
STR_UNKNOWN				= '- Unknown -'
STR_WAIT				= ' Please wait...'
STR_YES					= 'Yes'
STR_NO					= 'No'
STR_PROBABLY			= 'Probably'
STR_NOT_SURE			= 'not sure'
STR_SET_TO				= ' {} was set to [{}]'

STR_DIFF				= 'Different'
STR_NOT_FOUND			= 'not found'
STR_BAD_SIZE			= 'bad size'
STR_OK					= 'OK'
STR_FAIL				= 'Fail'
STR_ABORT				= ' Action was aborted'

STR_NIY					= ' Function is not implemented yet'
STR_CLEAN_FLAGS			= ' Clean all system flags'
STR_UNK_FILE_TYPE		= ' Unknown file type'
STR_UNK_CONTENT			= ' Unknown content'
STR_UART				= ' UART is set to '
STR_DEBUG				= ' Syscon debug is set to '

STR_DIFF_SLOT_VALUES	= ' Values in slots are different!'
STR_SYSFLAGS_CLEAN		= ' Sys flags were cleared. Tip: turn on UART'
STR_SAMU_UPD			= ' SAMU flag was set to '
STR_DOWNGRADE_UPD		= ' Downgrade was set to: '
STR_SNVS_ENTRIES		= '{} records found at 0x{:5X}'
STR_LAST_DATA			= ' Last {} records of {}: '
STR_MEMCLOCK_SET		= ' GDDR5 frequency was set to {:d}MHz [0x{:02X}]'

STR_PATCH_CANCELED		= ' Patch was canceled'
STR_PATCH_SUCCESS		= ' Successfully removed {} entries'
STR_PATCH_SAVED			= ' Patch was saved to {}'
STR_PATCH_INDEXES		= ' Last 08-0B at 0x{:04X} | Previous at 0x{:04X}\n'

STR_MPATCH_INPUT		= ' How many records to clean (from end): '
STR_CHOICE				= ' Make choice: '
STR_BACK				= ' Press [ENTER] to go back'
STR_MEMCLOCK_INPUT		= ' Setup frequency [400 - 2000] / [0 set default (0xFF)] MHz '
STR_SAMU_INPUT			= ' Setup SAMU [0 - 255] / [default is 255 (0xFF)] '

STR_PARTITIONS_CHECK	= ' Checking partitions'
STR_ENTROPY				= ' Entropy statistics'
STR_MAGICS_CHECK		= ' Checking magics'
STR_IS_PART_VALID		= '[{}] {} FW {}'
STR_FW_VERSION			= ' FW version {} / Active slot {}'

STR_COMPARE_RESULT		= ' {} | Result: {}'
STR_INCORRECT_SIZE		= ' {} - incorrect dump size!'
STR_FILE_NOT_EXISTS		= ' File {} doesn\'t exist!'
STR_SAVED_TO			= ' Saved to {}'
STR_ERROR_INPUT			= ' Incorrect input'
STR_ERROR_DEF_VAL		= ' Setting default values'
STR_ERROR_CHOICE		= ' Invalid choice'
STR_OUT_OF_RANGE		= ' Value is out of range!'
STR_FILES_MATCH			= ' Files are equal'
STR_FILES_MISMATCH		= ' Files mismatch'

STR_USE_NEWBLOBS		= ' Use new key blobs? [y] '
STR_CONFIRM_SEPARATE	= ' Save as separate file? [y] '
STR_CONFIRM				= ' Input [y] to continue: '
STR_CURRENT				= ' Current: '
STR_GO_BACK				= ' Go back'

STR_UNPATCHABLE = ' Can\'t proceed!\n'\
' Last SNVS record #{} counter [0x{:02X}] type [0x{:02X}]\n'\
' Last 08-0B index = {} / Previous 08-0B index = {}'

STR_OVERCLOCKING = '\n'\
' Dangerous operation! \n'\
' Most GDDR5 runs at 6000-8000 MHz. GDDR5 is quad pumped [x4]\n'\
' GDDR5 at 8000 MHz technically runs at 2000 MHz\n'\
' If you have problems, lower frequency to 1000 MHz\n'\
'\n'\
' Effective GDDR5 clock is 1350 MHz\n'\
' The frequency is selected experimentally\n'\
' - Too high value can lead to LOADBIOS -8 or DCT [*] error\n'\
' - Too low value leads to AMDINIT error \n'

STR_PATCHES = '\n'\
' Be careful: All patches are applied immediatly to file! \n'\
' Will switch value between available values for chosen option \n'

STR_DOWNGRADE = '\n'\
' Dangerous operation! \n'\
' Slot switching is used for FW revert (downgrade).\n'+\
' It also fixes "loadbios" error.\n'\
' Make sure you have backup of stock NOR dump and SYSCON.\n'\
' Syscon patching required! Otherwise you\'ll get "loadbios" error.\n'\
' Console will not boot normally.\n'

STR_ABOUT_MPATCH = 'Manual patch instructions'
STR_INFO_SC_MPATCH = '\n'\
' Every record has 16 bytes length. First byte is always "A5"\n'\
' The second byte is record "type" usualy in range [08-30] (hex)\n'\
' Firmware update takes 4 records with types {}\n'\
' To cancel last fw update we need to clean these 4 records (fill 0xFF)\n'\
' If there are {},{} types after {} patch is impossible\n'\
' backup slot is already erased, you\'ll got checkUpdVersion error\n'

STR_ABOUT_EAP = 'About EAP keys'
STR_INFO_HDD_EAP = '\n'\
' These keys allow you to explore PS4 HDD files with PC\n'\
' You can find additional info by visiting:\n '\

STR_APP_HELP = '\n'\
' Usage: ps4-wee-tools [params] \n'\
'\n'\
' Params: \n\n'\
'  <file> - auto detects file type and loads appropriate tool\n'\
'  <folder> - build dump from files from supplied folder\n'\
'  <file1> <file2> ... - compare files (with MD5 info)\n'\
'  -help - show this help screen\n'\
'\n'\
' File selection works only for *.bin files within app\'s directory\n'\
'\n'\
' Home: '
