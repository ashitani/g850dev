#!/usr/bin/env python
#coding: utf-8


import serial
from serial import *
from intelhex import IntelHex
import io as StringIO#python3
#import StringIO #python2
from time import sleep

import sys
import os

def puts(f,ch):
    f.write(ch)
    f.flush()

def send(filename, device, delay=50):

    suffix=os.path.splitext(filename)[-1]

    try:
        f=serial.Serial(port=device,
                        baudrate=9600,
                        bytesize=EIGHTBITS,
                        parity=PARITY_NONE,
                        stopbits=STOPBITS_ONE,
                        timeout=None,
                        xonxoff=False,
                        rtscts=True,
                        write_timeout=None, dsrdtr=False, inter_byte_timeout=None)
    except:
        print("Cannot open device: %s" % device)
        exit()

    dat=[]
    if suffix==".ihx":
        app = IntelHex()
        app.loadhex(filename)
        sio = StringIO.StringIO()
        app[0x100::].write_hex_file(sio)
        dat=sio.getvalue().split('\n')

        maxaddr = app.maxaddr()
        print()
        print("Target: %s"% filename)
        print()
        print("Type your pocket-computer:")
        print()
        print(">MON")
        print("*USER%04X"%maxaddr)
        print("*R")
        print()
        print("please hit enter when you are ready.")
        input()

    elif suffix==".txt":
        print()
        print("Target: %s"% filename)
        print()
        dat=open(filename).readlines().split('\n')
        print("please hit enter when you are ready.")
        input()

    else:
        print("cannot transfer %s file. use ihx or txt" % suffix)
        exit()

    print("Sending...")

    f.reset_output_buffer()

    for line in dat:
        if len(line)==0:
            break
        if line[-1]=='\n':
            line=line[:-1]

        for x in line:
            puts(f,x.encode())
        puts(f,b'\r\n') # CR LF

        #print(line+"\r\n", end="")
        sleep(0.001*delay)

    puts(f,b'\x1a') # End of File
    f.flush()
    f.close()


def receive(device):
    f=serial.Serial(port=device,
                    baudrate=9600,
                    bytesize=EIGHTBITS,
                    parity=PARITY_NONE,
                    stopbits=STOPBITS_ONE,
                    timeout=None,
                    xonxoff=False,
                    rtscts=True,
                    write_timeout=None, dsrdtr=False, inter_byte_timeout=None)

    ans=""
    while(1):
        txt=f.read()
        if txt==b'\x1a':
            break
        ans+=txt

    f.close()
    return ans


