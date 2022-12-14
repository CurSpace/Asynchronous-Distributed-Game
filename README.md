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


## Demo gif

![Alt Text](https://github.com/CurSpace/cs5113fa22-project/blob/main/media/demo.gif)

## Output

Pokedex: 
Pokedex: {'trainer1': [], 'trainer2': [], 'trainer3': [], 'trainer4': ['pokemon11'], 'trainer5': ['pokemon1', 'pokemon20'], 'trainer6': [], 'trainer7': [], 'trainer8': [], 'trainer9': ['pokemon16', 'pokemon24'], 'trainer10': ['pokemon12', 'pokemon26'], 'trainer11': ['pokemon22', 'pokemon9', 'pokemon8'], 'trainer12': [], 'trainer13': ['pokemon14'], 'trainer14': [], 'trainer15': ['pokemon18'], 'trainer16': ['pokemon7'], 'trainer17': ['pokemon10'], 'trainer18': [], 'trainer19': [], 'trainer20': [], 'trainer21': [], 'trainer22': [], 'trainer23': ['pokemon15', 'pokemon21'], 'trainer24': ['pokemon25'], 'trainer25': ['pokemon3', 'pokemon19', 'pokemon23'], 'trainer26': ['pokemon17']}

Path Tracker:

 Path: {'trainer1': [[11, 8], [12, 8], [11, 7], [10, 7], [11, 8], [10, 9], [9, 9], [9, 8], [8, 9], [8, 8], [8, 9]], 'trainer2': [[11, 17], [12, 17], [12, 16], [11, 16], [12, 15]], 'trainer3': [[0, 12], [1, 13], [0, 13], [1, 12], [1, 13], [0, 13]], 'trainer4': [[6, 6], [7, 5], [8, 4], [9, 4], [8, 4], [9, 3], [8, 2]], 'trainer5': [[2, 16], [3, 15], [3, 16], [3, 15], [4, 15], [5, 15], [6, 14], [5, 15], [5, 14], [4, 14]], 'trainer6': [[3, 11], [2, 12], [3, 13], [4, 13], [4, 14], [3, 15], [4, 15], [4, 16], [3, 15], [3, 16]], 'trainer7': [[16, 9], [17, 10], [18, 11], [17, 10], [18, 11], [17, 11], [18, 12]], 'trainer8': [[14, 16], [13, 15], [12, 14], [13, 13], [12, 12], [12, 13]], 'trainer9': [[3, 18], [3, 19], [4, 18], [3, 19], [2, 18], [1, 19], [0, 19], [1, 19]], 'trainer10': [[15, 19], [15, 18], [16, 17], [15, 16], [16, 16], [15, 17], [14, 18], [13, 19], [13, 18], [13, 19]], 'trainer11': [[12, 15], [12, 16], [11, 16], [10, 15], [9, 14], [10, 15], [11, 15], [10, 16]], 'trainer12': [[6, 18], [5, 19], [4, 18], [4, 19], [5, 18], [5, 17], [6, 16], [5, 16], [4, 15]], 'trainer13': [[12, 13], [11, 13], [12, 12]], 'trainer14': [[16, 18], [17, 18], [16, 19], [15, 19], [14, 18], [13, 19], [13, 18], [13, 17]], 'trainer15': [[16, 15], [17, 14], [18, 13], [17, 14], [17, 13]], 'trainer16': [[8, 17], [8, 18], [8, 17], [7, 18], [8, 17], [7, 16], [7, 17]], 'trainer17': [[0, 5], [0, 4], [1, 3], [1, 2], [2, 1], [3, 0], [3, 1], [3, 2], [4, 3], [4, 4]], 'trainer18': [[9, 13], [9, 12], [8, 11], [9, 12]], 'trainer19': [[4, 9], [3, 10], [4, 10], [4, 11], [3, 10], [4, 9], [3, 8], [3, 7], [2, 7], [1, 8]], 'trainer20': [[5, 10], [5, 9], [4, 8], [5, 7], [5, 8]], 'trainer21': [[13, 14], [12, 15], [11, 16], [11, 15], [10, 16], [11, 15], [12, 15], [13, 16], [13, 15], [12, 14], [11, 13], [12, 14]], 'trainer22': [[18, 10], [19, 11], [19, 10], [18, 10], [17, 11], [16, 12], [15, 11], [16, 12]], 'trainer23': [[19, 1], [18, 2], [18, 3], [19, 3], [18, 3], [19, 4], [18, 5], [17, 6]], 'trainer24': [[13, 9], [12, 9], [12, 10], [11, 9], [12, 10], [13, 11], [14, 11], [14, 10]], 'trainer25': [[2, 1], [2, 0], [3, 1], [4, 1], [5, 2], [6, 1], [7, 1], [7, 2]], 'trainer26': [[15, 1], [16, 2], [15, 3], [14, 2], [14, 3], [13, 3], [14, 2], [13, 1], [14, 0], [14, 1]], 'pokemon1': [[5, 15]], 'pokemon2': [[10, 0]], 'pokemon3': [[2, 0]], 'pokemon4': [[14, 6]], 'pokemon5': [[13, 5]], 'pokemon6': [[11, 19]], 'pokemon7': [[8, 18]], 'pokemon8': [[9, 14]], 'pokemon9': [[10, 15]], 'pokemon10': [[3, 0]], 'pokemon11': [[7, 4], [7, 5]], 'pokemon12': [[15, 18]], 'pokemon13': [[16, 5]], 'pokemon14': [[11, 13]], 'pokemon15': [[18, 3]], 'pokemon16': [[3, 19]], 'pokemon17': [[16, 2]], 'pokemon18': [[17, 14]], 'pokemon19': [[5, 2]], 'pokemon20': [[6, 14]], 'pokemon21': [[17, 6]], 'pokemon22': [[12, 16]], 'pokemon23': [[6, 1]], 'pokemon24': [[1, 19]], 'pokemon25': [[13, 11], [12, 10]], 'pokemon26': [[13, 19]]} Path: {'trainer1': [[11, 8], [12, 8], [11, 7], [10, 7], [11, 8], [10, 9], [9, 9], [9, 8], [8, 9], [8, 8], [8, 9]], 'trainer2': [[11, 17], [12, 17], [12, 16], [11, 16], [12, 15]], 'trainer3': [[0, 12], [1, 13], [0, 13], [1, 12], [1, 13], [0, 13]], 'trainer4': [[6, 6], [7, 5], [8, 4], [9, 4], [8, 4], [9, 3], [8, 2]], 'trainer5': [[2, 16], [3, 15], [3, 16], [3, 15], [4, 15], [5, 15], [6, 14], [5, 15], [5, 14], [4, 14]], 'trainer6': [[3, 11], [2, 12], [3, 13], [4, 13], [4, 14], [3, 15], [4, 15], [4, 16], [3, 15], [3, 16]], 'trainer7': [[16, 9], [17, 10], [18, 11], [17, 10], [18, 11], [17, 11], [18, 12]], 'trainer8': [[14, 16], [13, 15], [12, 14], [13, 13], [12, 12], [12, 13]], 'trainer9': [[3, 18], [3, 19], [4, 18], [3, 19], [2, 18], [1, 19], [0, 19], [1, 19]], 'trainer10': [[15, 19], [15, 18], [16, 17], [15, 16], [16, 16], [15, 17], [14, 18], [13, 19], [13, 18], [13, 19]], 'trainer11': [[12, 15], [12, 16], [11, 16], [10, 15], [9, 14], [10, 15], [11, 15], [10, 16]], 'trainer12': [[6, 18], [5, 19], [4, 18], [4, 19], [5, 18], [5, 17], [6, 16], [5, 16], [4, 15]], 'trainer13': [[12, 13], [11, 13], [12, 12]], 'trainer14': [[16, 18], [17, 18], [16, 19], [15, 19], [14, 18], [13, 19], [13, 18], [13, 17]], 'trainer15': [[16, 15], [17, 14], [18, 13], [17, 14], [17, 13]], 'trainer16': [[8, 17], [8, 18], [8, 17], [7, 18], [8, 17], [7, 16], [7, 17]], 'trainer17': [[0, 5], [0, 4], [1, 3], [1, 2], [2, 1], [3, 0], [3, 1], [3, 2], [4, 3], [4, 4]], 'trainer18': [[9, 13], [9, 12], [8, 11], [9, 12]], 'trainer19': [[4, 9], [3, 10], [4, 10], [4, 11], [3, 10], [4, 9], [3, 8], [3, 7], [2, 7], [1, 8]], 'trainer20': [[5, 10], [5, 9], [4, 8], [5, 7], [5, 8]], 'trainer21': [[13, 14], [12, 15], [11, 16], [11, 15], [10, 16], [11, 15], [12, 15], [13, 16], [13, 15], [12, 14], [11, 13], [12, 14]], 'trainer22': [[18, 10], [19, 11], [19, 10], [18, 10], [17, 11], [16, 12], [15, 11], [16, 12]], 'trainer23': [[19, 1], [18, 2], [18, 3], [19, 3], [18, 3], [19, 4], [18, 5], [17, 6]], 'trainer24': [[13, 9], [12, 9], [12, 10], [11, 9], [12, 10], [13, 11], [14, 11], [14, 10]], 'trainer25': [[2, 1], [2, 0], [3, 1], [4, 1], [5, 2], [6, 1], [7, 1], [7, 2]], 'trainer26': [[15, 1], [16, 2], [15, 3], [14, 2], [14, 3], [13, 3], [14, 2], [13, 1], [14, 0], [14, 1]], 'pokemon1': [[5, 15]], 'pokemon2': [[10, 0]], 'pokemon3': [[2, 0]], 'pokemon4': [[14, 6]], 'pokemon5': [[13, 5]], 'pokemon6': [[11, 19]], 'pokemon7': [[8, 18]], 'pokemon8': [[9, 14]], 'pokemon9': [[10, 15]], 'pokemon10': [[3, 0]], 'pokemon11': [[7, 4], [7, 5]], 'pokemon12': [[15, 18]], 'pokemon13': [[16, 5]], 'pokemon14': [[11, 13]], 'pokemon15': [[18, 3]], 'pokemon16': [[3, 19]], 'pokemon17': [[16, 2]], 'pokemon18': [[17, 14]], 'pokemon19': [[5, 2]], 'pokemon20': [[6, 14]], 'pokemon21': [[17, 6]], 'pokemon22': [[12, 16]], 'pokemon23': [[6, 1]], 'pokemon24': [[1, 19]], 'pokemon25': [[13, 11], [12, 10]], 'pokemon26': [[13, 19]]}

Captured Locations:
 Captured Locations: {'pokemon12': [15, 18], 'pokemon22': [12, 16], 'pokemon17': [16, 2], 'pokemon3': [2, 0], 'pokemon14': [11, 13], 'pokemon11': [7, 5], 'pokemon9': [10, 15], 'pokemon25': [12, 10], 'pokemon7': [8, 18], 'pokemon8': [9, 14], 'pokemon15': [18, 3], 'pokemon16': [3, 19], 'pokemon18': [17, 14], 'pokemon10': [3, 0], 'pokemon1': [5, 15], 'pokemon26': [13, 19], 'pokemon19': [5, 2], 'pokemon20': [6, 14], 'pokemon23': [6, 1], 'pokemon24': [1, 19], 'pokemon21': [17, 6]}





