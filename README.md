# cs5113fa22-project

## Developement Schedule

Nov 3 Complete Protos and Interface Design.

Nov 8 complete implementing the trainer functions.

Nov 13 Complet implementing the pokemon functions.

Nov 17 finish the server functions and submit version 1

Dec 01 make any necessary improvments to the existing system or finish any unfinished tasks from above.

Dec 14 presentation.

## Emoji Chooser

The game board is a 2d array with differen emojis representing differentt trainers and pokemon.
The game board will be initialized with the input(N,P and T) from the user. All the animal and trainer emojis with names will be stored in a text file.
The user input T and P is used to go through the list and select the emojis in random. This initilization will be done by the server. Empty spaces will be 
initialized with zeros.
Use a python script to generate a docker-compse.yml file with N,P and T as user input. N is the size of the board.
P is the number of pokemon and T is the number of trainers. 
The .proto will have the services and messages that need to be passed between the Server, Trainer and Pokemon nodes.


## Description of functions 

captured(Position)
	- Return a boolean value to the pokemon. 0 means that the pokemon is free and can move. 1 means it has 
	been captured by the trainer.

moves() 
	- Keeps track of all the elements(trainers on the board). 

	- Prints the board which is a 2d array to the screen. 

	- Continuously checks every few seconds if the board has changed state and reprints the board if the state is changed.

capture()

	- Returns the position and a boolean value to indicate that it has captured all pokemon in that position.
	- The server verifies this though the captured rpc. 

trainerCheck()

	- Looks at the 2d array and decides the best spot to move to.
	- Relays the move to the server which triggers the moves() function to update the 2d array.
	
reportMove()
	-reports the pokemon or trainer's move to server.

 
Pokedex() 

	- Prints a list of all caputured pokemon with trainer that captured the pokemon and a timestamp. 

trainerPath()

	- Prints the 2d array with numbers in ascending order to show the path take by the trainer. 1 is the start and higher numbers are the next positons previously taken.

pokemonCheck()

	- Checks the board to make a move so that it is not captured.
	- Sends it postion and boolean value to the server. 
	- The boolean value indicates if it was capture or not.
	- 1 implying capture and 0 implying free.
	- Relays the move to the server which triggers the moves() function to update the 2d array.

pokePath()

	- Prints the 2d array with numbers in ascending order to show the path take by the pokemon. 1 is the start and higher numbers are the next positons previously taken.

## function that are services.

	- Using a rpc functions when interaction between server the trainer or pokemon is requires.


- trainerCheck(Position) and pokemonCheck(Position) is used by the trainers and pokemons to check their surrounding spaces.

- captured(Position) is used to tell the pokemon in given position that it has been captured.

- reportMove(Position) is used by the pokemon and the trainer to report their position to the server their position after the move.


## rpc messages

	- cFlag - is a boolean value indicates if a pokemon has been captured.
	- Position - is a pair of int32s that idicate the position of the pokemon or the trainer.
	- Space - is a value of type position.
	- Sapces - is an array of spaces.
	- Valid - is the boolean value given to the pokemon or trainer to validate a move.





