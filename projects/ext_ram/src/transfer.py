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

import cv2
import glob
import numpy as np

class UART():
    def __init__(self,device,delay):

        try:
            self.f=serial.Serial(port=device,
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
        self.delay=delay

    def set_delay(self,delay):
        self.delay=delay

    def gets(self):
        ch=self.f.read()
        return int.from_bytes(ch,"little") # python3

    def puts(self,character):
        while(self.f.cts==False):
            pass

        self.f.write(character)
        sleep(0.001*self.delay)

    def send(self, dat, print_count=False):
        i=0
        for d in dat:
            if print_count:
                print("%04X" % (i+1),end="",flush=True) # length = i+1
            dat=bytes([d])
            #self.puts(chr(d)) # python2
            self.puts(dat) # python3
            i+=1
            if print_count:
                print("\b\b\b\b",end="",flush=True)
#        if print_count:
#            print()

    def close(self):
        self.f.flush()
        self.f.close()

def compress(dat):
    ans=[]
    zero_mode=0
    zero_count=0
    for d in dat:
        if d==0 and zero_mode==0:
            zero_mode=1
            zero_count=1
            ans.append(0)
        elif d==0 and zero_mode==1 and zero_count<255:
            zero_count+=1
        elif d==0 and zero_mode==1 and zero_count>254:
            ans.append(zero_count)
            zero_mode=1
            zero_count=1
            ans.append(0)

        elif zero_mode==1 and d!=0: # ０終わり
            ans.append(zero_count)
            ans.append(d)
            zero_count=0
            zero_mode=0
        else:
            ans.append(d)
    if zero_mode==1:
        ans.append(zero_count)
    return ans

def load_file(filename):
    img=cv2.imread(filename)
    img=img.astype(np.uint8)
    if type(img)==type(None):
        return None

    sizex=144
    sizey=48

    dat=[]
    for yi in range(sizey//8):
        y=yi*8
        for x in range(sizex):
            d=0
            for yl in range(8):
                if img[y+yl,x,0]>0:
                    d|=(1<<yl)
            dat.append(d)
    return dat


def make_dummy_data(d):
    dat=[]
    for i in range(144*6):
        dat.append(d)
    return compress(dat)

def int2byte(dat):
    return [(dat>>8)&0xff, dat&0xff]

def make_param(bank, start_address, dat):
    l=len(dat)
    ans = [bank]+int2byte(start_address) #+int2byte(l)
    return ans

if __name__ == '__main__':
    device='/dev/cu.usbserial-A62WWHTM'
    delay = 0 #[msec/char]

#----------------------------------------
    root_path="images/spaceship_1bit/"
    file_reg=r"%04d.png"
    start_frame=0
    end_frame=239
#----------------------------------------

    USE_UART=True
#    USE_UART=False # for test

    if USE_UART:
        s=UART(device, delay)

    internal_ram_start_address = 0x2000
    internal_ram_end_address   = 0x75ff

    external_ram_start_address = 0x8000
    external_ram_end_address   = 0xbfff

    bank=0
    start_address=external_ram_start_address

    dats = []

    print("creating data..please wait")
    for frame_index in range(start_frame, end_frame+1):
        print("\rloading frame: %04d"% frame_index, end="", flush=True)
        filename=root_path+file_reg%(frame_index)
        dat=load_file(filename)
        dat=compress(dat)
        length=len(dat)

        if (start_address+length>external_ram_end_address):
            bank+=1
            start_address=external_ram_start_address
            if(bank>3):
                bank=0x10
                start_address=internal_ram_start_address
        if(bank==0x10 and (start_address+length)>internal_ram_end_address):
            print("\nMemory size exceeded")
            end_frame=frame_index-1
            break
#        dat=make_dummy_data(frame_index+1)
        dat_param = make_param(bank,start_address,dat)
        dat = dat_param + dat

        dats.append(dat)
        start_address+=length

    print("\ndone. start pocket-computer now")

    for frame_index in range(start_frame, end_frame+1):
        dat=dats[frame_index]
        bank=dat[0]
        start_address=(dat[1]&0xff)*256+dat[2]
        length=len(dat)-3
        print("frame %d: "%frame_index, end="", flush=True)

        if USE_UART:
            while(s.gets()!=0x01):
                pass
            s.set_delay(0)
            s.send(dat+[0,0,0], print_count=True)

        print("\tBANK:%02X ADR:0x%04X LEN:0x%04X"%(bank,start_address,length), end="", flush=True)

        print("")

    if USE_UART:
        while(s.gets()!=0x01):
            pass
        s.set_delay(0)
        s.send([0xff,0xff,0xff,0x00,0x00,0x00]) # end signal

        s.close()
    print("finished")
