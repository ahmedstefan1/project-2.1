#include <avr/io.h>
#include <stdint.h>
#include <stdio.h>
#include <avr/sfr_defs.h>
#include "UART.h"

#define F_CPU 16E6
#include <util/delay.h>

#define UBBRVAL 51

#define HIGH 0x1
#define LOW  0x0

int ADCsingleREAD(uint8_t ADCport)
{
	int ADCvalue;

	ADMUX = ADCport;        // use #1 ADC
	ADMUX |= (1 << REFS0);   // use AVcc as the reference
	ADMUX &= ~(1 << ADLAR);  // clear for 10 bit resolution

	ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);

	ADCSRA |= (1 << ADEN);    // Enable the ADC
	ADCSRA |= (1 << ADSC);    // Start the ADC conversion

	while(ADCSRA & (1 << ADSC)); // waits for the ADC to finish

	ADCvalue = ADCL;
	ADCvalue = (ADCH << 8) + ADCvalue; // ADCH is read so ADC can be updated again

	return ADCvalue;
}


uint8_t getadc()
{
	double ADCvalue = 0;
	int degrees = 0;
	while (1) {
		// reads temperature
		ADCvalue = ADCsingleREAD(1);
		// rekent om naar graden C
		degrees = ((ADCvalue / 1024 * 5)-0.5)*100;
		// zet het om naar een int
		degrees = (int) degrees;

		transmit(degrees);
		// reads light sensor light sensor doesnt need conversion
		transmit(ADCsingleREAD(0));
		_delay_ms(1000);

	}
}



int main()
{
	// initialiseert uart
	uart_init();
	while(1){
		_delay_ms(1000);
		// haalt de waarde van de analoge sensoren op
		getadc();

	}
	return(0);
}

