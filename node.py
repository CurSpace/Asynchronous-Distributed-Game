import json
import random
import socket
import grpc
import concurrent
import pokemon_pb2
import pokemon_pb2_grpc
import time
import asyncio

global board
global num_pokemons
global pokedex
global path_tracker
global lock
global capture_locations
def createBoard(N):
    global board
    global pokedex 
    global path_tracker 
    global capture_locations 
    global num_pokemons
    pokedex = {}
    path_tracker = {}
    capture_locations = {}
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
            if list(board_pieces.keys())[count].startswith('trainer') == True:
                pokedex[list(board_pieces.keys())[count]]= [] 
            count = count + 1


# function to display the board
def printBoard(N):
    global board

    with open('board_pieces.config') as config:
        pieces = config.read()
    board_pieces = json.loads(pieces)
    print(' ','_'*6*N)
    print()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if  j == N -1 and board[i][j] == 0 :
                print('  | ',board[i][j],end = '  | ')
            elif j == N - 1:
                print('  | ',board_pieces[board[i][j]],end = ' |')

            elif board[i][j] == 0:
                print('  | ',board[i][j],end = '')
            # pokemon or trainer
            else:
                print('  |',board_pieces[board[i][j]], end = '')

        
        print()
        print(' ','_'*6*N)
        print()
    time.sleep(1)

def check_surroundings(hostname):
    your_surroundings = []
    surroundings = []
    you_are_at = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if str(board[i][j]) == hostname:
                you_are_at = [i,j]
                your_surroundings = [[i,j-1],[i-1,j],[i,j+1],[i+1,j],[i-1,j-1],[i-1,j+1],[i+1,j+1],[i+1,j-1]]
                #flatten list to send using rpc
    if len(your_surroundings) != 0:
        surroundings = [coordinate for position in your_surroundings for coordinate in position]
    return surroundings, you_are_at


async def run_trainer():
    global num_pokemons
    global lock
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
    num_pokemons = P
    while(num_pokemons != 0):
       async with grpc.aio.insecure_channel("server:50051") as channel:
            stub = pokemon_pb2_grpc.serverServiceStub(channel)
            my_name= socket.gethostname()
            # calling rpc funciton and using the messages
            response =  await stub.trainerCheck(pokemon_pb2.your_name(name=my_name),wait_for_ready=True)
            # only do this for the first iteratoin of the infinite loop
            num_pokemons = response.n_pokemons
            if response.loc == 0:
            
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
 
                if len(poks_near) != 0 :
                    captures = 1
                    move_to = random.choice(poks_near)
    # add pokemon to pokedex
    # replace pokemon with trainer and remove trainer from original space


                elif len(empty_spaces) != 0:
    # replace choosen empty space with trainer and remove trainer from original space
                    captures = 0
                    move_to = random.choice(empty_spaces)
                else:
                    move_to = []
                    captures = 0
            #Client sends its coice to server through the parameters 
                des = await stub.moveTrainer(pokemon_pb2.Decision(move2 = move_to, name = my_name,cur_pos1 = response.cur_pos, capture = captures),wait_for_ready=True)
            else:
                pass

async def run_pokemon():
    global lock
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
    captured = 0
    while(captured == 0):
       async with grpc.aio.insecure_channel("server:50051") as channel:
            stub = pokemon_pb2_grpc.serverServiceStub(channel)
            my_name= socket.gethostname()
            # calling rpc funciton and using the messages
            response =  await stub.pokemonCheck(pokemon_pb2.your_name(name=my_name),wait_for_ready=True)
            # make decision using the lists here!!!!!!!!!!!!!!!!!!!!!!!!!11
            # has lock so proceed
            if response.loc1 == 0:
                if len(response.cur_posp) != 0:

            # convert to pairs
                    if len(response.valid_mov) != 0:
                        valid_moves = [[response.valid_mov[i],response.valid_mov[i+1]] for i in range(0, len(response.valid_mov), 2)]
                    else:
                        valid_moves = []

                    if len(response.valid_mov_before) != 0:
                        valid_before_distance = [[response.valid_mov_before[i],response.valid_mov_before[i+1]] for i in range(0, len(response.valid_mov_before), 2)]
                    else:
                        valid_before_distance  = []
            
            # use the above two lists to make a choice
                    if len(valid_moves) != 0:
                        move_to = random.choice(valid_moves)

                    elif len(valid_before_distance) != 0:
                        move_to = random.choice(valid_before_distance)

                    else:
                        move_to = []
                    des = await stub.movePokemon(pokemon_pb2.Decision(move2 = move_to, name = my_name,cur_pos1 = list(response.cur_posp)),wait_for_ready=True)

                else:
                    captured = 1
            else:
                pass

