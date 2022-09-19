/* 
John Boesen
ECE 231, Fall 2022

Convert base 10 inputs to various bases*/

#include <stdio.h>
#include <string.h>


int dec_to_bin(int);

int main(void){
    int num;
    int base;
    char *  binary[9]; 
    do {
        printf("\nPlease enter number & base separated by a space (enter 0 0 to quit): ");
        scanf("%d %d", &num,&base);
        if (base == 16) { // Convert to base 16
            printf("%d in base %d = %X\n",num,base,num);
        }
        if (base == 10) { // Convert to base 10
            printf("%d in base %d = %d\n",num,base,num);
        }
        if (base == 8) { // Convert to base 8
            printf("%d in base %d = %o\n",num,base,num);
        }
        if (base == 2) { //convert to base 2
            dec_to_bin(num);
        }
        if (base!=2 && base!=8 && base!=10 && base!=16 && base!=0){ // Catches invalid entries
            printf("Please enter a base of either 16, 10, 8, 2");
        }
    } while(num != 0 || base !=0);
    return 0;

}
 int dec_to_bin(int num){
    char ret_str[9]; 
    char strtmp[9];
    int temp;
    int i;
    int len;

    printf("%d in base 2 = ",num);
    
    for (i=0; i<8; i++){ //Convert base 10 int to a str containing binary
        temp = num%2;
        sprintf(strtmp,"%d",temp);
        strcat(ret_str,strtmp);
        num = num/2;
    }
    len = strlen(ret_str);
    for (i=len-1;i>=0; i--){ // Flips the binary str
        printf("%c",ret_str[i]);
    }
    return 0;
}