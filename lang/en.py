#==========================================================
# Default language [EN]
# part of ps4 wee tools project
# https://github.com/andy-man/ps4-wee-tools
#==========================================================

MENU_SC_REBUILD_MODES = [
	'Normal mode (Choose FW, default values for rest / All (12) types)',
	'Minimal setup (Choose first two types and FW / 3 types)',
	'Expert mode (Adjust all (12) types)',
]

MENU_NVS_COPY = [
	'Replace %s with backup (%s <= %s)',
	'Replace backup with %s (%s => %s)',
]

MENU_EAP_KEYS = [
	'Replace A with B (key_a <= key_b)',
	'Replace B with A (key_a => key_b)',
	'Fix magic A *',
	'Fix magic B *',
	'Generate new A,B keys (length 0x60) *',
	'Generate new A,B keys (length 0x40) *',
	'Clean key B *',
]

MENU_FLASHER = [
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

MENU_SERIAL_MONITOR = {
	'Ctrl+Q':'quit monitor',
	'Ctrl+R':'restart monitor',
	'Ctrl+E':'toggle EMC cmd mode',
	'Ctrl+B':'show bytecodes < 0x20',
	'Ctrl+L':'log to file',
}

MENU_TOOL_SELECTION = [
	'File browser',
	'Terminal (UART)',
	'sFlash r/w (SPIway by Judges)',
	'Syscon r/w (SCTool by Abkarino & EgyCnq)',
	'Syscon r/o (SCRead by DarkNESmonk)',
	'Syscon w/o (For stock Renesas RL78)',
	'Change app\'s language',
	'Exit',
]

MENU_FILE_SELECTION = {
	'a':'Show all files / Toggle filters [bin,pup]',
	'f':'Build sflash0 dump',
	'b':'Build 2BLS/PUP',
	'r':'Batch rename (extract dump info to filename)',
	'c':'Compare files in current folder',
	'q':'Quit / Go back',
}

MENU_EXTRA_FLASHER = {
	's':'Select file',
	'f':'Launch Tool for this file',
	'q':'Quit / Go back',
}

MENU_EXTRA = {
	's':'Select another file',
	'f':'Flash this file (full/parts) back to IC',
	'r':'Rename file to canonical name',
	'q':'Quit / Go back',
}

MENU_SFLASH_ACTIONS = [
	'Flags (UART, RNG, Memtest, etc)',
	'Memory clocking (GDDR5)',
	'SAMU boot flag',
	'Switch CoreOS slot (FW revert)',
	'Legit CoreOS Patch',
	'Patch Southbridge',
	'Patch Torus (WiFi+BT)',
	'Additional tools',
]

MENU_SFLASH_ADV_ACTIONS = [
	'Extract partitions from sFlash0',
	'Build sFlash0 from extracted files',
	'View / Recover NVS areas (1C9, 1CA)',
	'View / Recover EAP key',
	'Get HDD keys = decrypt EAP key = create [keys.bin]',
	'Create EMC cfw (only for Fat 1xxx/11xx)',
	'Base validation and entropy stats',
	'Analyze and recover of corrupted partition',
]

MENU_SC_ACTIONS = [
	'Toggle Debug',
	'Auto SNVS patch',
	'SNVS block viewer',
	'NVS block viewer',
	'Manual SNVS patch',
	'Additional tools',
]

MENU_SC_ADV_ACTIONS = [
	'Reset SNVS counters',
	'Mode select (00-03)',
	'Boot modes (04-07)',
	'Rebuild Syscon\'s SNVS (Factory Reset)',
	'Recover Syscon\'s FW',
	'Convert for Renesas flasher (Motorolla S28)',
]

MENU_PATCHES = [
	'Method A - last 08-0B will be deleted (4 records)',
	'Method B - last 08-0B and below will be cleaned (%d records)',
	'Method C - clean everything below previous 08-0B (%d records)',
	'Method D - clean everything below last 08-0B (%d records)',
	'Method E - clean previous 08-0B and below (%d records)',
]

MENU_SC_STATUSES = [
	'Overwritten CoreOs slot',
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

STR_LANGUAGE			= 'Language'
STR_SECONDS				= '%0.0f seconds'
STR_NVS_AREAS			= 'NVS areas'
STR_PORTS_LIST			= 'Serial ports'
STR_MAIN_MENU			= 'Main menu'
STR_FILE_LIST			= 'Files list'
STR_SFLASH_INFO			= 'sFlash dump info'
STR_ADDITIONAL			= 'Additional tools'
STR_SYSCON_INFO			= 'Syscon dump info'
STR_COMPARE				= 'Compare'
STR_HELP				= 'Help'
STR_ACTIONS				= 'Actions'
STR_COREOS_SWITCH		= 'CoreOS slot switch'
STR_SWITCH_PATTERNS		= 'Switch patterns'
STR_MEMCLOCK			= 'Memory clock'
STR_SAMU_BOOT			= 'SAMU boot'
STR_SYSFLAGS			= 'System flags'
STR_NVS_ENTRIES			= 'Syscon %s entries'
STR_APATCH_SVNS			= 'SNVS auto patching'
STR_MPATCH_SVNS			= 'SNVS manual patcher'
STR_SFLASH_VALIDATOR	= 'sFlash validator'
STR_SFLASH_FLAGS		= 'sFlash flags'
STR_SFLASH_EXTRACT		= 'sFlash extractor'
STR_SFLASH_BUILD		= 'sFlash builder'
STR_HDD_KEY				= 'HDD eap key'
STR_2BLS_BUILDER		= '2BLS builder'
STR_UNPACK_2BLS			= '2BLS unpacker'
STR_UNPACK_PUP			= 'Decrypted PUP unpacker'
STR_EMC_CFW				= 'EMC CFW (Aeolia)'
STR_EAP_KEYS			= 'EAP keys'
STR_SC_BOOT_MODES		= 'Bootmode records'
STR_INFO				= 'Info'
STR_SC_READER			= 'Syscon reader'
STR_SPIWAY				= 'SPIway by Judges & Abkarino'
STR_SCF					= 'Syscon Flasher by Abkarino & EgyCnq'
STR_LEG_PATCH			= 'Legitimate CoreOS Patch'
STR_PART_RECOVERY		= 'Partition recovery'
STR_PART_ANALYZE		= 'Partition analyzing'
STR_PART_LIST			= 'Partitions list'
STR_PARTS_INFO			= 'Partitions info'
STR_WIFI_PATCHER		= 'WiFi patcher'
STR_SB_PATCHER			= 'Southbridge patcher'
STR_RL78FLASH			= 'RL78 Flasher'
STR_SC_REBUILDER		= 'Syscon Rebuilder'

STR_ALL					= 'All'
STR_UNIQUE				= 'Unique'
STR_BACKUP				= 'Backup'
STR_EQUAL				= 'Equal'
STR_NOT_EQUAL			= 'Not equal'
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
STR_IS_PART_VALID		= '[%s] %s FW %s'
STR_SNVS_ENTRIES		= '%d records found at 0x%05X'
STR_SERIAL_MONITOR		= 'Terminal'
STR_ELAPSEDTIME			= 'Elapsed time'

STR_NO_PORT_CHOSEN		= ' No port was chosen'
STR_NO_PORTS			= ' No one serial port was found'
STR_PORT_UNAVAILABLE	= ' Selected port is unavailable'
STR_PORT_CLOSED			= ' Port is closed'
STR_STOP_MONITORING		= ' Monitoring was stopped by user'

STR_RESTART_APP			= ' Restart App to apply changes'
STR_GENERATE_ALL_PS		= ' Generate all patches'
STR_ACTION_NA			= ' No action is available %s'
STR_EMC_CFW_WARN		= ' Currently EMC CFW is only for 10xx/11xx PS4 Fat'
STR_EMC_NOT_FOUND		= ' EMC FW was not found'
STR_DECRYPTING			= ' Decrypting'
STR_ENCRYPTING			= ' Encrypting'
STR_PATCHING			= ' Patching'
STR_EXPERIMENTAL		= ' * - experimental functions'
STR_PERFORMED			= ' Performed action: '

STR_EMPTY_FILE_LIST		= ' File list is empty'
STR_NO_FOLDER			= ' Folder %s doesn\'t exists'
STR_EXTRACTING			= ' Extracting sflash0 to %s folder'
STR_FILES_CHECK			= ' Checking files'
STR_BUILDING			= ' Building file %s'

STR_DONE				= ' All done'
STR_PROGRESS			= ' Progress %02d%% '
STR_PROGRESS_KB			= ' Progress: %dKB / %dKB'
STR_WAIT				= ' Please wait...'
STR_WAITING				= ' Waiting...'
STR_SET_TO				= ' %s was set to [%s]'
STR_ABORT				= ' Action was aborted'
STR_FILENAME			= ' Filename: '

STR_VALIDATE_NVS_CHECK	= ' Checking NVS areas'
STR_ACT_SLOT			= ' Active slot: %s [0x%02X]'
STR_NIY					= ' This feature is available in PRO version only'
STR_CLEAN_FLAGS			= ' Clean all system flags'
STR_UNK_FILE_TYPE		= ' Unknown file type'
STR_UNK_CONTENT			= ' Unknown content'
STR_UART				= ' UART is set to '
STR_DEBUG				= ' Syscon debug is set to '

STR_DIFF_SLOT_VALUES	= ' Values in slots are different!'
STR_SYSFLAGS_CLEAN		= ' Sys flags were cleared. Tip: turn on UART'
STR_SAMU_UPD			= ' SAMU flag was set to '
STR_DOWNGRADE_UPD		= ' Slot switch was set to: '
STR_LAST_SC_ENTRIES		= ' Showing last [%d/%d] entries of active block [%d]'
STR_MEMCLOCK_SET		= ' GDDR5 frequency was set to %dMHz [0x%02X]'

STR_RECOMMEND			= ' Recommended method [%s]'
STR_PATCH_CANCELED		= ' Patch was canceled'
STR_PATCH_SUCCESS		= ' Successfully removed %d entries'
STR_PATCH_SAVED			= ' Patch was saved to %s'
STR_RENAMED				= ' Renamed to %s'

STR_SC_BLOCK_SELECT		= ' Select data block [0-%d] | View Flat/Block [f] '
STR_MPATCH_INPUT		= ' How many records to clean (from end): '
STR_CHOICE				= ' Make choice: '
STR_BACK				= ' Press [ENTER] to go back'
STR_MEMCLOCK_INPUT		= ' Setup frequency [400 - 2000] / [0 set default (0xFF)] MHz '
STR_SAMU_INPUT			= ' Setup SAMU [0 - 255] / [default is 255 (0xFF)] '
STR_TOO_MUCH			= ' %d is too much, maximum value is %d'
STR_SC_BLOCK_CLEANED	= ' Block [%d] was entirely cleaned'
STR_OWC_RESET_REQUIRED	= ' You need reset SNVS counters at first to perform this action'
STR_SC_NO_BM			= ' Boot modes records were not found!'

STR_UNPATCHABLE			= ' Can\'t patch!'
STR_SYSCON_BLOCK		= ' Block [%d/%d] has [%d/%d] entries | Active block is [%d]\n'
STR_PARTITIONS_CHECK	= ' Checking partitions'
STR_ENTROPY				= ' Entropy statistics'
STR_MAGICS_CHECK		= ' Checking magics'
STR_DUPLICATES			= ' %d duplicate(s) found [%s]'
STR_SC_WARN_OVERWITTEN	= ' Warning: CoreOS is probably overwritten'

STR_SNVS_ENTRY_INFO		= 'Block %d #%03d Offset 0x%04X'
STR_SC_TOGGLE_FLATDATA	= 'Toggle between Flat/Block'
STR_SH_DUPLICATES		= 'Show / Hide duplicates'
STR_NO_ENTRIES			= 'No entries found'
STR_SKIPPED				= 'Skipped'
STR_SKIP_ENTRY			= 'Skip this type of entry'
STR_NO_FILE_SEL			= 'No file selected'

STR_INCORRECT_SIZE		= ' %s has incorrect dump size!'
STR_FILE_NOT_EXISTS		= ' File %s doesn\'t exist!'
STR_FILE_EXISTS			= ' Filename already exists!'
STR_ERROR_FILE_REQ		= ' You need to select file first'
STR_SAVED_TO			= ' Saved to %s'
STR_ERROR_INPUT			= ' Incorrect input'
STR_ERROR_DEF_VAL		= ' Setting default values'
STR_ERROR_CHOICE		= ' Invalid choice'
STR_ERROR_INFO_READ		= ' Error while reading file data'
STR_OUT_OF_RANGE		= ' Value is out of range!'
STR_FILES_MATCH			= ' Files are equal'
STR_FILES_MISMATCH		= ' Files mismatch'
STR_SIZES_MISMATCH		= ' Sizes mismatch!'
STR_RENAMED_COUNT		= ' %d files were renamed'
STR_FW_RECORDS			= ' FW versions - from Current(1) to Initial(%d)'

STR_SELECT_MODEL		= ' Select model:'
STR_SHOW_DETAILS		= ' Show details?'
STR_Y_OR_CANCEL			= ' [y - yes, * - cancel] '
STR_CHOOSE_AREA			= ' Choose area: '
STR_INPUT_SEL_DUMP		= ' Select second dump?'
STR_INPUT_DESTROY_PREV	= ' Destroy all previous FW (08-0B) records?'
STR_INPUT_BLOCK			= ' Input start block [count]: '
STR_INPUT_SAVE_IM		= ' Save all intermediate files?'
STR_INPUT_USE_SLOTB		= ' Use slot B (active)?'
STR_USE_NEWBLOBS		= ' Use new key blobs?'
STR_CONFIRM_SEPARATE	= ' Save as separate file?'
STR_CONFIRM				= ' Input [y] to continue: '
STR_CURRENT				= ' Current: '
STR_GO_BACK				= ' Go back'
STR_SC_BM_SELECT		= ' Select boot mode variant [1-%d] '
STR_OPEN_IN_SC_TOOL		= ' Open file in Syscon Tool?'
STR_FLASH_FILE			= ' Flash this file to IC?'

STR_READING_DUMP_N		= ' Reading dump %d'
STR_CHIP_NOT_RESPOND	= ' Chip doesn\'t respond, check wiring and push reset button'
STR_HOW_MUCH_DUMPS		= ' How much dumps to read? [max 10] '

STR_EMC_CMD_MODE		= 'Turning EMC cmd mode: [%s]'
STR_SHOW_BYTECODES		= 'Show byte codes < 0x20: [%s]'
STR_MONITOR_STATUS		= 'RX/TX: %d/%d (bytes) Elapsed: %d (sec)'

STR_CHIP_CONFIG			= ' Chip config'
STR_FILE_INFO			= ' File info'
STR_VERIFY				= ' Verify'

STR_SPW_PROGRESS		= 'Block %03d [%d KB / %d KB] %d%% %s '
STR_SPW_ERROR_CHIP		= 'Unsupported chip!'
STR_SPW_ERROR_VERSION	= 'Unsupported version! (v%d.%02d required)'
STR_SPW_ERROR_ERASE		= 'Error erasing chip!'
STR_SPW_ERROR_ERASE_BLK	= 'Block %d - error erasing block'
STR_SPW_ERROR_DATA_SIZE	= 'Incorrect data size %d'
STR_SPW_ERROR_LENGTH	= 'Incorrect length %d != %d!'
STR_SPW_ERROR_BLK_CHK	= 'Error! Block verification failed (block=%d)'
STR_SPW_ERROR_WRITE		= 'Error while writing!'
STR_SPW_ERROR_READ		= 'Teensy receive buffer timeout! Disconnect and reconnect Teensy!'
STR_SPW_ERROR_VERIFY	= 'Verification error!'
STR_SPW_ERROR_PROTECTED	= 'Device is write-protected!'
STR_SPW_ERROR_UNKNOWN	= 'Received unknown error!'
STR_SPW_ERROR_UNK_STATUS= 'Unknown status code!'
STR_SPW_ERR_BLOCK_ALIGN	= 'Expecting file size to be a multiplication of block size: %d'
STR_SPW_ERR_DATA_SIZE	= 'Data is %d bytes long (expected %d)!'
STR_SPW_ERR_OVERFLOW	= 'Chip has %d blocks. Writing outside the chip\'s capacity!'

STR_SCF_ERROR_VERSION	= 'Unsupported version! (v%d.%02d required)'
STR_SCF_ERROR_WRITE_BLK	= 'Error writing block %d'
STR_SCF_ERROR_ERASE_BLK	= 'Error erasing block %d'
STR_SCF_ERROR_READ_BLK	= 'Error reading block %d'
STR_SCF_ERROR_ERASE_CHIP= 'Error during chip erasing'

STR_SCF_ERR_INT			= 'Error during initialization'
STR_SCF_ERR_READ		= 'Read error'
STR_SCF_ERR_ERASE		= 'Erase error'
STR_SCF_ERR_WRITE		= 'Write error'
STR_SCF_ERR_CMD_LEN		= 'Incorrect command length'
STR_SCF_ERR_CMD_EXEC	= 'Error while executing command'
STR_SCF_ERR_UNKNOWN		= 'Received unknown error!'
STR_SCF_ERR_UNK_STATUS	= 'Unknown status code!'
STR_SCF_SAFE_ERASE		= ' Safe erase starting at block #%03d'

STR_CANT_USE			= 'Can\'t use this'
STR_DIFF_SN				= 'Serial numbers are different!'
STR_SSP_EQUAL			= 'Slot switch patterns are equal!'
STR_LP_FIRST_DUMP		= 'First dump'
STR_LP_SECOND_DUMP		= 'Second dump'

STR_CONVERTING_S28		= ' Converting to S28 format'
STR_S28_ALREADY			= ' File format is S28'

STR_USE_EXPERT_M		= ' Choose another model or use expert mode!'
STR_ERR_NO_FW_FOUND		= ' Error: Can not find %s for FW %s in DB'
STR_EXPERT_MODE			= ' Expert mode?'
STR_SELECT_FW_VER		= ' Select fw version'
STR_MODEL				= ' Model'
STR_FW_VER				= ' FW: %s / Slot: %s'
STR_SELECT_MOST_FILE	= ' Select most relevant file: '
STR_NO_FW_FILES			= ' Files are not found! Download files to fws folder:\n [%s]'

STR_ABOUT_SC_REBUILDER = 'About Syscon Rebuilder'
STR_INFO_SC_REBUILDER = ''\
' This util will help you to create custom version of Syscon.\n'\
' You can adjust each type of records in expert mode.\n'\
' Entries are sorted from current to past.\n'\
' * To select previous FW you need to input "2" or more.\n'\
' * Minimal setup consists of 3 types (00-03 + 04-07 + 08-0B)'

STR_ABOUT_RL78FLASH = 'About Stock Syscon'
STR_INFO_RL78FLASH = ''\
' In order to write new blank syscon chip (Renesas RL78G10)\n'\
' you need USB to TTL adapter, wires and some diodes.\n'\
' Wiring diagram can be found in assets/hw/l78flash folder'\

STR_ABOUT_NVS = 'About NVS recovery'
STR_INFO_NVS = ''\
' Swaps corrupted block with backup data (not suitable for 10xx/11xx)\n'\
' Warning - UART and other flags may be overwritten.\n'\
' If you need to set some flags do it after NVS recovery!\n'\

STR_ABOUT_TORUS_PATCH = 'About WiFi patcher'
STR_INFO_TORUS_PATCH = ''\
' Will be useful in case of:\n'\
' - corrupted Torus (WiFi+BT) FW\n'\
' - switching to another IC module'\

STR_ABOUT_SB_PATCH = 'About Southbridge patcher'
STR_INFO_SB_PATCH = ''\
' Will be useful in case of:\n'\
' - corrupted Southbridge FW or "EMC VERSION DOWN" errors\n'\
' - switching to another IC module (CXD90046 => CXD90036)\n'\
' - replacement of APU bundles (21xx => 22xx, 71xx => 72xx)'

STR_INFO_FLASH_TOOLS = ''\
' Flash tools (spiway & syscon flasher) are experimental! Be careful.'\

STR_ABOUT_PART_RECOVERY = 'Partition analyzing and recovery'
STR_INFO_PART_A_R = ''\
' Compares every byte of (SFlash/Syscon) partition with valid files\n'\
' and shows percentage of similarity.\n'\
' Most equal files will be at top of the list.\n'\
' Keep in mind that Southbridge FW consists of emc + eap'

STR_INFO_FW_LINK = ''\
' Put valid emc/eap/torus/syscon files to /fws/ folder\n'\
' You can download it from this repo:\n '

STR_ABOUT_LEG_PATCH = 'About Legitimate CoreOS Patch'
STR_INFO_LEG_PATCH = ''\
' This method is only suitable for working consoles!\n'\
' Because it requires updating via PS4 safe menu\n'\
'\n'\
' 1) Read first dump (if you\'ve not done it already)\n'\
' 2) Update the console to the SAME version via safe mode\n'\
' 3) Read second dump (both slots have equal FW)\n'\
'\n'\
' Now you can patch first dump with data from second one\n'\
' You can drag&drop 2 dumps on wee-tools shortcut to speed up'

STR_ABOUT_SCF = 'About Syscon Flasher'
STR_INFO_SCF = ''\
' Syscon Flasher allows you to r/w original PS4 syscon chip (RL78/G13)\n'\
' Flasher supports only A0x-COLx syscon models\n'\
' Currently hardware part is based on Teensy boards (2.0++/4.0/4.1)\n'\
' Look at </assets/hw/syscon_flasher> for diagrams and Teensy\'s FW\n'\
' More info here: '

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

STR_ABOUT_EAPKEYS = 'About EAP keys'
STR_INFO_EAPKEYS = ''\
' Eap key may be 0x40 and 0x60 bytes length\n'\
' PS4 10xx/11xx models usually have only one key\n'\
' And 12xx/Slim/PRO models have backup key\n'\

STR_IMMEDIATLY = ''\
' Be careful: All patches are applied immediately to the file!'

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
' The second byte is record "type" usually in range [0x00-0x30]\n'\
' Firmware update takes 4 records with types %s\n'\
' To cancel last fw update we need to clean these 4 records (fill 0xFF)\n'\
' If there are %s,%s types after %s patch is impossible\n'\
' backup slot is already overwritten, you\'ll got checkUpdVersion error'

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
' Homepage: '