class serverService(pokemon_pb2_grpc.serverServiceServicer):
    def trainerCheck(self, request, context):
        global num_pokemons
        global lock
        poks_near = []
        your_surroundings = []
        empty_spaces = []
        empty_space = []
        poks_near_by = []
        my_pokemons = []
        you_are_at = []
        # take lock
        if lock == 1:
            lock = 0
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
        
            if len(surroundings) != 0:

                your_surroundings = [[surroundings[i],surroundings[i+1]] for i in range(0, len(surroundings), 2)]

                for i,move in enumerate(your_surroundings):
                    if move[0] < 0 or move[0] >= N or move[1] < 0 or move[1] >= N:
                        your_surroundings.pop(i)
    #can't stay at my current postion or a position occupied by another trainer.
                    elif str(board[move[0]][move[1]]) != request.name and str(board[move[0]][move[1]]).startswith('trainer') == True:
        #your_surroundings.remove([])
                        your_surroundings.pop(i)
    # if there is a pokemon next to me add to list
                    elif str(board[move[0]][move[1]]).startswith('pokemon') == True:
                        poks_near.append(your_surroundings[i])
    # add all empty space to list
                    else:
                        empty_spaces.append(your_surroundings[i])
            
        
        #flatten lists to send through rcp
            if len(empty_spaces) != 0:
                empty_space = [coordinate for position in empty_spaces for coordinate in position]

            if len(poks_near) != 0: 
                poks_near_by = [coordinate for position in poks_near for coordinate in position]
        
            return(pokemon_pb2.Spaces(pokemons_near = poks_near_by,emt_spaces = empty_space, n_pokemons = num_pokemons, cur_pos = you_are_at,loc = lock ))
        else:
            return(pokemon_pb2.Spaces(pokemons_near = [],emt_spaces = [], n_pokemons = num_pokemons, cur_pos = [],loc = lock ))

    def moveTrainer(self,request, context):
        global board 
        global pokedex
        global capture_locations
        global num_pokemons
        global lock
        global path_tracker

        # need N to print board
        with open('board_parameters.config') as config:
            params = config.read()
        board_parameters = json.loads(params)
        N = board_parameters['N']
        P = board_parameters['P']
        T = board_parameters['T']
        # change the board based on decision form client/trainer
        
       # update pokedex when pokemon is captures
        if request.capture == 1 and len(request.move2) != 0:
                pokedex[request.name].append(board[request.move2[0]][request.move2[1]]) 
                path_tracker[request.name].append(request.move2)
                capture_locations[board[request.move2[0]][request.move2[1]]] = request.move2
                board[request.move2[0]][request.move2[1]] = request.name
                board[request.cur_pos1[0]][request.cur_pos1[1]] = 0
                num_pokemons = num_pokemons - 1 
        elif len(request.move2) != 0:
            path_tracker[request.name].append(request.move2)
            board[request.move2[0]][request.move2[1]] = request.name
            board[request.cur_pos1[0]][request.cur_pos1[1]] = 0
        else: 
            pass
        printBoard(N)
        print("Pokedex:", pokedex)
        print("Captured Locations:", capture_locations)
        print("Path:", path_tracker)
        # release lock
        lock = 1
        return(pokemon_pb2.Valid(move_status = 'moved!' ))

    def pokemonCheck(self, request, context):
        global lock
        invalid_moves = []
        occupied_by_trainer = []
        valid_before_distance = []
        your_surroundings = []
        you_are_at = []
        # take lock
        if lock == 1:
            lock = 0
            with open('board_parameters.config') as config:
                params = config.read()
            board_parameters = json.loads(params)
            N = board_parameters['N']
            P = board_parameters['P']
            T = board_parameters['T']
        # getting hostname and using it at server side to check surroundings 
            surroundings, you_are_at = check_surroundings(request.name) 

            if len(surroundings) != 0:
        # the rpc funciton stores all the values of the necessary fields
            # convert list form rpc back to pairs
                your_surroundings = [[surroundings[i],surroundings[i+1]] for i in range(0, len(surroundings), 2)]
                for i,move in enumerate(your_surroundings):
                    if move[0] < 0 or move[0] >= N or move[1] < 0 or move[1] >= N:
                        invalid_moves.append(move)

                valid_moves = [move for move in your_surroundings if move not in invalid_moves ]

        # remove moves with trainers
