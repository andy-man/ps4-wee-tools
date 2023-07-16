#==============================================================
# PS4 Wee Tools
#==============================================================
import sys
import tools.Tools as Tools



def main(args):
    
    args.pop(0)
    
    if len(args) >= 2:
    	Tools.screenCompareFiles(args)
    elif len(args) == 1:
    	if args[0] in ['help','-help','h','-h','?']:
    		Tools.screenHelp()
    	else:
    		Tools.screenFileSelect(args[0])
    else:
    	Tools.screenFileSelect()



main(sys.argv)