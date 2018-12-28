#include <stdio.h>
#include <stdint.h>
#include <conio.h>

#define MAX_FRAMES 240

#include "uart.h"      // serial rx library
#include "extrom.h"    // external rom r/w library
#include "display.h"   // decompress and display library

static struct extrom_pointer compressed_frames[MAX_FRAMES];
static uint8_t buffer[900];     // compressed data   144x48/8 + header 3 + footer 3
static uint8_t frame_data[894]; // decompressed data 144x48/8

uint16_t load_frame(){
    uint8_t bank;
    uint16_t start_address,length;
    uint16_t frame_index=0;

    clrscr(); // clear screen
    start_uart();

    printf("push 1 to start\n");
      while (getk() != '1') {};
    clrscr(); // clear screen

    while(1){
        printf("frm %04d:",frame_index);

        // recieve frame parameter & data
        tx_uart(0x01);
        length= receive_data(buffer);

        length-=3;
        bank = buffer[0];
        start_address = (buffer[1]<<8) | buffer[2];
        if (bank==0xFF){printf("\n");break;}

        // save buffer to extrom
        if (bank<4){
            write_ext_rom((&buffer+3), length,start_address,bank);
        }else if (bank==0x10){
            write_int_ram((&buffer+3), length,start_address);
        }

        // save to extrom pointer
        compressed_frames[frame_index].bank= bank;
        compressed_frames[frame_index].start_address= start_address;
        compressed_frames[frame_index].length= length;

        printf("%02X %04X %04X\n",bank,start_address,length);
        if(frame_index%5==4){clrscr();}
        frame_index++;

        if (frame_index>MAX_FRAMES){
            break;
        }
    }
    return frame_index;

}

void play_movie(uint16_t max_frame){

    uint8_t bank;
    uint16_t start_address,length;
    uint16_t frame_index=0;

    clrscr();

    for(frame_index=0;frame_index<max_frame;frame_index++){

        bank = compressed_frames[frame_index].bank;
        start_address = compressed_frames[frame_index].start_address;
        length = compressed_frames[frame_index].length;

        // 読み出しと伸長とLCD書き出しを同時にやればbufferも減らせるし早いのでいずれ合体したい
        if (bank<4){
            read_ext_rom(buffer, length, start_address, bank);
        }else if(bank==0x10){
            read_int_ram(buffer, length, start_address);
        }
        decompress(buffer, length, frame_data);
        my_blit(frame_data);

    }


}


void main()
{
    uint16_t max_frame;

    max_frame=load_frame();

    while(1){
        clrscr();
        printf("push 5 to go");
        while (getk() != '5') {};

        play_movie(max_frame);

        while (1){
            uint8_t key=getk();
            if(key == '0') { // play again
                break;
            }else if(key == '9') { // quit
                stop_uart();
                return;
            }
        }
    }

}
