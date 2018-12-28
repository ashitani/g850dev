#include <stdio.h>
#include <conio.h>
#include <stdint.h>
#include "display.h"

void my_blit(uint8_t* dat){
#asm
    ld ix,2
    add ix, sp

    ld h, (ix+1)  ;x_H
    ld l, (ix)    ;x_L

    ld b,  144 ;  // x length
    ld de, 0x00 ; // cursor position

loop:
    call write
    inc hl ; // IOCS doesn't incriment HL for the last byte writing?
    inc d;   // increment Y cursor
    ld a,d
    cp 6
    jp nz,loop
    ret

write:
    push bc
    push de
    call 0xbfd0
    pop de
    pop bc
    ret
#endasm
}


void decompress(uint8_t *data, uint16_t length, uint8_t *frame_data){
    uint8_t k,d=0;
    uint16_t last,adr,dat_index=0;

    adr=0;
    last = adr + length;

    while(adr<last){
        d=data[adr++];
        if(d==0){
            d=data[adr++];
            for(k=0; k< d;k++){
                frame_data[dat_index++]=0;
            };
        }else{
            frame_data[dat_index++]=d;
        }
    }
}
