__author__ = 'prateek'
from node import Node
from node import NodeType

class Game:
    matrix = []
    rows =0
    cols =0
    solutionMatrix=[]

    def __init__(self,matrix,row_count,column_count):
        self.matrix = matrix
        self.rows=row_count
        self.cols = column_count
        self.solutionMatrix=[[-1 for i in range(0,self.rows)] for j in range(0,self.cols)]
        self.unsolvedCount=-1
        self.unsolvedPositions=[]
        print self.solutionMatrix

    def formulate(self):
        print "Starting problem formulation"
        self.print_matrix()
        self.node_consistency()
        #self.init_unsolved()
        self.create_constraint_graph()
        self.print_constraint_graph()
        self.solve()

        # formulate the problem and add data structures which might help solve the problem
        # instrument the matrix to populate the data structures

    def solve(self):
        # The Algorithm goes here
        print "Solving KAKURO"


    def print_matrix(self):
        self.unsolvedCount=0
        for i in range(0,self.rows):
            print "--------------"
            for j in range(0,self.cols):
                print str(self.matrix[i][j].node_value) + " domain: "+str(self.matrix[i][j].domain.keys())
                #print "row id : "+str(self.matrix[i][j].row_index)
                #print "col id : "+str(self.matrix[i][j].col_index)

                if self.matrix[i][j].node_type==NodeType.VALUE_NODE and self.matrix[i][j].node_value==0:
                    self.unsolvedCount+=1


    def create_constraint_graph(self):
        print "Creating constraint graph"
        for i in range(0,self.rows):
            for j in range(0,self.cols):
                if self.matrix[i][j].node_type==NodeType.CONSTRAINT_NODE:
                    col_constraint= self.matrix[i][j].col_constraint;
                    #print col_constraint
                    if(col_constraint!=-1):
                        col_list=[]
                        print "Traversing constraints in the same column"
                        # found a valid column constraint for this node
                        # search all rows greater than i till the next constraint node or black node

                        k=i+1;
                        while k<self.rows and (self.matrix[k][j].node_type!=NodeType.BLACK_NODE or self.matrix[k][j].node_type!=NodeType.CONSTRAINT_NODE):
                            col_list.append(self.matrix[k][j])
                            k=k+1
                        done_list=[]
                        for nd1 in col_list:
                            for nd2 in col_list:
                                if nd2.row_index not in done_list:
                                    if nd1.row_index!=nd2.row_index:
                                        nd1.adj_list.append((nd2.row_index,nd2.col_index))
                                        nd2.adj_list.append((nd1.row_index,nd1.col_index))
                            done_list.append(nd1.row_index)
                        # further reduce the domain by eliminating constraint - {number of blank boxes}


                    # doing the same thing for row constraints
                    row_constraint = self.matrix[i][j].row_constraint;
                    print "row_constraint " +str(row_constraint)
                    if row_constraint!=-1:
                        k=j+1;
                        row_list=[]
                        print "Traversing constraints in the same row"
                        while k<self.cols and (self.matrix[i][k].node_type!=NodeType.BLACK_NODE or self.matrix[i][k].node_type!=NodeType.CONSTRAINT_NODE):
                            row_list.append(self.matrix[i][k])
                            k=k+1
                        done_list=[]
                        for nd1 in row_list:
                            for nd2 in row_list:
                                if nd2.col_index not in done_list:
                                    if nd1.col_index!=nd2.col_index:
                                        nd1.adj_list.append((nd2.row_index,nd2.col_index))
                                        nd2.adj_list.append((nd1.row_index,nd1.col_index))
                            done_list.append(nd1.col_index)



    def print_constraint_graph(self):
        for i in range(0,self.rows):
            print "================"
            for j in range(0,self.cols):
                print self.matrix[i][j].adj_list


    def node_consistency(self):
        #going through the matrix looking for constraint nodes
        # if constraint node found, look for the next constraint node or black node
        for i in range(0,self.rows):
            for j in range(0,self.cols):

                if self.matrix[i][j].node_type==NodeType.CONSTRAINT_NODE:
                    print "Found constraint node"
                    print "i = "+ str(i)
                    print "j = "+str(j)
                    col_constraint= self.matrix[i][j].col_constraint;
                    #print col_constraint
                    if(col_constraint!=-1):
                        print "Reducing domain for cells in the same column"
                        # found a valid column constraint for this node
                        # search all rows greater than i till the next constraint node or black node and check
                        # for node consistency
                        k=i+1;
                        blankCount=0
                        while k<self.rows and (self.matrix[k][j].node_type!=NodeType.BLACK_NODE or self.matrix[k][j].node_type!=NodeType.CONSTRAINT_NODE):
                            blankCount=blankCount+1
                            #for key in  self.matrix[k][j].domain.keys():
                            #    if key>=col_constraint:
                            #        del self.matrix[k][j].domain[key]
                            k=k+1

                        # further reduce the domain by eliminating constraint - {number of blank boxes}

                        k=i+1;
                        if(blankCount>=1):
                            while k<self.rows and (self.matrix[k][j].node_type!=NodeType.BLACK_NODE or self.matrix[k][j].node_type!=NodeType.CONSTRAINT_NODE):
                                offset = blankCount*(blankCount-1)/2
                                print "offset= "+str(offset)
                                for key in  self.matrix[k][j].domain.keys():
                                    if key>col_constraint-offset:
                                        del self.matrix[k][j].domain[key]
                                k += 1
                    self.print_matrix()
                    # doing the same thing for row constraints
                    row_constraint = self.matrix[i][j].row_constraint;
                    print "row_constraint " +str(row_constraint)
                    if row_constraint!=-1:
                        k=j+1;
                        blankCount=0
                        while k<self.cols and (self.matrix[i][k].node_type!=NodeType.BLACK_NODE or self.matrix[i][k].node_type!=NodeType.CONSTRAINT_NODE):
                            blankCount+=1
                            #for key in self.matrix[i][k].domain.keys():
                             #   if key>col_constraint:
                              #      del self.matrix[k][j].domain[key]
                            k=k+1
                        print "Reducing domain for cells in the same row"
                        k=j+1;
                        if blankCount>0:
                            offset= blankCount*(blankCount-1)/2
                            print "offset= "+str(offset)
                            while k<self.cols and (self.matrix[i][k].node_type!=NodeType.BLACK_NODE or self.matrix[i][k].node_type!=NodeType.CONSTRAINT_NODE):
                                for key in self.matrix[i][k].domain.keys():
                                    if key>row_constraint-offset:
                                        del self.matrix[i][k].domain[key]
                                k=k+1
                        self.print_matrix()
                        print self.unsolvedCount

