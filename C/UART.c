#include<avr/io.h>
#include<stdlib.h>
#include<avr/sfr_defs.h>
#define F_CPU 16E6
#define UBBRVAL 51

void uart_init(){
	//set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	//disable U2X mode
	UCSR0A=0;
	//enable transmitter
	UCSR0B= _BV(RXEN0) | _BV(TXEN0) | (1<<RXCIE0);
	//set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C=_BV(UCSZ01)|_BV(UCSZ00);
}
void transmit(uint8_t data){
	//wait for an empty transmit buffer
	//UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A,UDRE0);
	//send the data
	UDR0=data;
}
char recieve(void) {
	loop_until_bit_is_set(UCSR0A, RXC0); /* Wait until data exists. */
	return UDR0;
}


