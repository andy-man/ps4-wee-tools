#==============================================================
# PS4 Syscon Tools
# part of ps4 wee tools project
# https://github.com/andy-man/ps4-wee-tools
#==============================================================
import os
from lang._i18n_ import *
import utils.utils as Utils
import utils.syscon as Syscon
import utils.utils as Utils
import tools.Tools as Tools

# Screens

def screenAdvSysconTools(file):
	
    MENU_SC_ADV_ACTIONS[2-1] = UI.dark(MENU_SC_ADV_ACTIONS[2-1])
    MENU_SC_ADV_ACTIONS[5-1] = UI.dark(MENU_SC_ADV_ACTIONS[5-1])
    MENU_SC_ADV_ACTIONS[6-1] = UI.dark(MENU_SC_ADV_ACTIONS[6-1])

    while True:

        UI.clearScreen()
        print(TITLE+UI.getTab(STR_ADDITIONAL))
		
        UI.showMenu(MENU_SC_ADV_ACTIONS,1)

        UI.showStatus()
		
        choice = input(STR_CHOICE)

        if choice == '':
            break
        elif choice == '1':
            resetSysconCounters(file)
        elif choice == '2':
            UI.setStatus(STR_NIY)
        elif choice == '3':
            screenBootModes(file)
        elif choice == '4':
            print()
            print(UI.highlight(STR_NIY))
            print(UI.warning(' Using Legacy method'))
            cleanSyscon(file)
        elif choice == '5':
            UI.setStatus(STR_NIY)
        elif choice == '6':
            UI.setStatus(STR_NIY)
        else:
            UI.setStatus(STR_ERROR_CHOICE)

    return



def screenBootModes(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_ABOUT_SC_BOOTMODES))
	print(UI.warning(STR_INFO_SC_BOOTMODES))
	
	print(UI.getTab(STR_SC_BOOT_MODES))
	
	with open(file, 'r+b') as f:
		data = f.read()
		SNVS = Syscon.NVStorage(Syscon.SNVS_CONFIG, Syscon.getSysconData(f, 'SNVS'))
		entries = SNVS.getAllDataEntries()
	
	modes = Syscon.getEntriesByType(Syscon.SC_TYPES_BOOT, entries)
	
	if len(modes) <= 0:
		print(UI.warning(STR_SC_NO_BM))
		input(STR_BACK)
		return
	
	items = []
	duplicates = []
	
	for i in range(len(modes)):
		inf = Syscon.getRecordPos(modes[i], SNVS)
		edata = []
		for k in range(len(Syscon.SC_TYPES_BOOT)):
			edata.append(Utils.hex(Syscon.NvsEntry(entries[modes[i]+k]).getData(),''))
		
		color = ''
		
		if edata in items:
			color = Clr.fg.orange
			duplicates.append(str(i+1))
		else:
			items.append(edata)
		
		item = Clr.fg.pink + edata[0] + Clr.reset + ' ... ' + Clr.fg.pink + edata[-1] + Clr.reset
		print(color + ' % 2d: Block %d (#%03d) at 0x%04X'%(i+1, inf['block'], inf['num'], inf['offset']) + Clr.reset + ' ' + item)
	
	print()
	
	if len(duplicates):
		print(STR_DUPLICATES%(len(duplicates), ','.join(duplicates)))
	
	UI.showStatus()
	
	choice = input(UI.DIVIDER+STR_SC_BM_SELECT%(len(modes)))
	
	try:
		c = int(choice)
		
		out_file = Utils.getFilePathWoExt(file,True)
		
		if c == len(modes):
			UI.setStatus(' It\'s already active boot mode!')
		elif c > 0 and c < len(modes):
			ofile = out_file+'_bootmode_%d.bin'%(c)
			sel = modes[c-1]
			act = modes[-1]
			# replace last(active) with selected
			for i in range(len(Syscon.SC_TYPES_BOOT)):
				temp = entries[act + i]
				entries[act + i] = entries[sel + i]
				entries[sel + i] = temp
			
			Utils.savePatchData(ofile, data, [{'o':Syscon.SC_AREAS['SNVS']['o'], 'd':SNVS.getRebuilded(entries)}])
			UI.setStatus(STR_SAVED_TO%ofile)
	except:
		return
	
	screenBootModes(file)

# Functions

def resetSysconCounters(file):
	
	with open(file, 'rb') as f:
		data = f.read()
		SNVS = Syscon.NVStorage(Syscon.SNVS_CONFIG, Syscon.getSysconData(f, 'SNVS'))
	
	ofile = Utils.getFilePathWoExt(file, True) + '_owc_reset.bin'
	
	with open(ofile, 'wb') as f:
		f.write(data)
		Syscon.setSysconData(f, 'SNVS', SNVS.getRebuilded())
	
	UI.setStatus(STR_SAVED_TO%ofile)



def cleanSyscon(file):
	
	c = input(UI.highlight(STR_INPUT_DESTROY_PREV+STR_Y_OR_CANCEL))
	full = True if c.lower() == 'y' else False
	
	with open(file, 'rb') as f:
		data = f.read()
		SNVS = Syscon.NVStorage(Syscon.SNVS_CONFIG, Syscon.getSysconData(f, 'SNVS'))
	
	clean = []
	entries = SNVS.getAllDataEntries()
	
	if full:
		# Full clean - only last FW records will be saved
		for i in range(len(entries)):
			if entries[i][1] in Syscon.SC_TYPES_BOOT + Syscon.SC_TYPES_MODES:
				clean.append(entries[i])
		
		inds = Syscon.getEntriesByType(Syscon.SC_TYPES_UPD, entries)
		if len(inds) >= 2: # add previous FW records
			items = entries[inds[-2]:inds[-2]+len(Syscon.SC_TYPES_UPD)]
			print(items)
			clean += items
		if len(inds) >= 1: # add current FW records
			items = entries[inds[-1]:inds[-1]+len(Syscon.SC_TYPES_UPD)]
			print(items)
			clean += items
	else:
		# Regular clean preserves all FW records
		for i in range(len(entries)):
			if entries[i][1] in Syscon.SC_TYPES_BOOT + Syscon.SC_TYPES_MODES + Syscon.SC_TYPES_UPD:
				clean.append(entries[i])
	
	ofile = Utils.getFilePathWoExt(file,True) + '_clean'+('_full' if full else '')+'.bin'
	
	with open(ofile, 'wb') as f:
		f.write(data)
		Syscon.setSysconData(f, 'SNVS', SNVS.getRebuilded(clean))
	
	UI.setStatus(STR_SAVED_TO%ofile)