#include <avr/io.h>
#include <util/delay.h>
#define DELAY 1000

int main(void){
     DDRD = 1<<DDD6;
    PORTD = 1<<PORTD3|1<<PORTD4;

    while(1){
        //Look for input from the first button
        if ((PIND & (1<<PIND3)) == 0 && (PIND & (1<<PIND4)) !=0){
            PORTD |= (1<<PORTD6);
            _delay_ms(0.5);
            PORTD &= ~(1<<PORTD6);
            _delay_ms(4.5);
        }

        //Look for input from the second button
        if ((PIND & (1<<PIND4)) == 0 && (PIND & (1<<PIND3)) !=0){
            PORTD |= (1<<PORTD6);
            _delay_ms(2);
            PORTD &= ~(1<<PORTD6);
            _delay_ms(3);
        } 

        //Look for input from the thrid button
        if ((PIND & (1<<PIND3))==0 && (PIND & (1<<PIND4))==0){
            PORTD |= (11<<PORTD6);
            _delay_ms(4.5);
            PORTD &= ~(11<<PORTD6);
            _delay_ms(0.5);
        }
        else{
            PORTD &= ~(1<<PORTD6);
        }
    }
    return 0;
}