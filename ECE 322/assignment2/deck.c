#include "deck.h"

int shuffle(void){
	/* Initialize variables*/	
	char ranks[13] = {'2','3','4','5','6','7','8','9','T','J','Q','K','A'};
	char suits[4] = {'C','D','H','S'};
	int num;
	int i=0;
	char inrank;
	char insuit;
	int j;
	if (deck_instance.top_card !=0){
		for(int k = deck_instance.top_card;k<52;k++){
			free(deck_instance.list[k]);
		}
		deck_instance.top_card=0;
	}
	struct card* temp;
	/*Build deck randomly, making sure to not introduce duplicates*/
	while(i<52){
		num=rand() % 13;
		inrank = ranks[num];
		insuit = suits[rand()%4];
		if (i != 0){
			for (j=0;j<i;j++){
				if (deck_instance.list[j]->suit == insuit && deck_instance.list[j]->rank == inrank){
					break; /*Pick new combination if it is already present in the deck*/
				}
			}
			if (i == j){ /*Add new card to deck and increment the placement index*/ 
				temp = (struct card*)malloc(sizeof(struct card*));	
				temp->suit=insuit;
				temp->rank=inrank;
				deck_instance.list[i]=temp;
				i++;	
			}
		}
		else{ /*Skip for loop if it is the first position in the array*/
			temp = (struct card*)malloc(sizeof(struct card*));			
			temp->suit=insuit;
			temp->rank=inrank;			
			deck_instance.list[i]=temp;
			i++;
		}
	}
	return 0;
}

int deal_player_cards(struct player* target){
	/*Initialize Variables*/
	int num=deck_instance.top_card;

	if (num<45){ /*Check to see if there are enough cards in the deck to deal*/
		for (int i=num;i<num+7;i++){
			if (deck_instance.list[i] == NULL){ /*Exits if there is no pointer*/
				return 1;			
			}	
			
			add_card(target,deck_instance.list[i]);
			deck_instance.list[i]=NULL;
		}
		deck_instance.top_card = deck_instance.top_card + 7;
		return 0;
	}
	else{
		return 1;
	}
}

struct card* next_card(){
	struct card* temp = deck_instance.list[deck_instance.top_card];
	deck_instance.list[deck_instance.top_card] = NULL;
	deck_instance.top_card++;
	return temp;
}

size_t deck_size(){
	return 52 - deck_instance.top_card;

}
