import json
def createBoard(N):
    board = [[0 for i in range(N)] for j in range(N)]
    print(board)
    # intialize board



def main():
    # read config
    with open('board_parameters.config') as config:
        params = config.read()
    board_parameters = json.loads(params)
    print(board_parameters)
    N = board_parameters['N']
    P = board_parameters['P']
    T = board_parameters['T']
    createBoard(N)

if __name__ == '__main__':
    main()
