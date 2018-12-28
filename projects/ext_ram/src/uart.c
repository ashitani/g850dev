#include <stdio.h>
#include <stdint.h>
#include <conio.h>

// outp/inp is defined on stdlib.h

void start_uart() __z88dk_fastcall{
    outp(0x60,2    ); // set 11pin to UART mode
    outp(0x74,1    ); // uart clock enable
    outp(0x73,0    ); // uart hw reset
    outp(0x73,1    );
    outp(0x73,0    );
    outp(0x70,0x0d ); // 9600bps intterrupt enable
    outp(0x71,0x4e ); // no parity 8bit
    outp(0x71,0x10 ); // error clear
    outp(0x63,0    ); // flow clear
    outp(0x71,5    ); // r/t enable
    outp(0x63,0x14 ); // flow control
}

void stop_uart() __z88dk_fastcall{
    // clear port
    outp(0x60,0    );
    outp(0x62,0    );
    outp(0x63,0    );
}


// uint8_t rx_uart() __z88dk_fastcall{
//     uint16_t r;
//     uint8_t dat;
//     uint16_t err;

//     err=0;
//     r=0;


//     //wait to receive data. "0" key to break
//     while( ((r&0x02)==0))
//     {
//         //if(getk()=="0"){return 0;}
//         r = inp(0x71); //input check
//         err+=1;
//         if(err==65535){
//             #asm
//             in a,(0x71);
//             ld b,a
//             in a,(0x72);
//             ld c,a
//             in a,(0x63);
//             ld d,a
//             rst 0x30;
//             #endasm
//             return 0x00;
//         };
//     }
//     dat=inp(0x72);
//     return (uint8_t)dat;
// }

void tx_uart(uint8_t dat) __z88dk_fastcall{
    uint16_t r;

    r=0;
    //wait to tx data. "0" key to break
    while( ((r&0x04)==0) && (getk()!='0'))
    {
        r = inp(0x71); //check output buffer
    }
    outp(0x72,dat);
    return;
}


// receive untile 00 00 00 and reply the data length
uint16_t receive_data(uint8_t *received_data) __z88dk_fastcall __naked {
    #asm
    ; HL = received_data address

    ld ix,OLD_A
    ld a,0xff
    ld (IX),a
    ld (IX),a
    ld de,0 ; counter

loop_rx:
    in a,(0x71) ; read status
    and a,0x02
    jp z,loop_rx

    in a,(0x72)
    ld c,a ; original a

    or a,(IX)
    or a,(IX+1)
    jp z,exit_rx  ; exit if a_k ==0 and a_k-1 ==0 and a_l-2 ==0

    ld (hl),c
    inc hl

    ld a,(IX)
    ld (IX+1),a; a_k-2
    ld a,c
    ld (IX),a;  a_k-1
    inc de
    jp loop_rx

exit_rx:
    ex de,hl ; hl=de ( return counter)
    dec hl
    dec hl
    ret

OLD_A:
    defb 0,0
     #endasm
}


// // receive untile 00 00 00 and reply the data length
// uint16_t receive_data_(uint8_t *received_data){
//     uint16_t i=0;
//     while(1){
//         received_data[i]=rx_uart();
//         if(received_data[i]==0 && received_data[i-1]==0 && received_data[i-2]==0){break;}
//  //       if(getk()=="0"){return 0;};
//         i++;
//     }

//     return i-1; // length
// }


// // receive fixed length data
// uint16_t receive_fixed_data(uint8_t *received_data, uint16_t length){
//     uint16_t i;
//     for(i=0;i<length;i++){
//         received_data[i]=rx_uart();
// //        if(getk()=="0"){return 0;};
//     }

//     return i; // length
// }