# make of list of trainers close by
                if valid_moves != 0:
                    for i,j in valid_moves:
    #print(i,j)
                        if str(board[i][j]).startswith('trainer') == True:
                            occupied_by_trainer.append([i,j])
                            valid_moves.remove([i,j])
                    valid_before_distance = valid_moves

# compare valid move's distance with trainers
                    for x,y in occupied_by_trainer:
                        for i,j in valid_moves:
                            if abs(x-i) <=1 or abs(y-j) <= 1:
                                valid_moves.remove([i,j])
            else:
                valid_before_distance = []
                valid_moves = []
        #flatten lists to send through rcp
            if len(valid_before_distance) != 0:
                valid_before_dist = [coordinate for position in valid_before_distance for coordinate in position]
            else:
                valid_before_dist = []

            if len(valid_moves) != 0: 
                valid_movs = [coordinate for position in valid_moves for coordinate in position]
            else: 
                valid_movs = []

            return(pokemon_pb2.PSpaces(valid_mov = valid_movs,valid_mov_before = valid_before_dist, cur_posp = you_are_at, loc1 = lock))
        else:

            return(pokemon_pb2.PSpaces(valid_mov = [],valid_mov_before = [], cur_posp = [], loc1 = lock))

    def movePokemon(self,request,context):
        global num_pokemons
        global board 
        global path_tracker
        # need N to print board
        with open('board_parameters.config') as config:
            params = config.read()
        board_parameters = json.loads(params)
        N = board_parameters['N']
        P = board_parameters['P']
        T = board_parameters['T']
        # change the board based on decision form client/trainer
        if len(request.move2) != 0:

            path_tracker[request.name].append(request.move2)
            board[request.move2[0]][request.move2[1]] = request.name
            board[request.cur_pos1[0]][request.cur_pos1[1]] = 0
        else:
            pass
        printBoard(N)
        print("Path:", path_tracker)
        # release loc
        lock = 1
        return(pokemon_pb2.Valid(move_status = 'moved!' ))


global num_pokemons
async def run_server():
    global num_pokemons
    global lock
    lock = 1
    with open('board_parameters.config') as config:
        params = config.read()
    board_parameters = json.loads(params)
    N = board_parameters['N']
    P = board_parameters['P']
    T = board_parameters['T']
    global board
    num_pokemons = P
    createBoard(N) 
    # add server function to serverService class
    server = grpc.aio.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    pokemon_pb2_grpc.add_serverServiceServicer_to_server(serverService(),server)
    server.add_insecure_port('server:50051')
    await server.start()
    await server.wait_for_termination()
    '''
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        server.stop(0)
        '''
def main():
    global pokedex
    global path_tracker
    global capture_locations
    # read config
    name = socket.gethostname()
    if name == 'server':
        asyncio.run(run_server())
    if name.startswith('trainer') == True:
        asyncio.run(run_trainer())
    
    if name.startswith('pokemon') == True:
        asyncio.run(run_pokemon())

if __name__ == '__main__':
    main()
    
