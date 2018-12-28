#ifndef __DISPLAY_H
#define __DISPLAY_H

#include <stdint.h>
struct extrom_pointer
{
    uint8_t  bank;
    uint16_t start_address;
    uint16_t length;
};

void my_blit(uint8_t* dat);
void decompress(uint8_t *data, uint16_t length, uint8_t *frame_data);


#endif