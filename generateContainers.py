#!/usr/bin/env python3

import argparse
import json
def main():

    pokemons = ['\U0001F980','\U0001F364','\U0001F436','\U0001F43B','\U0001F41F','\U0001F42C','\U0001F407','\U0001F40B','\U0001F99E','\U0001F421','\U0001F32C','\U0001F43C','\U0001F42B','\U0001F418','\U0001F99A','\U0001F404','\U0001F410','\U0001F40E','\U0001F416','\U0001F414','\U0001F986','\U0001F54A','\U0001F9A2','\U0001F426','\U0001F985','\U0001F98B','\U0001F41B','\U0001F41C','\U0001F997','\U0001F41D','\U0001F9A1','\U0001F43F']

    trainers = ['\U0001F9D2','\U0001F467','\U0001F468','\U0001F603','\U0001F9D3','\U0001F937','\U0001F604','\U0001F601','\U0001F605','\U0001F600','\U0001F642','\U0001F643','\U0001F609','\U0001F60A','\U0001F607','\U0001F970','\U0001F60D','\U0001F929','\U0001F60B','\U0001F61B','\U0001F92A','\U0001F61D','\U0001F911','\U0001F917','\U0001F92D','\U0001F92B','\U0001F914','\U0001F910','\U0001F928','\U0001F611']
    # gettiing size of board N, number of pokemons P and number of trainers T from user
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type = int, choices = range(1,101), required = True)
    parser.add_argument('--P', type = int, choices = range(1,30), required = True)
    parser.add_argument('--T', type = int, choices = range(1,30), required = True)
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
