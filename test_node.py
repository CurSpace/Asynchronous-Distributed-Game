import json
import random
import socket
import grpc
import concurrent
import pokemon_pb2
import pokemon_pb2_grpc
import time
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
            board[x][y] = list(board_pieces.keys())[count]
            # initialize path tracker
            path_tracker[list(board_pieces.keys())[count]] = [[x,y]]

            # initialize 
            if list(board_pieces.keys())[count][:-1] == 'trainer':
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

def check_surroundings(hostname):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if str(board[i][j]) == hostname:
                you_are_at = (i,j)
                your_surroundings = [[i,j-1],[i-1,j],[i,j+1],[i+1,j],[i-1,j-1],[i-1,j+1],[i+1,j+1],[i+1,j-1]]
                #flatten list to send using rpc
                surroundings = [coordinate for position in your_surroundings for coordinate in position]
    return surroundings, you_are_at


def run_trainer():
    global board
    # add all trainer functionality
    # these two line make the connection
    # do everything under the with
    # set num_pokeomns so that it enters the loop when the loop runs for the first time it will be updated with the actual value
    with open('board_parameters.config') as config:
        params = config.read()
    board_parameters = json.loads(params)
    N = board_parameters['N']
    P = board_parameters['P']
    T = board_parameters['T']
    num_pokemons = 1
    count = 0
    while(num_pokemons != 0):
        num_pokemons = 0 
        with grpc.insecure_channel("server:50051") as channel:
            stub = pokemon_pb2_grpc.serverServiceStub(channel)
            my_name= socket.gethostname()
            # calling rpc funciton and using the messages
            response =  stub.trainerCheck(pokemon_pb2.your_name(name=my_name),wait_for_ready=True)
            # only do this for the first iteratoin of the infinite loop
            if count == 0:
                num_pokemons = response.n_pokemons
                count = count + 1
            
            # convert to pairs
            if len(response.pokemons_near) != 0:
                poks_near = [[response.pokemons_near[i],response.pokemons_near[i+1]] for i in range(0, len(response.pokemons_near), 2)]
            else:
                poks_near = []

            if len(response.emt_spaces) != 0:
                empty_spaces = [[response.emt_spaces[i],response.emt_spaces[i+1]] for i in range(0, len(response.emt_spaces), 2)]
            else:
                empty_spaces = []

 # client makes choice
 
            if len(poks_near) > 0 :
                move_to = random.choice(poks_near)
    # add pokemon to pokedex
    # replace pokemon with trainer and remove trainer from original space


            elif len(empty_spaces) > 0:
    # replace choosen empty space with trainer and remove trainer from original space
                move_to = random.choice(empty_spaces)
            else:
                move_to = []
            #Client sends its coice to server through the parameters 
            print("MOVE TO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11",type(move_to))
            des =  stub.moveTrainer(pokemon_pb2.Decision(move2 = move_to, name = my_name,cur_pos1 = response.cur_pos),wait_for_ready=True)

def run_pokemon():
    # add all pokemon functionality
    '''
    with grpc.insecure_channel("server:50051") as channel:
        stub = pokemon_pb2_grpc.serverServiceStub(channel)
        my_name= socket.gethostname()
        # calling rpc funciton and passing message your_name to it
        response =  stub.trainerCheck(pokemon_pb2.your_name(name=my_name),wait_for_ready=True)
'''

           # the choice happens here 
# the class name is the name of the service in proto file

    with open('board_parameters.config') as config:
        params = config.read()
    board_parameters = json.loads(params)
    N = board_parameters['N']
    P = board_parameters['P']
    T = board_parameters['T']

    while(captured = 1):
        with grpc.insecure_channel("server:50051") as channel:
            stub = pokemon_pb2_grpc.serverServiceStub(channel)
            my_name= socket.gethostname()
            # calling rpc funciton and using the messages
            response =  stub.pokemonCheck(pokemon_pb2.your_name(name=my_name),wait_for_ready=True)
            # make decision using the lists here!!!!!!!!!!!!!!!!!!!!!!!!!11

            # convert to pairs
            if len(response.pokemons_near) != 0:
                valid_moves = [[response.valid_movs[i],response.valid_movs[i+1]] for i in range(0, len(response.valid_movs), 2)]
            else:
               valid_moves = []
