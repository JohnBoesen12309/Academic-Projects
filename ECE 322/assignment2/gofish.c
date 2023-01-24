#include <stdio.h>
#include <time.h>
#include "deck.h"

int main(int args, char* argv[]) 
{
	/*Initialize Variables*/
	int turn = 0;
	char check_book;
	int check_game = 0;
	char rank;
	int a = 0;
	int pbooks;
	int cbooks;
	char exit;
	char garb;
	struct card* temp_card;
	srand(time(NULL));
	deck_instance.top_card = 0;
	
	while (1){ /*Continue running the application until user exit*/
		reset_player(&user);
		reset_player(&computer);		
		printf("Shuffling deck...\n");
		shuffle();
		deal_player_cards(&user);
		deal_player_cards(&computer);
		turn = 0;
		check_game = game_over(&user);
		a=0;
		check_game = 0;

		while(check_game == 0){ /*Run game until one player wins*/
			printf("Player 1's Hand - ");		
			printHand(&user);
			printf("Player 1's Book - ");
			printBook(&user);
			printf("Player 2's Book - ");
			printBook(&computer);			
	
			if (turn % 2 == 0){ /*Set of outputs for User turn*/
				printf("Player 1's turn, enter a Rank: ");
				rank = user_play(&user);			
				printf("    -Player 2 has ");	
				a = search_hand(&computer,rank);
				if (a == 0){ /*Draw a card if opponent doesn't have any of rank in hand*/
					printf("no %c's \n",rank);
					printf("    -Go Fish, Player 1 draws a card\n");
					temp_card = next_card();
					add_card(&user,temp_card);
					check_book = check_add_book(&user);
				}					
				else{ /*Transfer all instances of cards containing rank to opponent*/
					printf("    -Player 1 has ");					
					search_hand(&user, rank);					
					transfer_cards(&computer,&user,rank);
					check_book = check_add_book(&user);
				}
				if (check_book != 'Z'){ /*Add book to User and check to see if they win*/
					printf("    -Player 1 books %c \n",check_book);
					printf("    -Player 1 gets another turn\n");
					check_game = game_over(&user);
					pbooks++;	
				}
				else{
					printf("    -Player 2's turn\n");
					turn++;
				}	
			}
			else{ /*Set of outputs for computer turn*/
				printf("Player 2's turn, enter a Rank: ");
				rank = computer_play(&computer);
				printf("%c \n", rank);
				printf("    -Player 1 has ");
				a = search_hand(&user,rank);
				if (a == 0){ /*Draw a card if User's hand doesn't contain cards with rank*/
					printf("no %c's \n",rank);
					printf("    -Go Fish, Player 2 draws a card\n");
					temp_card = next_card();
					add_card(&computer,temp_card);
					check_book = check_add_book(&computer);
				}
				else{ /*Transfer user's cards containing rank to computer's hand*/
					printf("    -Player 2 has ");
					search_hand(&computer,rank);
					transfer_cards(&user,&computer,rank);
					check_book = check_add_book(&computer);
				}
				if (check_book != 'Z'){ /*Add book to computer and check for win state*/
					printf("    -Player 2 books %c \n",rank);
					printf("    -Player 2 gets another turn\n");
					check_game = game_over(&computer);
					cbooks++;
				}
				else{
					printf("    -Player 1's turn\n");
					turn++;
				}
			}			
		}
		if (turn % 2 == 0){ /*Print win messages*/		
			printf("Player 1 wins! %i - %i",pbooks,cbooks);
		}
		else{
			printf("Player 2 wins! %i - %i",pbooks,cbooks);
		}
		printf("Do you want to play again [Y/N]: ");
		exit = getc(stdin);
		while(!(exit == 'N' || exit == 'Y')){ /*Determine if User wishes to exit application*/
			printf("Invalid Input\n");
			printf("Do you want to play again [Y/N]: ");
			exit = getc(stdin);
			garb = getc(stdin);
		}
		if (exit == 'N'){
			printf("Exiting.");			
			break;
		}
	}
}
