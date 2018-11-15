#define F_CPU 16E6

#include <stdio.h>
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "UART.h"
#include "AVR_TTC_scheduler.h"


#define HIGH 0x1
#define LOW  0x0

// initialiseert de ultrasoon poorten
void init() {
	//zet poort B en D op outut
	DDRD = 0xff;
	DDRB = 0xFF;
	// zet Pin PB0 als input om de echo te lezen
	DDRB &= ~(1<<DDB0);

	PORTB |= (1<<PB0);
	PORTB &= ~(1<<PB1);

	// activate timer 1
	PRR &= ~(1<<PRTIM1);
	// Initial timer value
	TCNT1 = 0;
	// prescaler of 8
	TCCR1B |= (1<<CS11);
	// First capture on rising edge
	TCCR1B |= (1<<ICES1);

	PCICR = (1<<PCIE0);	// Enable PCINT[7:0] we use pin PB0 which is PCINT0
	PCMSK0 = (1<<PCINT0);// set PB0 as intterupt port
	sei();				// Enable Interrupts
}


int ADCsingleREAD(uint8_t ADCport)
{
	// use ADC port
	ADMUX = ADCport;
	// ADC instellingen
	ADMUX |= (1 << REFS0);
	ADMUX &= ~(1 << ADLAR);
	ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
	// Enable ADC
	ADCSRA |= (1 << ADEN);
	// Start ADC conversion
	ADCSRA |= (1 << ADSC);
	// wait for ADC to finish
	while(ADCSRA & (1 << ADSC));
	int ADCwaarde;
	ADCwaarde = ADCL;
	ADCwaarde = (ADCH << 8) + ADCwaarde;
	//return adc waarde
	return ADCwaarde;
}


void encode(int sensor, int data){
	// maakt variabelen aan
	unsigned char value1;
	unsigned char value2;
	unsigned char value3;

	unsigned char first_hex;
	unsigned char second_hex;
	unsigned char xor;

	unsigned char temp;

	// zet de eerste 4 bits voor eth eerste hex getal op hun plek
	first_hex = (sensor & 0x0F)<<4;
	temp = (data & 0xF0)>>4;
	// naakt eerste hex waarde
	first_hex = first_hex | temp;
	// zet de eerste 4 bits op hun plek voor het 2de hex getal
	second_hex = (data & 0x0F)<<4;

	// wat bit shiften is nodig voor dat we het Xorren
	value1 = sensor;
	value2 = (data & 0xF0)>>4;
	value3 = data & 0x0F;

	// berekening voor de check
	xor = value1 ^ value2 ^ value3;

	//maakt de tweede hex waarde
	second_hex  = second_hex | xor;

	// verstuurt het packet
	transmit(first_hex);
	transmit(second_hex);
	transmit(0x0A);
}

void send_burst(){
	// zet de trigger hoog
	PORTB |= (1<<PB1);
	// voor 10uS
	_delay_us(10);
	// doet de trigger uit
	PORTB &= ~(1<<PB1);
	// turn on debugging LED
	PORTB |= (1<<PB3);
}


void getsensors()
{
	double ADCwaarde = 0;
	int degrees = 0;
	while (1) {
		// reads temperature
		ADCwaarde = ADCsingleREAD(1);
		// rekent om naar graden C
		degrees = ((ADCwaarde / 1024 * 5)-0.5)*100;
		// zet het om naar een int
		degrees = (int) degrees;

		// encode data en transmit het naar de comp
		encode(8,degrees);
		// reads light sensor and encodes it and transmits it, light sensor needs no conversion
		encode(4, ADCsingleREAD(0));
		send_burst();
		_delay_ms(1000);
	}
}


int main() {
	// alle inits
	uart_init();
	init();
	SCH_Init_T0();
	unsigned char ultrasoon;
	unsigned char run_sensors;
	//unsigned char delayfunc;
	//unsigned char ontvang;

	//voegt de task voor et uitlezen van de ultrasoon toe
	run_sensors = SCH_Add_Task(getsensors,5,1000);
	//delayfunc = SCH_Add_Task(delay,2,1000);
	//ontvang = SCH_Add_Task(recieve,0,100);
	SCH_Start();
	while (1) {
		SCH_Dispatch_Tasks();
		_delay_ms(1000);
	}
}


ISR(PCINT0_vect) {
	// doet de global interrupts uit
	cli();
	// Checks if echo is high
	if (bit_is_set(PINB,PB0)) {
		// Reset Timer
		TCNT1 = 0;
		// doet de debugging LED aan
		//PORTB |= (1<<PB3);
	} else {
		// Save Timer value
		uint16_t numuS = TCNT1;
		// slaat het register op
		uint8_t oldSREG = SREG;
		double distance;
		// rekent afstand om van het aantal uS naar cm
		distance = numuS/58/2;

		// zet de data om naar een packet en verstuurd die
		encode(2,(int)distance);
		// als de afstand kleiner is dan 10
		if (distance < 10){
			//zet poort 7 aan voor de groene led en verstuurt een packet
			PORTD = 0x80;
			transmit(0x10);
			transmit(0x10);
			transmit(0x0A);
		}
		// als de afstand hoger is dan 40
		else if (distance > 40)
		{
			// zet poort 5 hoog voor de rode led en stuurt een packet
			PORTD = 0x20;
			transmit(0x10);
			transmit(0x32);
			transmit(0x0A);
		}
		else{
			// zet de gele led (6) aan en verstuurt een packet
			PORTD = 0x40;
			transmit(0x10);
			transmit(0x23);
			transmit(0x0A);
		}
		_delay_ms(1000);
		// zet het register terug
		SREG = oldSREG;
		// zet debugging LED uit
		PORTB &= ~(1<<PB3);
		// Enable interrupts
		sei();
	}
}