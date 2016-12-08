#!/usr/bin/python3

import sys
import os
from pathlib import Path
import getopt
import serial_d302

def usage():
    print("-d DEVICE")
    print("-v")
    print("-h")

def d10(hex_string):
    read_CID_dec = int(hex_string[:2], 16)
    read_FC_NUM_dec = int(hex_string[2:], 16)
    print("D10:")
    print("Client ID: " + str(read_CID_dec))
    print("Number: " + str(read_FC_NUM_dec))

def w26(hex_string):
    read_CID_dec = int(hex_string[:2], 16)
    read_FC_dec = int(hex_string[2:4], 16)
    read_NUM_dec = int(hex_string[6:], 16)
    print("W26:")
    print("Client ID: " + str(read_CID_dec))
    print("FC: " + str(read_FC_dec))
    print("Number: " + str(read_NUM_dec))

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:v")
except getopt.GetoptError as err:
    # print help information and exit:
    print(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
device = None
verbose = False
for o, a in opts:
    if o == "-v":
        verbose = True
    elif o in ("-h"):
        usage()
        sys.exit()
    elif o in ("-d"):
        device = a
    else:
        assert False, "unhandled option"

if device == None:
   print("No device")
   usage()
   sys.exit(2)

print("Using device: " + device)

d302 = serial_d302.d302()

if device not in d302.serial_ports():
   print("Device not found")
   sys.exit(2)

if not d302.open_port(device):
   print("Error opening device")
   sys.exit(2)

serial_answer = d302.read_message()
if serial_answer != '':
   print("Answer: " + serial_answer)
   print("Checksum: " + serial_answer[-3:-2])
   hex_string = serial_answer[8:-4];
   print("HEX: " + hex_string)
   d10(hex_string)
   w26(hex_string)
else:
   print("NO CARD")

d302.close_port()
