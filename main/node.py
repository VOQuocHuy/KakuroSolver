#!/usr/bin/python
__author__ = 'prateek'

class NodeType:
    VALUE_NODE=0
    CONSTRAINT_NODE=1
    BLACK_NODE=-1
#This class represents a node in the matrix
# Type 0 corresponds to the value node
# Type 1 corresponds to the constraint node
# Type -1 corresponds to the black node
class Node(object):
    #node_type=-1
    #node_value=-1
    #col_constraint = -1
    #row_constraint = -1
    #adjList=[]
    #row_index=-1
    #col_index=-1
    #domain

    def __init__(self,row_index,col_index,type,value):
        self.row_index=row_index
        self.col_index= col_index
        self.node_type=type
        self.node_value=value
        self.adj_list=[]
        self.domain={}
        if self.node_type== NodeType.VALUE_NODE:
            self.domain={}
            for i in range(1,10):
                self.domain[i]=True
        else:
            self.domain={}
        self.prev_domain={}
        if self.node_type== NodeType.VALUE_NODE:
            self.visited=False

        if self.node_type== NodeType.CONSTRAINT_NODE:
            col_constraint,row_constraint = self.node_value.split(':')

            #print "column constraint "+col_constraint
            #print "row constraint "+row_constraint
            if len(col_constraint)!=0:
                self.col_constraint = int(col_constraint)
            else:
                self.col_constraint=-1
            if len(row_constraint)!=0:
                self.row_constraint= int(row_constraint)
            else:
                self.row_constraint=-1
        if self.node_type==NodeType.VALUE_NODE:
            self.left_constraint_coord=None
            self.top_constraint_coord =None

    def __cmp__(self,other):
            if other!=None:
                return len(self.domain)-len(other.domain)
            else:
                return True

    def set_value(self,value):
        self.node_value= value
