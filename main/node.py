#!/usr/bin/python
__author__ = 'prateek'

class NodeType:
    VALUE_NODE=0
    CONSTRAINT_NODE=1
    BLANK_NODE=-1
#This class represents a node in the matrix
# Type 0 corresponds to the value node
# Type 1 corresponds to the constraint node
# Type -1 corresponds to the black node
class Node:
    node_type=-1
    node_value=-1
    col_constraint = -1
    row_constraint = -1
    def __init__(self,type,value):
        self.node_type=type
        self.node_value=value
        if self.node_type== NodeType.VALUE_NODE:
            self.domain={}
            for i in range(1,10):
                self.domain[i]=True
        else:
            self.domain={}

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
    def set_value(self,value):
        self.node_value= value
