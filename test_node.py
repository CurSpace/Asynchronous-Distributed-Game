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


def run_trainer():
    # add all trainer functionality
    # these two line make the connection
    # do everything under the with
    with grpc.insecure_channel("server:50051") as channel:
        stub = pokemon_pb2_grpc.serverServiceStub(channel)
        my_name= socket.gethostname()
        # calling rpc funciton and using the messages
        response =  stub.trainerCheck(pokemon_pb2.your_name(name=my_name),wait_for_ready=True)

def run_pokemon():
    # add all pokemon functionality
    with grpc.insecure_channel("server:50051") as channel:
        stub = pokemon_pb2_grpc.serverServiceStub(channel)
        my_name= socket.gethostname()
        # calling rpc funciton and passing message your_name to it
        response =  stub.trainerCheck(pokemon_pb2.your_name(name=my_name),wait_for_ready=True)

# the class name is the name of the service in proto file

class serverService(pokemon_pb2_grpc.serverServiceServicer):
    def trainerCheck(self, request, context):
        print("Trainer host",request.name)        

    def pokemonCheck(self, request, context):
        print("Trainer host",request.name)        

    def captured(self, request, context):
        pass

    def reportMove(self, request, context):
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
