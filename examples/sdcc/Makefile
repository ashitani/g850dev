OBJS = test.ihx pntc.ihx

all: mycrt.rel $(OBJS)

.SUFFIXES: .ihx .rel .s .asm

mycrt.rel: mycrt.s
	sdasz80 -o $<


.c.ihx:
	sdcc -mz80 --code-loc 0x100 --no-std-crt0 -Wlmycrt.rel $<

.asm.rel:
	sdasz80 -o $<

.rel.ihx:
	sdldz80 -i $*

.phony: clean

clean:
	rm -f test.asm *.rel *.ihx *.lk *.lst *.map *.noi *.sym 
