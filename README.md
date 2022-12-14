# cs5113fa22-project

## Running the code

	- First run generateContainers.py to create the docker-compose.yml file.

		python3 generateContainers.py --N 20 --P 26 --T 26

	- Then docker-compose up --build to run the game.

# Code Summary

	In this project we use docker, grpc and python to create an asynchronus pokemon game. We will call it pokemon OU.The board is a 2d array of zeros and emojis. 0 indicates that the space is empty and an emoji means that the space is occupied. 

	- The board is a 2d array where each field is either 0 to indicate that it's empty or has an emoji to indicate that it is occupied.
	- board is a global variable that stores the 2d array.
	- The board parameters are stored in a config file so that they can be fetched when necessary.
	- Global variable pokedex is use to track who captured a pokemon.
	- Global variable path_tracker keeps track of the path taken by every piece(pokemon/trainer) on the board.
	- Global variabel capture_locations tracks the name the of pokemon captured and the location it was captured in.

createBoard() - creates a 2d array which is the board and places the pieces on the board randomly. It also initializes the pokedex and path_tracker with just the trainer names as keys and all names as keys for the path tracker. Both dictionaries have values of type list.

printBoard()

	- This function prints the board to the console. I uses a delay of 1 sec to make it easier to keep track of whats happening on the board.

check_surroundings()

	- This fuction returns the coordinates of the eight surrounding spaces of current host.
	- The array is flattened so that it can be sent using RPC.
	- This function also returns the caller's current location(you_are_at).

run_trainer()

	- This is a function that is called asynchronously using async grpc.
	- The trainer only runs when number of pokemons on the board is not zero.
	- Also the trainer must hold the lock to proceed. The lock value must be zero.
	- The number of pokemons is tracked by a global variable num_pokemons.
	- If the there are still pokemons on the board then the trainer connects to the server and asks to see it's surroundings.
	- trainerCheck()
		- The rpc trainerCheck() calls check_surroundings and filters the surrounding spaces further into two lists.
		- poks_near and empty_spaces. These lists are then flattened to be sent to the trainer.	
		- Upon recieving these lists the trainer makes a random choice first on the poks_near list because we always prioritize capturing a pokemon, if the pokemon list is empty then we make 
a random choice from the empty_spaces. If both lists are empty the we do nothing.
	- moveTrainer()
		- After deciding on a move it is passed to the moveTrainer rpc which moves the trainer from the server side.
		- It updates the pokedex if any pokemon are captured and also updates the capture_location dict which stores the names of the pokemons and the location at which they were captured.
		- Then it prints the board, pokedex, Captured locations and path tracker.
		- Finally the lock is released.


run_pokemon()
 
	- This is a function that is called asynchronously using async grpc.
	- The pokemon only run when the captured flag is zero. Which means it is still alive.
	- The pokemon then checks if it has the lock. If it has the lock then it uses the surroundings which is requested from the server to generate two lists.
	- valid_moves which take distance from a trainer into consideration and vlid_before_distance which does not consider the distance from trainer.
	- The pokemon prefers to make a random choice from the valid_moves list first and from valid_before_distance list next.
	-pokemonCheck() 
		- valid_moves which take distance from a trainer into consideration and vlid_before_distance which does not consider the distance from trainer.
	 	- It aquires the lock and looks and the surroundings and make two filtered lists and sends it to pokemon.
	- movePokemon()
		- The pokemon upon recieving the valid_move and valid_before_distance lists makes a choice and send it's choice to the server via movePokemon rpc.
		- The move pokemon rpc makes the move and updates the board and prints it.
		- It also updates and print the path tracker.
		- Then finally it releases the lock.
run_server()
 	
	- This is a function that is called asynchronously using async grpc.
	- It intializes the lock to 1 and the number of pokemons to P by reading from a config file.
	- Then it create a server and makes the necessary connections and adds services to the server.
	- Then it starts and waits to be terminated.
	- The termination occurs when all the pokemons have been captured.

main() 

	- It gets the host name and runs the server if the host names is server.
	- It runs the trainer or pokemon depending on the host name using asuncio.run() 


## RPC messages

your_name

	- This message type is used to store hostname.

Decision 

	- This message is used to describe space that the trainer or pokemon want to move to.
	- It consists of: move2 which is the choice, name which is the current hostname, cur_pos1 which is the current position and capture which is a flag taht indicates to the pokemon about it capture status.

Spaces
	- Spaces describes the spaces on the board that the trainer makes a decision on.
	- It consists of two lists, poks_near and emt_spaces an int to store number of pokemons left and cur_pos for current position on the board, loc is used for locking.
PSpaces

	- Similar to Space except it does not include the number of pokemon.
	- It is used by pokemons to represent their surroundings. 
	- It consists of two list, valid_mov and valid_mov_before, cur_posp to store current positon of pokemon and loc1 for locking.

Valid 
	- It is used to see if a move has completed successfully.

	 	 

## Assumptions

	- There can be only one element(pokemon/trainer) per space on the board.
	- The pokemon and trainer lists have 30 emojies each.
	- A google instance with 16 cores is used.


## Output

![Alt Text](https://github.com/CurSpace/cs5113fa22-project/blob/main/gif_AdobeExpress%20(2).gif)
