#include<avr/io.h>
#include<stdlib.h>
#include<avr/sfr_defs.h>
#define F_CPU 16E6
#include<util/delay.h>
#include "UART.h"
#include "AVR_TTC_scheduler.h"




int main(void){
	uart_init();
	//SCH_Init_T1();
	//unsigned char Task_x;
	//unsigned char Task_y;
	//Task_x = SCH_Add_Task(task,0,10);
	//Task_y = SCH_Add_Task(task,0,10);
	//SCH_Start();
	//while(1){
	//	SCH_Dispatch_Tasks();
	//}
	_delay_ms(1000);
	while(1){
		// voorbeeld code voor seriele verbinding
		_delay_ms(1000);
		transmit(0x83);
		transmit(0x29);
		transmit(0x0A);
		
		transmit(0x10);
		transmit(0x10);
		transmit(0x0A);
		_delay_ms(1000);
		
		transmit(0x10);
		transmit(0x23);
		transmit(0x0A);
		
		_delay_ms(1000);
		transmit(0x24);
		transmit(0x06);
		transmit(0x0A);
		
		_delay_ms(1000);
		transmit(0x42);
		transmit(0x06);
		transmit(0x0A);
	}
	return(0);
}