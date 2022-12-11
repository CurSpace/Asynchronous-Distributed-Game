import json
import random
import socket

global board
def createBoard(N):
    global board
    pokedex = {}
    path_tracker = {}
    board = [[0 for i in range(N)] for j in range(N)]
    # intialize board
    with open('board_pieces.config') as config:
        pieces = config.read()
    board_pieces = json.loads(pieces)
    # Inserting the pieces into the board
    count  = 0
    while(count != len(board_pieces)):
        # randomizing the index values
        x = random.randint(0,N - 1)
        y = random.randint(0, N - 1)
        # insert only if space is empty
        if board[x][y] == 0:
            board[x][y] = list(board_pieces.values())[count]
            # initialize path tracker
            path_tracker[list(board_pieces.keys())[count]] = [[x,y]]

            # initialize 
            if list(board_pieces.keys())[count][:-1] == 'Trainer':
                pokedex[list(board_pieces.keys())[count]]= [] 
            count = count + 1

    print("Pokedex",pokedex)
    print("Path Tracker", path_tracker)
    # store pokedex and path_tracker in a file for later use
    with open("pokedex.config",'w') as config1:
            config1.write(json.dumps(pokedex))

    with open("pokedex.config",'w') as config2:
            config2.write(json.dumps(path_tracker))


# function to display the board
def printBoard(N):
    global board
    print(' ','_'*6*N)
    print()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if  j == N -1 and board[i][j] == 0 :
                print('  | ',board[i][j],end = '  | ')
            elif j == N - 1:
                print('  | ',board[i][j],end = ' |')

            elif board[i][j] == 0:
                print('  | ',board[i][j],end = '')
            # pokemon or trainer
            else:
                print('  |',board[i][j], end = '')

        
        print()
        print(' ','_'*6*N)
        print()

def check_surroundings():
    for i in range(len(board)):
    for j in range(len(board[i])):
        if str(board[i][j]) == hostname:
            you_are_at = (i,j)
            your_surroundings = [[i,j-1],[i-1,j],[i,j+1],[i+1,j],[i-1,j-1],[i-1,j+1],[i+1,j+1],[i+1,j-1]]
    return your_surroundings

def pokemon_move():
    pass

def trainer_move():
    pass

def run_server():
    with open('board_parameters.config') as config:
        params = config.read()
    board_parameters = json.loads(params)
    N = board_parameters['N']
    P = board_parameters['P']
    T = board_parameters['T']
    global board
    createBoard(N) 
    printBoard(N)

def run_trainer():
    # add all trainer functionality
global board
poks_near = []
empty_spaces = []
my_pokemons = []
pokedex = {}

for i,move in enumerate(your_surroundings):

    if move[0] < 0 or move[0] > N or move[1] < 0 or move[1] > N:
        your_surroundings.pop(i)
    #can't stay at my current postion or a position occupied by another trainer.
    elif str(board[move[0]][move[1]]) != hostname and str(board[move[0]][move[1]])[:-1] == 'Trainer':
        print(i)
        #your_surroundings.remove([])
        your_surroundings.pop(i)
    # if there is a pokemon next to me add to list
    elif str(board[move[0]][move[1]])[:-1] == 'Pokemon':
        poks_near.append(your_surroundings[i])
    # add all empty space to list
    else:
        empty_spaces.append(your_surroundings[i])

print(len(poks_near))
print(empty_spaces)
if len(poks_near) > 0 :
    move_to = random.choice(poks_near)
    # add pokemon to pokedex
    my_pokemons.append(board[move[0]][move[1]])
    pokedex[hostname] = my_pokemons
    # replace pokemon with trainer and remove trainer from original space
    board[move[0]][move[1]] = hostname
    board[you_are_at[0]][you_are_at[1]] = 0
    
    
else:
    # replace choosen empty space with trainer and remove trainer from original space
    move_to = random.choice(empty_spaces)
    board[move_to[0]][move_to[1]] = hostname
    board[you_are_at[0]][you_are_at[1]] = 0


def run_pokemon():
    # add all pokemon functionality
    for i,move in enumerate(your_surroundings):
    if move[0] < 0 or move[1] < 0 or move[0] > N or move[1] > N:
        #print(move)
        invalid_moves.append(move)
#         your_surroundings.pop(i)

valid_moves = [move for move in your_surroundings if move not in invalid_moves ]

# remove moves with trainers
# make of list of trainers close by
print(board)
for i,j in valid_moves:
    #print(i,j)
    if str(board[i][j])[:-1] == 'Trainer':
        occupied_by_trainer.append([i,j])
        valid_moves.remove([i,j])

valid_before_distance = valid_moves

print('Valid Before Taking distance into consideration',valid_moves)

# compare valid move's distance with trainers
for x,y in occupied_by_trainer:
    for i,j in valid_moves:
        if abs(x-i) <=1 or abs(y-j) <= 1:
            valid_moves.remove([i,j])
            
   # if str(board[i][j]) ==
# when valid_moves is not empty randomly coose on element
if valid_moves:
    move_to = random.choice(valid_moves)
    # replace empty pokemon tand remove pokemon from original space
    board[move[0]][move[1]] = pokemon_name
    board[you_are_at[0]][you_are_at[1]] = 0

elif valid_before_distance:
    move_to = random.choice(valid_before_distance) 
    # replace empty pokemon tand remove pokemon from original space
    board[move[0]][move[1]] = pokemon_name
    board[you_are_at[0]][you_are_at[1]] = 0

    # Don't move if the valid list is empty in the first place
else:
    pass
#print("Invalid Move",invalid_moves)
print("Valid Moves",valid_moves)
print(your_surroundings)
print(occupied_by_trainer)

def main():
    # read config
    name = socket.gethostname()
    if name == 'server':
        run_server()
    if name[:-1] == 'trainer':
        run_trainer()
    
    if name[:-1] == 'pokemon':
        run_pokemon()

if __name__ == '__main__':
    main()
