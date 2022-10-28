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
