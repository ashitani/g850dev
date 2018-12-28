#!/usr/bin/env python
#coding: utf-8

# 20kHz sampling data
SAMPLE_RATE=20e3

# https://www.akiyan.com/pc-g850_technical_data#basic_middle_code
basic_table=[
"","","","","","","","","","","","","","","","MON",
"RUN","NEW","CONT","PASS","LIST","LLIST","CLOAD","RENUM","LOAD","","","DELETE","FILES","","","LCOPY",
"CSAVE","OPEN","CLOSE","SAVE","","RANDOMIZE","DEGREE","RADIAN","GRAD","BEEP","WAIT","GOTO","TRON","TROFF","CLEAR","USING",
"DIM","CALL","POKE","GPRINT","PSET","PRESET","","","","","ERASE","LFILES","KILL","","","",
"","","","","","OUT","","","PIOSET","POIPUT","SPOUT","SPRINT","HDCOPY","ENDIF", "REPEAT","UNTIL",
"CLS","LOCATE","TO","STEP","THEN","ON","IF","FOR","LET","REM","END","NEXT","STOP","READ","DATA","",
"PRINT","INPUT","GOSUB","LNINPUT","LPRINT","RETURN","RESTORE","","GCURSOR","LINE","","","","","","CIRCLE",
"PAINT","OUTPUT","APPEND","AS","","","ELSE","","","","WHILE","WEND","SWITCH","CASE","DEFAULT","ENDSWITCH",
"MDF","REC","POL","","","","TEN","RCP","SQU","CUR","HSN","HCS", "HTN", "AHS", "AHC", "AHT",
"ACT","LN" , "LOG", "EXP", "SQR", "SIN", "COS", "TAN", "INT", "ABS", "SGN", "DEG", "DMS", "ASN", "ACS", "ATN",
"RND", "AND", "OR",  "NOT", "PEEK",    "XOR", "INP","","PIOGET","","","","","POINT","PI","FRE",
"EOF","","LOF", "","","","NCR","NPR","","","","","","","","CUB",
"","","","","","","MOD","FIX","","","","","","","","",
"ASC","VAL","LEN","VDEG","","","","","","","","","","","","",
"","","","","","","","","","INKEY$","MID$","LEFT$","RIGHT$","","","",
"CHR$","STR$","HEX$","DMS$","","","","","","","","","","","",""
]

TYPE_BIN=1
TYPE_BASIC=2

def read_data(filename):
    f=open(filename).readlines()

    data=[]
    for l in f:
        dat=l[:-1].split(":")[1::]
        if dat!=[]:
            d=dat[0].split(" ")
            for x in d:
                for c in x:
                   data.append(int(c))
    return data




def split_pwm_data(data, printing=False):
    '''
    PWM群を切り出す
    '''

    length=0
    old_x=data[0]
    old_edge=-1
    split_data=[]
    pwm_data=[]

    ans=[]

    for x in data:
        if old_x==0 and x==1:
            #rising
            if old_edge==0 and length>10:
                if len(pwm_data)>1:
                    if printing:
                        print("PWM Data: ", len(pwm_data)) 
                    ans.append(pwm_data)
                if printing:
                    print("L %5d [msec]"% (length*1000/SAMPLE_RATE )) 
                pwm_data=[]
#            else:
                # if len(split_data)<5:
                #     pwm_data.append(0)
                # else:
                #     pwm_data.append(1)
            old_edge=1
            length=0
            split_data=[]
        if old_x==1 and x==0:
            #falling
            if old_edge==1 and length>10:
                if len(pwm_data)>1:
                    ans.append(pwm_data)
                    if printing:
                        print("PWM Data: ", len(pwm_data)) 
                if printing:
                    print("H %5d [msec]"% (length*1000/SAMPLE_RATE)) 
            else:
                if len(split_data)<5:
                    pwm_data.append(0)
                else:
                    pwm_data.append(1)
            old_edge=0
            length=0
            split_data=[]
        split_data.append(x)
        old_x=x
        length+=1
    return ans

def chop_long_header(data, lh,printing=False):
    ans=[]
    odd=1-lh
    i=0
    for x in data:
        if x==odd:
            if printing:
                print("Chopped ",i, " data")  
            return data[i:]
        i+=1

def get_data(data,printing=False,dlen=3):
    '''
        PWMデータから生データを切り出す
    '''

    # 長い01を取り除く
    # 長い0,長い1,長い0, データ、と続くのでdlen=3
    # 前半か後半を判定したい場合はここで1/0の長さを見ればよい

    data_num=len(data)
    lh=0
    for i in range(dlen):
        data=chop_long_header(data, lh,printing)
        lh=1-lh

    # 頭と最後の1を取り除く
    data = data[1:len(data)-1]

    data_num = int(len(data)/9)
    ans=[]
    for i in range(data_num):
        d=(data[(i*9+1):(i*9+9)])
        ds="0b"+"".join(["%d"%i for i in d])
        ans.append(eval(ds))
    return ans

def decode_basic(decoded_data):

    reserved=False
    ln=False
    txt=""
    while(True):
        x=decoded_data.pop(0)

        if x==0xfe: #reserved
            code=decoded_data.pop(0)
            txt+=basic_table[code]+" "
        elif x==0x1f: #line number
            num=decoded_data.pop(0)<<8
            num+=decoded_data.pop(0)
            txt+="%d" % num
        else:
            txt+=chr(x)
        if(len(decoded_data)==0):
            break
    return txt

def dump_data(data):
    # if(len(data)%16!=0):
    #     data+=["-"]*(16-(len(data)%16))
    address=0
    print()
    for i in range(int(len(data)//16+1)):
        d=data[i*16:(i+1)*16]
        print("%04X: "%address, end="")
        for x in d:
            print("%02X "%x,end="")
        address+=16
        print()
    print()

def dump_basic(data):
    txt=""
    #skip header(TBD)
    dat=data[12:]
    while(True):
        line_num = (dat.pop(0)<<8)
        line_num+=dat.pop(0)
        byte_num = dat.pop(0)
        codes=[]
        for i in range(byte_num):
            codes.append(dat.pop(0))
        txt+="%d:%s\n" % (line_num, decode_basic(codes))
        if(len(dat)<=2):
            break
    return txt

def main():
    from sys import argv
    if len(argv)!=2:
        print("Usage python decode.py [filename]")
        exit()

    printing=True

    data = read_data(argv[1])
    ans = split_pwm_data(data, printing)

    decoded_data = get_data(ans[0],printing) #前半
    #dump_data(decoded_data)
    data_type=decoded_data[0]

    decoded_data = get_data(ans[1],printing) #後半
    dump_data(decoded_data)

    if data_type==TYPE_BASIC:
        txt=dump_basic(decoded_data)
        print()
        print(txt)
    else:
        dump_data(decoded_data[:-2])# パリティを除く

if __name__ == '__main__':
    main()