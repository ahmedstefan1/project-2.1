/*
 *
 *      Program uses a ATMega328p MCU to query a HC-SR04 ultrasonic module. Then Calculates and displays the distance to a object in cm on the NewHaven display.
 *
 *      The ultrasonic module is triggered every 60 ms by setting pin PC4 (the trigger) high for 10 us. A change in state on pin PC5 (the echo)
 *      causes a interrupt. The interrupt checks if PC5 is high. If it is a timer is started that increments every micro second. Once PC5 triggers a
 *      interrupt again and is low the result is calculated and displayed in centimeters on the NewHaven display. Distance in cm is calculated
 *      by the amount of microseconds PC5 (the echo) is active high divided by 58.
 *
 *      Pin placement of ATMega328p:
 *      Pin PC4				HC-SR04 Trig
 *      Pin PC5				HC-SR04 Echo
 */
#define F_CPU 16E6

#include <stdio.h>
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "UART.h"
#include "AVR_TTC_scheduler.h"

#define UBBRVAL 51

#define HIGH 0x1
#define LOW  0x0


void init() {
	DDRD = 0xff;
	DDRB = 0xFF;
	DDRB &= ~(1<<DDB0);
	// Set Pin PB0 as input to read Echo
	PORTB |= (1<<PB0);
	// Enable pull up on C5
	PORTB &= ~(1<<PB1);
	// put trigger PB1 on low

	PRR &= ~(1<<PRTIM1);
	// To activate timer1 module
	TCNT1 = 0;
	// Initial timer value
	TCCR1B |= (1<<CS11);
	// prescaler of 8
	TCCR1B |= (1<<ICES1);
	// First capture on rising edge

	PCICR = (1<<PCIE0);	// Enable PCINT[7:0] we use pin PB0 which is PCINT0
	PCMSK0 = (1<<PCINT0);// set PB0 as intterupt port
	sei();				// Enable Interrupts
}


int ADCsingleREAD(uint8_t ADCport)
{
	// use ADC port
	ADMUX = ADCport;
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

	unsigned char value1;
	unsigned char value2;
	unsigned char value3;

	unsigned char first_hex;
	unsigned char second_hex;
	unsigned char xor;

	unsigned char temp;

	first_hex = (sensor & 0x0F)<<4;
	temp = (data & 0xF0)>>4;
	first_hex = first_hex | temp;
	second_hex = (data & 0x0F)<<4;

	value1 = sensor;
	value2 = (data & 0xF0)>>4;
	value3 = data & 0x0F;
	xor = value1 ^ value2 ^ value3;

	second_hex  = second_hex | xor;

	transmit(first_hex);
	transmit(second_hex);
	transmit(0x0A);
}


void getadc()
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

		encode(8,degrees);
		// reads light sensor light sensor doesnt need conversion devide by 100 to give percentage
		encode(4, ADCsingleREAD(0));
		_delay_ms(500);
	}
}

void send_burst(){
			PORTB |= (1<<PB1);						// Set trigger on
			_delay_us(10);							// for 10uS
			PORTB &= ~(1<<PB1);						// turn off trigger
}


int main() {
	uart_init();
	init();
	SCH_Init_T0();
	unsigned char ultrasoon;
	unsigned char run_adc;
	unsigned char ontvang;
	ultrasoon = SCH_Add_Task(send_burst,1,100);
	//run_adc = SCH_Add_Task(getadc,5,1000);
	//ontvang = SCH_Add_Task(recieve,0,100);
	SCH_Start();
	while (1) {
		SCH_Dispatch_Tasks();
		//encode(1,0x23);
		_delay_ms(1000);
	}
}


ISR(PCINT0_vect) {
	cli();
	if (bit_is_set(PINB,PB0)) {					// Checks if echo is high
		TCNT1 = 0;								// Reset Timer
		PORTB |= (1<<PB3);
	} else {
		uint16_t numuS = TCNT1;					// Save Timer value
		uint8_t oldSREG = SREG;
		double distance;
		distance = numuS/58/2;

		//
		encode(2,(int)distance);
		if (distance < 10){
			PORTD = 0x80;
			transmit(0x10);
			transmit(0x10);
			transmit(0x0A);
		}
		else if (distance > 40)
		{
			PORTD = 0x20;
			transmit(0x10);
			transmit(0x32);
			transmit(0x0A);
		}
		else{
			PORTD = 0x40;
			transmit(0x10);
			transmit(0x23);
			transmit(0x0A);
		}
		_delay_ms(1000);
		SREG = oldSREG;							// Enable interrupts
		PORTB &= ~(1<<PB3);						// Toggle debugging LED
		sei();
	}
}