TARGETS = main.ihx

CCFLAGS = +g800 -lm -create-app -clib=g850b # 6 lines/V
CC = zcc

all: $(TARGETS)

main.ihx: main.c uart.lib extrom.lib display.lib
	$(CC) $(CCFLAGS) -luart -lextrom -ldisplay -o$*.ihx $<

.SUFFIXES: .c .ihx .lib
.c.ihx:
	$(CC) $(CCFLAGS) -o$*.ihx $<
.c.lib:
	$(CC) +g800 -x -o$* $<

.PHONY: clean
clean:
	$(RM) $(TARGETS) *.o *.def *.bin *.rom *.lst *.lib g800user.txt
