#!/usr/bin/python
__author__ = 'prateek'
#This class represents a node in the matrix
# Type 0 corresponds to the value node
# Type 1 corresponds to the constraint node
# Type 2 corresponds to the black node
class Node:
    node_type=0
    node_value=0
    def __init__(self,type,value):
        self.node_type=type
        self.node_value=value

    def set_value(self,value):
        self.node_value= value
