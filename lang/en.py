#==========================================================
# Default language [EN]
# part of ps4 wee tools project
#==========================================================

MENU_EAP_KEYS = [
	'Replace A with B (key_a <= key_b)',
	'Replace B with A (key_a => key_b)',
	'Fix magic A *',
	'Fix magic B *',
	'Generate new A,B keys (length 0x60) *',
	'Generate new A,B keys (length 0x40) *',
	'Clean key B *',
]

MENU_SPIWAY = [
	'Read all',
	'Read area',
	'Read block',
	'Write all',
	'Write area',
	'Write block',
	'Verify all',
	'Verify area',
	'Verify block',
	'Erase all',
	'Erase area',
	'Erase block',
]

MENU_TOOL_SELECTION = [
	'File browser',
	'Terminal (UART)',
	'sFlash r/w (SPIway by Judges)',
	'Syscon r/w (SCTool by Abkarino & EgyCnq)',
	'Syscon r/o (SCRead by DarkNESmonk)',
	'Exit',
]

MENU_FILE_SELECTION = {
	'a':'Show all files / Toggle filters [bin,pup]',
	'f':'Build sflash0 dump',
	'b':'Build 2BLS/PUP',
	'c':'Compare bin files in current folder',
	'm':'Go to [Main menu]',
}

MENU_ADDTIONAL = [
	'Extract sFlash\'s partitions',
	'Build dump from extracted files',
	'View / Recover EAP key',
	'Get HDD keys = decrypt EAP key = create [keys.bin]',
	'Base validation and entropy stats',
	'Create EMC cfw (only for Fat 1xxx/11xx)',
]

MENU_EXTRA_FLASHER = {
	's':'Select file',
	'f':'Launch Tool for this file',
	'm':'Open Main menu',
}

MENU_EXTRA = {
	's':'Select another file',
	'f':'Flash this file (full/parts) back to console',
	'm':'Open Main menu',
}

MENU_NOR_ACTIONS = [
	'Flags (UART, RNG, Memtest, etc)',
	'Memory clocking (GDDR5)',
	'SAMU boot flag',
	'CoreOS slot switching (FW revert)',
	'Additional tools',
]

MENU_SC_ACTIONS = [
	'Toggle Debug',
	'SNVS block viewer',
	'Auto SNVS patch',
	'Manual SNVS patch',
	'Rebuild SNVS',
	'Boot modes (Factory Service Mode / Normal)',
	'Clean SNVS (sc factory reset)',
]

MENU_PATCHES = [
	'Method A - last 08-0B will be deleted (4 records)',
	'Method B - last 08-0B and below will be cleaned ({} records)',
	'Method C - clean everything below previous 08-0B ({} records)',
]

MENU_SC_STATUSES = [
	'Not patchable',
	'Patchable',
	'Already patched or stuck on update',
	'Probably patchable',
]

MENU_SPW_ACTS = {
	'read':		'Reading',
	'write':	'Writing',
	'verify':	'Verifying',
	'erase':	'Erasing',
}

STR_SECONDS				= '{:0.0f} seconds'
STR_PORTS_LIST			= 'Serial ports'
STR_MAIN_MENU			= 'Main menu'
STR_FILE_LIST			= 'Files list'
STR_NOR_INFO			= 'NOR dump info'
STR_ADDITIONAL			= 'Additional tools'
STR_SYSCON_INFO			= 'Syscon dump info'
STR_COMPARE				= 'Compare'
STR_HELP				= 'Help'
STR_ACTIONS				= 'Actions'
STR_COREOS_SWITCH		= 'CoreOS switch'
STR_SWITCH_PATTERNS		= 'Switch patterns'
STR_MEMCLOCK			= 'Memory clock'
STR_SAMU_BOOT			= 'SAMU boot'
STR_SYSFLAGS			= 'System flags'
STR_SVNS_ENTRIES		= 'SNVS entries'
STR_APATCH_SVNS			= 'SNVS auto patching'
STR_MPATCH_SVNS			= 'SNVS manual patcher'
STR_NOR_VALIDATOR		= 'NOR validator'
STR_NOR_FLAGS			= 'NOR flags'
STR_NOR_EXTRACT			= 'NOR extractor'
STR_NOR_BUILD			= 'NOR builder'
STR_HDD_KEY				= 'HDD eap key'
STR_2BLS_BUILDER		= '2BLS builder'
STR_UNPACK_2BLS			= '2BLS unpacker'
STR_EMC_CFW				= 'EMC CFW (Aeolia)'
STR_EAP_KEYS			= 'EAP keys'
STR_SC_BOOT_MODES		= 'Bootmode records'
STR_INFO				= 'Info'
STR_SC_READER			= 'Syscon reader'
STR_SPIWAY				= 'SPIway by Judges & Abkarino'

