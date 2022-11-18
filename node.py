import json
import random
import socket

def createBoard(N):
    board = [[0 for i in range(N)] for j in range(N)]
    # intialize board
    with open('board_pieces.config') as config:
        pieces = config.read()
    board_pieces = json.loads(pieces)
    # Inserting the pieces into the board
    for i in range(len(board_pieces)):
        # randomizing the index values
        x = random.randint(0,N - 1)
        y = random.randint(0, N - 1)
        # insert only if space is empty
        if board[x][y] == 0:
            board[x][y] = list(board_pieces.values())[i]
    return board, board_pieces

def printBoard(board,N):
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


def run_server():
    with open('board_parameters.config') as config:
        params = config.read()
    board_parameters = json.loads(params)
    N = board_parameters['N']
    P = board_parameters['P']
    T = board_parameters['T']
    board, board_pieces = createBoard(N) 
    printBoard(board,N)

def main():
    # read config
    name = socket.gethostname()
    if name == 'server':
        run_server()


if __name__ == '__main__':
    main()