class serverService(pokemon_pb2_grpc.serverServiceServicer):
    def trainerCheck(self, request, context):
        global num_pokemons
        poks_near = []
        empty_spaces = []
        my_pokemons = []
        print("Trainer host",request.name)        
        
        with open('board_parameters.config') as config:
            params = config.read()
        board_parameters = json.loads(params)
        N = board_parameters['N']
        P = board_parameters['P']
        T = board_parameters['T']
        # getting hostname and using it at server side to check surroundings 
        surroundings, you_are_at = check_surroundings(request.name) 
        # the rpc funciton stores all the values of the necessary fields
            # convert list form rpc back to pairs
        your_surroundings = [[surroundings[i],surroundings[i+1]] for i in range(0, len(surroundings), 2)]
        print(your_surroundings)

        for i,move in enumerate(your_surroundings):
            if move[0] < 0 or move[0] >= N or move[1] < 0 or move[1] >= N:
                your_surroundings.pop(i)
    #can't stay at my current postion or a position occupied by another trainer.
            elif str(board[move[0]][move[1]]) != request.name and str(board[move[0]][move[1]])[:-1] == 'Trainer':
        #your_surroundings.remove([])
                your_surroundings.pop(i)
    # if there is a pokemon next to me add to list
            elif str(board[move[0]][move[1]])[:-1] == 'pokemon':
                poks_near.append(your_surroundings[i])
    # add all empty space to list
            else:
                empty_spaces.append(your_surroundings[i])
            
        you_are_at = list(you_are_at)
         
        print("Empty Spaces",empty_spaces)
        print("Pokemons Near", poks_near)
        #flatten lists to send through rcp
        if len(empty_spaces) != 0:
            empty_space = [coordinate for position in empty_spaces for coordinate in position]
        else:
            empty_space = []

        if len(poks_near) != 0: 
            poks_near_by = [coordinate for position in poks_near for coordinate in position]
        else: 
            poks_near_by = []

        return(pokemon_pb2.Spaces(pokemons_near = poks_near_by,emt_spaces = empty_space, n_pokemons = num_pokemons, cur_pos = you_are_at ))

    def moveTrainer(self,request, context):
        global board 
        # need N to print board
        with open('board_parameters.config') as config:
            params = config.read()
        board_parameters = json.loads(params)
        N = board_parameters['N']
        P = board_parameters['P']
        T = board_parameters['T']
        # change the board based on decision form client/trainer
        board[request.move2[0]][request.move2[1]] = request.name
        board[request.cur_pos1[0]][request.cur_pos1[1]] = 0
        print("PRINT AT SERVER")
        printBoard(N)
        return(pokemon_pb2.Valid(move_status = 'moved!' ))

    def pokemonCheck(self, request, context):
        print("Trainer host",request.name)        
        invalid_moves = []
        occupied_by_trainer = []
        valid_before_distance = []

        with open('board_parameters.config') as config:
            params = config.read()
        board_parameters = json.loads(params)
        N = board_parameters['N']
        P = board_parameters['P']
        T = board_parameters['T']
        # getting hostname and using it at server side to check surroundings 
        surroundings, you_are_at = check_surroundings(request.name) 
        # the rpc funciton stores all the values of the necessary fields
            # convert list form rpc back to pairs
        your_surroundings = [[surroundings[i],surroundings[i+1]] for i in range(0, len(surroundings), 2)]
        print(your_surroundings)
        for i,move in enumerate(your_surroundings):
            if move[0] < 0 or move[0] >= N or move[1] < 0 or move[1] >= N:
                invalid_moves.append(move)

        valid_moves = [move for move in your_surroundings if move not in invalid_moves ]

        # remove moves with trainers
# make of list of trainers close by
        for i,j in valid_moves:
    #print(i,j)
            if str(board[i][j])[:-1] == 'trainer':
                occupied_by_trainer.append([i,j])
                valid_moves.remove([i,j])
        valid_before_distance = valid_moves

# compare valid move's distance with trainers
        for x,y in occupied_by_trainer:
            for i,j in valid_moves:
                if abs(x-i) <=1 or abs(y-j) <= 1:
                    valid_moves.remove([i,j])
        
        #flatten lists to send through rcp
        if len(valid_before_distance) != 0:
            valid_before_dist = [coordinate for position in valid_before_distance for coordinate in position]
        else:
            valid_before_dist = []

        if len(valid_moves) != 0: 
            valid_movs = [coordinate for position in valid_moves for coordinate in position]
        else: 
            valid_movs = []
        you_are_at = list(you_are_at)

        return(pokemon_pb2.Spacesp(valid_mov = valid_movs,valid_mov_before = valid_before_dist, cur_posp = you_are_at))

    def movePokemon(self,request,context):

    def captured(self, request, context):
        pass

    def reportMove(self, request, context):
        pass

global num_pokemons
def run_server():
    global num_pokemons
    with open('board_parameters.config') as config:
        params = config.read()
    board_parameters = json.loads(params)
    N = board_parameters['N']
    P = board_parameters['P']
    T = board_parameters['T']
    global board
    num_pokemons = P
    createBoard(N) 
    printBoard(N)
    # add server function to serverService class
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    pokemon_pb2_grpc.add_serverServiceServicer_to_server(serverService(),server)
    server.add_insecure_port('server:50051')
    server.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        server.stop(0)
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
