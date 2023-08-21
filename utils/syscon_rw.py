#==========================================================
# spiway lib by hjudges
# part of ps4 wee tools project
#==========================================================

import time, sys
from lang._i18n_ import *
from utils.serial import WeeSerial



class SysconRWTool:
	
	class cmd:
		PING			= 0		# Check if Syscon tool connected and get its version major value
		INFO			= 1		# Check if Syscon tool connected and get its version minor value + free ram size
		READ_BLOCK		= 2		# Read block data
		READ_CHIP		= 3		# Read full chip data
		ERASE_BLOCK		= 4		# Erase block data
		ERASE_CHIP		= 5		# Erase full chip data
		WRITE_BLOCK		= 6		# Write block data
		WRITE_BLOCK_EX	= 7		# Extended Write block data
		SET_DATA		= 0x0A	# Set data to be written into syscon write buffer
		INIT			= 0x10	# Initialize syscon
		UNINIT			= 0x20	# Uninitialize syscon
		RESET			= 0x80	# Reset syscon tool
	
	class block:
		
		BOOT0_BLOCKS		= 4
		FLASH_START			= 0
		FLASH_PART_START	= 4
		FLASH_END			= 511
		FW					= 384
		SNVS_NVS_START		= 384
		SNVS_NVS_END		= 511
		SNVS_NVS			= SNVS_NVS_END - SNVS_NVS_START
		DEBUG_SETTING_OFFSET = 0xC3
	
	class msg:
		OK				= 0x00
		ERR_INT			= 0xF0
		ERR_READ		= 0xF1
		ERR_ERSASE		= 0xF4
		ERR_WRITE		= 0xF6
		ERR_CMD_LEN		= 0xFA
		ERR_CMD_EXEC	= 0xFE
		ERR				= 0xFF

#serialPort - 115200