STR_NO_INFO				= '- No info -'
STR_OFF					= 'Off'
STR_ON					= 'On'
STR_WARNING				= 'Warning'
STR_HELP				= 'Help'
STR_UNKNOWN				= '- Unknown -'
STR_YES					= 'Yes'
STR_NO					= 'No'
STR_PROBABLY			= 'Probably'
STR_NOT_SURE			= 'not sure'
STR_DIFF				= 'Different'
STR_NOT_FOUND			= 'not found'
STR_BAD_SIZE			= 'bad size'
STR_OK					= 'OK'
STR_FAIL				= 'Fail'
STR_CANCEL				= 'Cancel'
STR_IS_PART_VALID		= '[{}] {} FW {}'
STR_SNVS_ENTRIES		= '{} records found at 0x{:5X}'
STR_SERIAL_MONITOR		= 'Terminal'

STR_NO_PORTS			= ' No one serial port was found'
STR_PORT_UNAVAILABLE	= ' Selected port is unavailable'
STR_PORT_CLOSED			= ' Port is closed'
STR_STOP_MONITORING		= ' Monitoring was stopped by user'

STR_EMC_CFW_WARN		= ' Currently EMC CFW is only for 10xx/11xx PS4 Fat'
STR_EMC_NOT_FOUND		= ' EMC FW was not found'
STR_DECRYPTING			= ' Decrypting'
STR_ENCRYPTING			= ' Encrypting'
STR_PATCHING			= ' Patching'
STR_EXPERIMENTAL		= ' * - experimental functions'
STR_PERFORMED			= ' Performed action: '

STR_EMPTY_FILE_LIST		= ' File list is empty'
STR_NO_FOLDER			= ' Folder {} doesn\'t exists'
STR_EXTRACTING			= ' Extracting sflash0 to {} folder'
STR_FILES_CHECK			= ' Checking files'
STR_BUILDING			= ' Building file {}'

STR_DONE				= ' All done'
STR_PROGRESS			= ' Progress {:2d}% '
STR_WAIT				= ' Please wait...'
STR_WAITING				= ' Waiting...'
STR_SET_TO				= ' {} was set to [{}]'
STR_ABORT				= ' Action was aborted'
STR_FILENAME			= ' Filename: '

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
STR_LAST_SC_ENTRIES		= ' Showing [{}/{}] entries of active block [{}]'
STR_MEMCLOCK_SET		= ' GDDR5 frequency was set to {:d}MHz [0x{:02X}]'

STR_RECOMMEND			= ' Recommended method [{}]'
STR_PATCH_CANCELED		= ' Patch was canceled'
STR_PATCH_SUCCESS		= ' Successfully removed {} entries'
STR_PATCH_SAVED			= ' Patch was saved to {}'
STR_PATCH_INDEXES		= ' Last 08-0B - {} | Previous 08-0B - {}\n'
STR_SC_BLOCK_SELECT		= ' Select data block [0-{}] or show flat [f] '
STR_MPATCH_INPUT		= ' How many records to clean (from end): '
STR_CHOICE				= ' Make choice: '
STR_BACK				= ' Press [ENTER] to go back'
STR_MEMCLOCK_INPUT		= ' Setup frequency [400 - 2000] / [0 set default (0xFF)] MHz '
STR_SAMU_INPUT			= ' Setup SAMU [0 - 255] / [default is 255 (0xFF)] '
STR_TOO_MUCH			= ' {} is too much, maximum value is {}'
STR_SC_BLOCK_CLEANED	= ' Block [{}] was entirely cleaned'
STR_REBUILD_REQUIRED	= ' You need rebuild SNVS at first to perform this action'
STR_SC_NO_BM			= ' Boot modes records were not found!'
STR_SC_ACTIVE_BM		= ' It\'s already active boot mode!'

