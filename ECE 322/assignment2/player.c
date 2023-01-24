#include "player.h"
#include <stdio.h>
#include <time.h>

int add_card(struct player* target, struct card* new_card){
	/*Initialize Variables*/
	struct hand* temp;
	temp = (struct hand*)malloc(sizeof(struct hand*));
	
	if (temp == NULL) {return 1;} /*Exits if malloc breaks*/
	
	temp->top = *new_card; /*Adds new card to the top of the hand*/
	temp->next = target->card_list;
	target->card_list = temp;
	target->hand_size++;
	return 0;

}

int remove_card(struct player* target, struct card* old_card){
	/*Initialize Variables*/	
	struct hand* iterator = target->card_list;
	struct hand* previous = NULL;
	
	if (iterator == NULL) { return 0; } /*Exit if list empty*/

	while (!(iterator->top.suit == old_card->suit && iterator->top.rank == old_card->rank)){ /*Iterates until exact card is found*/
		previous = iterator;
		iterator = iterator->next;
		if (iterator == NULL) /*Exits if it hits the end of the list*/
			return 0;
	}

	if (previous != NULL){
		previous->next = iterator->next;
	}
	else {
		target->card_list = iterator->next;
	}
	
	free(old_card);
	target->hand_size=target->hand_size - 1;
	return 1;	
}

char check_add_book(struct player* target){
	/*Initialize Variables*/	
	char inrank = (char) (target->card_list->top.rank);
	int sum = search(target,inrank);
	int i;
	
	if (sum == 4){ /*Check to see if the search found 4 instances of a rank*/
		struct hand* temp = target->card_list;
		while (sum>0){
			if (temp->top.rank == inrank){					
				remove_card(target,&(temp->top));
				sum--;
			}
			temp = temp->next;
		}
		for (i = 0;i<7;i++){ /*Find an open position in the book array*/
			if (target->book[i] == 'Z'){
				target->book[i] = inrank;
				break;
			}
		}
		return inrank;
	}
	else{
		return 'Z';
	}
}

int search(struct player* target, char rank){
	/*Initialize Variables*/	
	struct hand* temp;
	int i = 1;
	int sum = 0;
	temp = target->card_list;
	
	while (temp != NULL){ /*Iterate through the card_list to find amount of instances of a rank*/
		if (temp->next == target->card_list){
			temp->next = NULL;
		}
		if (temp->top.rank == rank){
			sum++;
		}		
		temp = temp->next;
		i++;
	}
	return sum;
}

int transfer_cards(struct player* src, struct player* dest, char rank){
	/*Initialize Variables*/	
	struct hand* temp;
	int i = 0;
	temp = src->card_list;
	
	while (temp != NULL){ /*Find cards that have a matching rank and add them to dest*/
		if (temp->top.rank == rank){						
			add_card(dest,&(temp->top));
			i++;	
		}
		temp = temp->next;
	}
	temp = src->card_list;
	while (i>0){ /*Remove all cards with the matching rank from the src hand*/		
		if (temp->top.rank == rank){					
			remove_card(src,&(temp->top));
			i--;
		}
		temp = temp->next;
	}
	return i;
}

int game_over(struct player* target){
	/*Initialize Variable*/
	int check = 0;
	
	for (int i=0;i<7;i++){ /*Iterate over the book array to see if all of the positions are filled*/
		if (target->book[i] != 'Z'){
			check++;
		}
	}
	if (check >= 7){
		return 1;
	}
	else{
		return 0;
	}
}

int reset_player(struct player* target){
	/*Initialize Variables*/
	int check = 1;

	while (check == 1){/*Remove all cards in hand*/
		struct card* rem = &(target->card_list->top);
		check = remove_card(target, rem);
	}
	for (int i=0;i<7;i++){ /*Reset book array*/
		target->book[i]='Z';
	target->hand_size = 0;
	}
	return 0;
}

char computer_play(struct player* target){
	/*Initalize Variables*/
	int num = rand() % 13;
	char ranks[13] = {'2','3','4','5','6','7','8','9','1','J','Q','K','A'};
	char inrank = ranks[num];
	int check = search(target,inrank);

	while (1){ /*Randomly pick a card from computer's hand*/
		if (check == 0){
			num=rand() % 13;
			inrank = ranks[num];
			check = search(target,inrank);
		}
		else{
			return inrank;
		}
	}
	
}

char user_play(struct player* target){
	/*Initialize Variables*/
	char input='\n';
	int check;

	while (1){ /*Read User Input and Check to see if it is vaild*/
		while(input == '\n'){		
			input=getchar();
		}
		check=search(target,input);	
		if (check == 0){
			printf("\nError-must have at least one card from rank to play\n");
			printf("Player 1's turn, enter a Rank: ");
			input='\n';
		}
		else{
			return input;
		}
	}
}

void printHand (struct player* target){ /*Print the contents of target hand to stout*/
	if (target->hand_size == 0){
		deal_player_cards(target);
	}	
	struct hand* temp;
	temp = target->card_list;
	while (temp != NULL){
		
		printf("%c%c ",temp->top.rank, temp->top.suit);
		temp=temp->next;
		
	}
	printf("\n");
}

void printBook (struct player* target){ /*Print the contents of target book array to stout*/
	for (int i=0;i<7;i++){
		if (target->book[i] != 'Z'){					
			printf("%c ",target->book[i]);				
		}
	}
	printf("\n");
}

int search_hand (struct player* target, char rank){ /*Search target hand for all instances containing rank and print to stout*/
	struct hand* temp;
	temp = target->card_list;
	int hasCard = 0; 
	while (temp != NULL){
		if (temp->top.rank == rank){
			printf("%c%c ",rank,temp->top.suit);
			hasCard = 1;
		}
		temp=temp->next;
	}
	if (hasCard){
		printf("\n");
	}
	return hasCard;
}

