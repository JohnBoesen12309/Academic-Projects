/*
Source Code File: HW3_main.c
Name: John Boesen
Date Due: 4/3/2022
Description: This will show the ambient tempreture in both Celsius and Fahrenheit
*/

#include <avr/io.h>
#include <util/delay.h>
#define DELAY 5

int main(void) {
  unsigned char ledDigits[] = {0x7B,0x48,0x67,0x6E,0x5C,0x3E,
    0x3F,0x68,0x7F,0x7C};
  unsigned int i=0;
  double num;
  double temp;
  unsigned char DIG1,DIG2,DIG3;
  unsigned char unit[] = {0x35,0x33};
  int j;
  
  DDRD = 0xFF;
  DDRB = 0xFE;
  PORTB = 0xFE;

 while(1) {
    DDRC = 0x00; //Read the temp off of the sensor (Edited from lecture slide)
    ADMUX = 0xC0;
    ADCSRA = 0x87;
    ADCSRA |= (1<<ADSC);
    while ((ADCSRA & (1<<ADIF)) == 0);
    temp = ADCL | (ADCH << 8);
    
    if ((PINB & (1<<PIND0)) == 0){ // Switch to C if button is pushed
        i=1;
        num = (temp-320)/(9.0/5.0); // Convert F to C
      }
    else{
      i=0;
      num = temp;
    }
    /*if (i == 0){
      num = temp;
    }
    if (i == 1){
       num = (temp-320)/(9.0/5.0);
    }*/

    for (j=0; j<25; j++){ // Sample tempreture every 125 ms (Uses the 4 digit ring counter from lecutre as base)
      PORTD = unit[i]; // Display unit (F or C)
      PORTB =~ (1<<4);
      _delay_ms(DELAY);

      DIG1 = ((int) num/100) % 10; //Display tempreture readout
      PORTD = ledDigits[DIG1];
      PORTB =~ (1<<1);
      _delay_ms(DELAY);

      DIG2 = ((int) num/10) % 10;
      PORTD = ledDigits[DIG2];
      PORTD |= 0x80;
      PORTB =~ (1<<2);
      _delay_ms(DELAY);

      DIG3 = (int) num % 10;
      PORTD = ledDigits[DIG3];
      PORTB =~ (1<<3);
      _delay_ms(DELAY);
    }
  }
}
