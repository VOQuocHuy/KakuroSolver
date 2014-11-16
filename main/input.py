__author__ = 'prateek'
from node import Node
from game import Game

def input_console():
    K = input()
    M = input()
    #input =[[Node(0,0) for row in range(0,K)] for column in range(0,K)]
    inputMatrix =[[0 for row in range(0,K)] for column in range(0,K)]

    for i in range(0,K):
        for j in range(0,M):
            node_type,node_value = raw_input().split(' ')
            input[i][j] = Node(int(node_type),int(node_value))
    #print input[0][0].node_type
    return inputMatrix

def input_file():
    handler = open("testcases/input.txt")
    text= handler.readlines()
    print text

input_file()

