/*
Source Code File: blink.c
Name: John Boesen
Date Due: 3/3/2022
Description: This will blink 2 LEDs in different patterns based on which button is pressed
*/
/* 
Inputs: D3-5 
Output: D6, D7
If Button1 == 5V && Button2 != 5V && Button3 != 5v;
    Then 5 Hz through D6
If Button2 == 5v && Button1 != 5V && BUtton3 != 5V;
    Then 5 Hz through D7
if Button3 == 5V && Button2 != 5V && Button1 != 5V;
    Then 5 Hz through D6 and D7
  */
#include <stdio.h>
#include <util/delay.h>
#include <avr/io.h>




int main(void){
    DDRD = 1<<DDD6|1<<DDD7;
    PORTD = 1<<PORTD3|1<<PORTD4|1<<PORTD5;

    while(1){
        //Look for input from the first button
        if ((PIND & (1<<PIND3)) == 0 && (PIND & (1<<PIND4)) !=0 && (PIND & (1<<PIND5))!=0){
            PORTD |= (1<<PORTD6);
            _delay_ms(100);
            PORTD &= ~(1<<PORTD6);
            _delay_ms(100);
        }

        //Look for input from the second button
        if ((PIND & (1<<PIND4)) == 0 && (PIND & (1<<PIND3)) !=0 && (PIND & (1<<PIND5))!=0){
            PORTD |= (1<<PORTD7);
            _delay_ms(100);
            PORTD &= ~(1<<PORTD7);
            _delay_ms(100);
        } 

        //Look for input from the thrid button
        if ((PIND & (1<<PIND5)) == 0 && (PIND & (1<<PIND3))!=0 && (PIND &(1<<PIND4))!=0){
            PORTD |= (11<<PORTD6);
            _delay_ms(100);
            PORTD &= ~(11<<PORTD6);
            _delay_ms(100);
        }
        else{
            PORTD &= ~(1<<PORTD6);
            PORTD &= ~(1<<PORTD7);
        }
    }
    return 0;
}