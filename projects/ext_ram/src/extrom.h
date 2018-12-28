#ifndef __EXTROM_H
#define __EXTROM_H

void read_ext_rom(uint8_t *data, uint16_t length, uint16_t address, uint8_t bank);
void write_ext_rom(uint8_t *data, uint16_t length, uint16_t address, uint8_t bank);

void read_int_ram(uint8_t *data, uint16_t length, uint16_t address);
void write_int_ram(uint8_t *data, uint16_t length, uint16_t address);

#endif