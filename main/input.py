__author__ = 'prateek'
from node import Node
from game import Game
import time
import sys


def input_console():
    K = input()
    M = input()
    #input =[[Node(0,0) for row in range(0,K)] for column in range(0,K)]
    input_matrix =[[0 for row in range(0,K)] for column in range(0,K)]

    for i in range(0,K):
        for j in range(0,M):
            node_type,node_value = raw_input().split(' ')
            input[i][j] = Node(node_type,node_value)
    #print input[0][0].node_type
    return input_matrix,K,M

def input_file():
    input_matrix=[]
    path = sys.argv[1]
    if path=="":
        path = "testcases/testcase5.txt"
    handler = open(path)
    text= handler.readlines()
    M= len(text)
    N=0;
    i=0;
    for line in text:
        elements = line.replace("\n","").split(" ")
        print (elements)
        N= len(elements)
        row = []
        j=0
        for element in elements:
            #print "processing element"+ element
            if element.find(':')!=-1:
                #print "Creating constraint node"
                row.append(Node(i,j,1,element))
            else:
                if int(element)==-1:
                    #print "Creating blank node"
                    row.append(Node(i,j,-1,-1))
                else:
                #    print "Creating value node"
                    row.append(Node(i,j,0,int(element)))
            j=j+1
        input_matrix.append(row)
        i+=1
    #print input_matrix
    return input_matrix,M,N


matrix,M,N= input_file()
start = time.time()
game= Game(matrix,M,N)
game.print_matrix()
game.formulate()
end = time.time()
print "\n"
print "Running Time"
print end-start