STR_UNPATCHABLE			= ' Can\'t patch!'
STR_SYSCON_BLOCK		= ' Block [{}/{}] has [{}/{}] entries | Active block is [{}]\n'
STR_PARTITIONS_CHECK	= ' Checking partitions'
STR_ENTROPY				= ' Entropy statistics'
STR_MAGICS_CHECK		= ' Checking magics'
STR_SNVS_ENTRY_INFO		= 'Block {} #{:03d} Offset 0x{:04X}'
STR_DUPLICATES			= ' {} duplicate(s) found {}'

STR_FW_VERSION			= ' FW version {} / Active slot {}'

STR_COMPARE_RESULT		= ' {} | Result: {}'
STR_INCORRECT_SIZE		= ' {} - incorrect dump size!'
STR_FILE_NOT_EXISTS		= ' File {} doesn\'t exist!'
STR_ERROR_FILE_REQ		= ' You need to select file first'
STR_SAVED_TO			= ' Saved to {}'
STR_SAVING_TO			= ' Saving to {}'
STR_ERROR_INPUT			= ' Incorrect input'
STR_ERROR_DEF_VAL		= ' Setting default values'
STR_ERROR_CHOICE		= ' Invalid choice'
STR_OUT_OF_RANGE		= ' Value is out of range!'
STR_FILES_MATCH			= ' Files are equal'
STR_FILES_MISMATCH		= ' Files mismatch'
STR_SIZES_MISMATCH		= ' Sizes mismatch!'

STR_CHOOSE_AREA			= ' Choose area: '
STR_INPUT_BLOCK			= ' Input start block [count]: '
STR_INPUT_SAVE_IM		= ' Save all intermediate files? [y] '
STR_USE_NEWBLOBS		= ' Use new key blobs? [y] '
STR_CONFIRM_SEPARATE	= ' Save as separate file? [y] '
STR_CONFIRM				= ' Input [y] to continue: '
STR_CURRENT				= ' Current: '
STR_GO_BACK				= ' Go back'
STR_SC_BM_SELECT		= ' Select boot mode variant [1-{}] '
STR_OPEN_IN_SCTOOL		= ' Open file in syscon tool? [y] '
STR_FLASH_PATCHED		= ' Flash patched to console (SPIway)? [y] '

STR_READING_DUMP_N		= ' Reading dump {}'
STR_CHIP_NOT_RESPOND	= ' Chip doesn\'t respond, check wiring and push reset button'
STR_HOW_MUCH_DUMPS		= ' How much dumps to read? [max 10] '

STR_EMC_CMD_MODE		= 'Turning EMC cmd mode [{}]'

STR_CHIP_CONFIG			= ' Chip config'
STR_FILE_INFO			= ' File info'
STR_VERIFY				= ' Verify'

STR_SPW_PROGRESS		= 'Block %03d [%d KB / %d KB] %d%% %s '
STR_SPW_ERROR_CHIP		= 'Unsupported chip!'
STR_SPW_ERROR_VERSION	= 'Unsupported version! (v%d.%02d required)'
STR_SPW_ERROR_ERASE		= 'Error erasing chip!'
STR_SPW_ERROR_ERASE_BLK	= 'Block %d - error erasing block'
STR_SPW_ERROR_DATA_SIZE	= 'Incorrent data size %d'
STR_SPW_ERROR_LENGTH	= 'Incorrect length %d != %d!'
STR_SPW_ERROR_BLK_CHK	= 'Error! Block verification failed (block=%d)'
STR_SPW_ERROR_WRITE		= 'Error while writing!'
STR_SPW_ERROR_READ		= 'Teensy receive buffer timeout! Disconnect and reconnect Teensy!'
STR_SPW_ERROR_VERIFY	= 'Verification error!'
STR_SPW_ERROR_PROTECTED	= 'Device is write-protected!'
STR_SPW_ERROR_UNKNOWN	= 'Received unknown error! (Got 0x%02x)'
STR_SPW_ERROR_UNK_STATUS= 'Unknown status code!'
STR_SPW_ERR_BLOCK_ALIGN	= 'Expecting file size to be a multiplication of block size: %d'
STR_SPW_ERR_DATA_SIZE	= 'Data is %d bytes long (expected %d)!'
STR_SPW_ERR_OVERFLOW	= 'Chip has %d blocks. Writing outside the chip\'s capacity!'

