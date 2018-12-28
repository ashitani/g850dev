#ifndef __UART_H
#define __UART_H

void start_uart();
void stop_uart();
uint8_t rx_uart();
void tx_uart(uint8_t);
uint16_t receive_data(uint8_t *);
uint16_t receive_fixed_data(uint8_t *, uint16_t );

#endif