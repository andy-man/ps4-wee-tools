#==============================================================
# PS4 Wee Tools
# app entry point
#==============================================================
import os, sys
import tools.Tools as Tools
import tools.SFlashTools as SFlashTools
from lang._i18n_ import UI



def main(args):
	
	UI.setTitle()
    
	args.pop(0)

	if len(args) == 2:
		if args[0].replace('-', '', 2) == 'parts':
			return SFlashTools.screenPartitionsInfo(args[1])
		# Quick Legitimate patch (check)
		if os.path.isfile(args[0]) and os.path.isfile(args[1]):
			if not Tools.quickLegitimatePatch(args):
				Tools.screenCompareFiles(args)
	elif len(args) >= 2:
		Tools.screenCompareFiles(args)
	elif len(args) == 1:
		if args[0].replace('-', '', 2) in ['help','h','?']:
			Tools.screenHelp()
		elif not Tools.launchTool(args[0]):
			Tools.screenFileSelect(args[0])
	else:
		Tools.screenMainMenu()



main(sys.argv)