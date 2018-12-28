#include <stdint.h>

void read_ext_rom(uint8_t *data, uint16_t length, uint16_t address, uint8_t bank){
#asm
ld ix,2
add ix, sp

ld d, (ix+7)  ;data_address_H
ld e, (ix+6)  ;data_address_L
ld b, (ix+5)  ;lendth_H
ld c, (ix+4)  ;length_L
ld h, (ix+3)  ;address_H
ld l, (ix+2)  ;address_L

in a,(0x17)
push af
ld a,0x00
out (0x17),a ; DISABLE INTERURPTS
in a, (0x19)
push af

push de
ld e, (ix)  ; bank
sla e
sla e
sla e
sla e
ld d, 0x40  ; /CEROM2=L,  BANK1=0, BANK0=0
or d
or e
out (0x19),a
pop de

ldir

pop af
out (0x19),a ;RESUME ROM port
pop af
out (0x17),a ; RESUME INTERRUPTS
ret
#endasm
}

void write_ext_rom_(uint8_t *data, uint16_t length, uint16_t address, uint8_t bank){
#asm
    di
    nop
    nop
    nop
    nop
    nop
    nop
    ei
ret
#endasm
}

void write_ext_rom(uint8_t *data, uint16_t length, uint16_t address, uint8_t bank){
#asm

ld ix,2
add ix, sp

ld h, (ix+7)  ;data_address_H
ld l, (ix+6)  ;data_address_L
ld b, (ix+5)  ;lendth_H
ld c, (ix+4)  ;length_L
ld d, (ix+3)  ;address_H
ld e, (ix+2)  ;address_L


in a,(0x17)
push af
ld a,0x00
out (0x17),a ; DISABLE INTERURPTS
in a, (0x19)
push af

push de
ld e, (ix)    ;bank
sla e
sla e
sla e
sla e
ld d, 0x40  ; /CEROM2=L,  BANK1=0, BANK0=0
or d
or e
out (0x19),a
pop de

ldir

pop af
out (0x19),a ;RESUME ROM port
pop af
out (0x17),a ; RESUME INTERRUPTS

ret
#endasm
}


void read_int_ram(uint8_t *data, uint16_t length, uint16_t address){
#asm

ld ix,2
add ix, sp

ld d, (ix+5)  ;data_address_H
ld e, (ix+4)  ;data_address_L
ld b, (ix+3)  ;lendth_H
ld c, (ix+2)  ;length_L
ld h, (ix+1)  ;address_H
ld l, (ix)    ;address_L

ldir
ret
#endasm
}

void write_int_ram(uint8_t *data, uint16_t length, uint16_t address){
#asm

ld ix,2
add ix, sp

ld h, (ix+5)  ;data_address_H
ld l, (ix+4)  ;data_address_L
ld b, (ix+3)  ;lendth_H
ld c, (ix+2)  ;length_L
ld d, (ix+1)  ;address_H
ld e, (ix)    ;address_L

ldir
ret
#endasm
}