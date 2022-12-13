#!/usr/bin/env python3

import argparse
import json
def main():

    trainers = ["\U0001F480", "\U0001F9D2", "\U0001F466", "\U0001F467", "\U0001F9B3", "\U0001F468", "\U0001F469", "\U0001F64D", "\U0001F475", "\U0001F9D3"]

    pokemons = ["\U0001F412", "\U0001F98D", "\U0001F43A", "\U0001F98A", "\U0001F436", "\U0001F431", "\U0001F981", "\U0001F42E", "\U0001F437", "\U0001F42D"]
    print("Enter N,P and T")
    # gettiing size of board N, number of pokemons P and number of trainers T from user
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type = int, choices = range(1,10), required = True)
    parser.add_argument('--P', type = int, choices = range(1,10), required = True)
    parser.add_argument('--T', type = int, choices = range(1,10), required = True)
    args = parser.parse_args()
    
    # Storing N,P and T into a config file
    board_parameters = {'N':args.N,'P':args.P,'T':args.T}
    with open('board_parameters.config','w') as config:
        config.write(json.dumps(board_parameters))

    # Creating docker-compose from user input
    node_creator = open("docker-compose.yml","w")
    node_creator.write("version: '3.7'\n\n")
    # creating server
    node_creator.write("services:\n  server:\n    build: .\n    hostname: server\n    container_name: Server\n    networks:\n    - default")
    
    # creating the pokemon nodes 
    pieces_dict = {}
    for i in range(1,args.T + 1):
        node_creator.write("\n  train"+str(i)+":\n    build: .\n    hostname: trainer"+str(i)+"\n    container_name: Trainer"+str(i)+"\n    networks:\n     - default")
        # appending to dict
        pieces_dict['trainer'+str(i)] = trainers[i]

    for i in range(1,args.P + 1):
        node_creator.write("\n  poke"+str(i)+":\n    build: .\n    hostname: pokemon"+str(i)+"\n    container_name: Pokemon"+str(i)+"\n    networks:\n     - default")
        pieces_dict['pokemon'+str(i)] = pokemons[i]

    node_creator.close()
    # storing as str because if i do dumps cannot print the emoji
    with open("board_pieces.config",'w') as config1:
        config1.write(json.dumps(pieces_dict))
    
    node_creator.close()
    
if __name__ == "__main__":
    main()