STR_INFO_MONITOR = ''\
' Ctrl+Q [enter] - quit monitor\n'\
' Ctrl+R [enter] - restart monitor\n'\
' Ctrl+E [enter] - toggle EMC cmd mode (adds checksum after cmd)'

STR_ABOUT_SPIWAY = 'About SPIway'
STR_INFO_SPIWAY = ''\
' SPIway - sflash r/w with random block access support (Teensy++ 2.0)\n'\
' Look at </assets/hw/spiway> folder for diagrams and Teensy\'s FW\n'\
' More info at PSDevWiki: '

STR_ABOUT_SC_GLITCH = 'About Syscon Glitch'
STR_INFO_SC_GLITCH = ''\
' Syscon reader by DarkNESmonk (Arduino Nano V3 CH340)\n'\
' Look at </assets/hw/syscon_reader> folder for more info'

STR_ABOUT_SC_BOOTMODES = 'About boot modes'
STR_INFO_SC_BOOTMODES = ''\
' Boot mode records are encrypted, so we can\'t detect its purpose\n'\
' You should try each of them by yourself to determine what is it for\n'\
' Keep in mind: some records may have duplicates (marked with color)'

STR_OVERCLOCKING = ''\
' Dangerous operation!\n\n'\
' Most GDDR5 runs at 6000-8000 MHz. GDDR5 is quad pumped [x4]\n'\
' GDDR5 at 8000 MHz technically runs at 2000 MHz\n'\
' If you have problems, decrease frequency to 1000 MHz\n'\
'\n'\
' Effective GDDR5 clock is 1350 MHz\n'\
' The frequency is selected experimentally\n'\
' - Too high value can lead to LOADBIOS -8 or DCT [*] error\n'\
' - Too low value leads to AMDINIT error'

STR_ABOUT_EAPKEYS = 'About eap keys'
STR_INFO_EAPKEYS = ''\
' Eap key may be 0x40 and 0x60 bytes length\n'\
' PS4 10xx/11xx models usually have only one key\n'\
' And 12xx/Slim/PRO models have backup key\n'\

STR_IMMEDIATLY = ''\
' Be careful: All patches are applied immediatly to the file!'

STR_PATCHES = STR_IMMEDIATLY + '\n'\
' Will switch value between available values for chosen option'

STR_DOWNGRADE = ''\
' Dangerous operation!\n\n'\
' Slot switching is used for FW revert (downgrade).\n'+\
' It also fixes "loadbios" error.\n'\
' Make sure you have backup of stock sFlash dump and SYSCON.\n'\
' Syscon patching required! Otherwise you\'ll get "loadbios" error.\n'\
' Console will not boot normally.'

STR_ABOUT_MPATCH = 'Manual patch instructions'
STR_INFO_SC_MPATCH = ''\
' Every record has 16 bytes length. First byte is always "A5"\n'\
' The second byte is record "type" usualy in range [0x00-0x30]\n'\
' Firmware update takes 4 records with types {}\n'\
' To cancel last fw update we need to clean these 4 records (fill 0xFF)\n'\
' If there are {},{} types after {} patch is impossible\n'\
' backup slot is already erased, you\'ll got checkUpdVersion error'

STR_ABOUT_EAP = 'About EAP keys'
STR_INFO_HDD_EAP = ''\
' These keys allow you to explore PS4 HDD files with PC\n'\
' You can find additional info by visiting:\n '\

STR_ABOUT_EMC_CFW = 'About EMC CFW'
STR_INFO_EMC_CFW = ''\
' Use at your own risk!\n'\
' Only for Aeolia (PS4 Fat 10xx/11xx)\n'\
' Grants control over the southbridge and syscon\n\n'\
' Additional info:\n '

STR_APP_HELP = ''\
' Usage: ps4-wee-tools [params] \n'\
'\n'\
' Params: \n\n'\
'  <file>              : load appropriate tool for supplied file\n'\
'  <folder>            : build dump with files from supplied folder\n'\
'  <file1> <file2> ... : compare files (with MD5 info)\n'\
'  --help              : show this help screen\n'\
'\n'\
' Home: '
