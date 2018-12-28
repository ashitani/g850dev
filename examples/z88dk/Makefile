TARGETS = hello.ihx sin.ihx hello2.ihx inline1.ihx inline2.ihx

CCFLAGS = +g800 -lm -create-app -clib=g850b # 6 lines/V
CC = zcc

ASMFLAGS = +g800 --no-crt -create-app -Cz"--ihex --org=0x100"


all: $(TARGETS)

sin.ihx: sin.c
	$(CC) $(CCFLAGS) -lm -o$*.ihx $<

.SUFFIXES: .c .ihx .lib .asm


.c.ihx:
	$(CC) $(CCFLAGS) -o$*.ihx $<
.c.lib:
	$(CC) +g800 -x -o$* $<
.asm.ihx:
	$(CC) $(ASMFLAGS) -o$*.ihx $<

.PHONY: clean
clean:
	$(RM) $(TARGETS) *.o *.def *.bin *.rom *.lst *.lib g800user.txt
