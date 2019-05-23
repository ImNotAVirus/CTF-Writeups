#!/bin/env python3
import os
import re
from time import sleep
from pygdbmi.gdbcontroller import GdbController

#
# Globals
#

DIRNAME = os.path.dirname(os.path.realpath(__file__))
RE_MATCH_ADDY = re.compile(r'0x[0-9a-fA-F]+')
SORTARR_PIE_OFF = 0xdb9

#
# Init GDB
#

gdbmi = GdbController()
gdbmi.write('set cwd ./bin')
gdbmi.write('-file-exec-file ./bin/amicomputable')
gdbmi.write('set disassembly-flavor intel')
gdbmi.write('set environment LD_PRELOAD %s/quick_sort.so' % DIRNAME)
gdbmi.write('run')

print("The PIE offset of the sorting function is: %s" % hex(SORTARR_PIE_OFF))

#
# Search the sort array function
# Cf. Writeup (SOON)
#

sleep(0.5)
gdbmi.send_signal_to_gdb('SIGINT')
gdbmi.interrupt_gdb()

res = gdbmi.write('')
curr_addy = [x['payload']['frame']['addr'] for x in res if x['type'] == 'notify'][0]
curr_addy = int(curr_addy, 16)

print("We just break on: %s" % hex(curr_addy))

sortarr_addy = (curr_addy & 0xFFFFFFFFFFFFF000) + SORTARR_PIE_OFF

print("Sorting function is located at: %s" % hex(sortarr_addy))

#
# Search for our custom Quick Sort function
#

res = gdbmi.write('print sort_array')
msg = [x for x in res if x['type'] == 'console'][0]['payload']
quicksort_addy = int(RE_MATCH_ADDY.findall(msg)[0], 16)

print("Our quick sort function is located at: %s" % hex(quicksort_addy))

#
# Hook the binary sort function
# 48 b8 35 08 40 00 00 00 00 00   mov rax, 0x0000000000400835
# ff e0                           jmp rax
#

print("Let's do some magic things")

gdbmi.write('b *%s' % hex(sortarr_addy))
gdbmi.write('run')
gdbmi.write('set *(short*)%d = 0xb848' % sortarr_addy)                   # mov rax
gdbmi.write('set *(long long*)%d = %d' % (sortarr_addy + 2, quicksort_addy))  # our new sort
gdbmi.write('set *(short*)%d = 0xe0ff' % (sortarr_addy + 10))            # jmp rax
gdbmi.write('continue')

#
# Just get your awesome flag
#    => ECSC{5d12758be6f2a971153c5599339f77b0}
#

res = gdbmi.get_gdb_response(timeout_sec=15)
flag = [x for x in res if x['type'] == 'output'][0]['payload']

print("\nHere is your flag: %s" % flag)

# Close everything
gdbmi.exit()
