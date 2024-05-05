#==========================================================
# TXT file to PY array
# part of ps4 wee tools project
# https://github.com/andy-man/ps4-wee-tools
#==========================================================
import os



def writeVar(f, name, var):
	f.write(name+" = {\n")
	for key in var:
		f.write("'%s' : { 't':%s, 'fw':%s},\n" %(key.lower(), var[key]['t'], var[key]['fw']))
	f.write("}\n\n")

def addEntry(var, md5, type, fw):
	if not md5 in var:
		var[md5] = {'t':type, 'fw':[fw]}
	else:
		var[md5]['fw'].append(fw)



eap_kbl = {}
emc_ipl = {}
torus_fw = {}

fname = 'md5.txt'

if not os.path.exists(fname):
	input('File %s not found'%fname)
	exit(1)
# Using readlines()
f = open(fname, 'r')
Lines = f.readlines()
for line in Lines:
	line = line.strip()
	
	data = line.split()
	if len(data) < 3:
		continue
	
	if line.startswith('eap_kbl_'):
		addEntry(eap_kbl, data[2], data[0][8:12], data[1])
	elif line.startswith('emc_ipl_'):
		addEntry(emc_ipl, data[2], data[0][8:12], data[1])
	elif line.startswith('torus_fw_'):
		addEntry(torus_fw, data[2], data[0][9:13], data[1])

f.close()


f = open("data.py", "w")

writeVar(f, 'EAP_KBL_MD5', eap_kbl)
writeVar(f, 'EMC_IPL_MD5', emc_ipl)
writeVar(f, 'TORUS_FW_MD5', torus_fw)

f.close()

print('eap_kbl %d'%len(eap_kbl))
print('emc_ipl %d'%len(emc_ipl))
print('torus_fw %d'%len(torus_fw))
print()
print('Total %d'%(len(eap_kbl) + len(emc_ipl) + len(torus_fw)))

input()