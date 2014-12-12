__author__ = 'prateek'
from node import Node
from node import NodeType
import copy

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
        """
        This method is for formulating the problem. Follows the following steps
        1) Enforce node consistency
        2) Creates a Constraint Graph
        3) Solves the Formed Graph by Backtrack search with Forward Checking and Constraint propagation
        """
        print "Starting problem formulation"
        self.print_matrix()
        self.node_consistency()
        #self.init_unsolved()
        self.create_constraint_graph()
        #self.print_constraint_graph()
        self.solve()
        self.print_matrix()

        # formulate the problem and add data structures which might help solve the problem
        # instrument the matrix to populate the data structures

    def solve(self):
        # The Algorithm goes here
        print "Solving KAKURO"

        #self.DFS(self.matrix[0][0])
        self.BackTrackingSearch(self.getNextMostConstrainedVar())

    def check_constraint_violated(self,node):
        """
        Method for forward checking during backtrack search
        :param node:
        :return: True if any constraint is violated, False if no constraint violated
        """
        """
        :param node:
        :return:
        """
        rowViolated=False
        colViolated=False

        #checking if column constraint is violated
        sum=0
        constraintValue=-1
        if node.top_constraint_coord!=None:
            i,j = node.top_constraint_coord
            constraintValue= self.matrix[i][j].col_constraint
            k=i+1
            unassignedFound= False
            while k<self.rows and (self.matrix[k][j].node_type!=NodeType.BLACK_NODE and self.matrix[k][j].node_type!=NodeType.CONSTRAINT_NODE):
                if self.matrix[k][j].node_value==0:
                    unassignedFound=True
                sum+=self.matrix[k][j].node_value
                k+=1
            if unassignedFound==False and sum!=constraintValue:
                rowViolated=True
        #checking if row constraint is violated
        sum=0
        if node.left_constraint_coord!=None:
            i,j = node.left_constraint_coord
            constraintValue= self.matrix[i][j].row_constraint
            k=j+1
            unassignedFound=False
            sum=0
            while k<self.cols and (self.matrix[i][k].node_type!=NodeType.BLACK_NODE and self.matrix[i][k].node_type!=NodeType.CONSTRAINT_NODE):
                if self.matrix[i][k].node_value==0:
                    unassignedFound=True
                sum+=self.matrix[i][k].node_value
                k+=1
            if unassignedFound==False and sum!=constraintValue:
                colViolated=True

        return rowViolated or colViolated

    def getNextLeastConstrainedVar(self,node):
        i= node.row_index
        j= node.col_index
        #placeholder for the least constrainted variable
        if j+1<self.cols:
            return self.matrix[i][j+1]
        else:
            if i+1<self.rows:
                return self.matrix[i+1][0]
            else:
                return None

    def getNextMostConstrainedVar(self):
        print "Entering the most constrained variable"
        mini=-1
        minj=-1
        minVal = 1000
        found= False
        for i in range(0,self.rows):
            for j in range(0,self.cols):
               if self.matrix[i][j].node_type==NodeType.VALUE_NODE and self.matrix[i][j].visited==False:
                    found = True
                    if len(self.matrix[i][j].domain)<minVal:
                        mini = i
                        minj =j
                        minVal = len(self.matrix[i][j].domain)
        if found==True:
            return self.matrix[mini][minj]
        else:
            return None




    def DFS(self,node):
                while node.node_type!=NodeType.VALUE_NODE:
                    node = self.getNextLeastConstrainedVar(node)
                    #node = self.getNextMostConstrainedVar()
                node.visited=True
                works = False
                #print "selected for DFS"
                #print "i= "+str(node.row_index)
                #print "j="+str(node.col_index)
                domainCopy = copy.deepcopy(node.domain)
                for i in domainCopy:
                    if i not in node.domain:
                        continue
                    #if node.row_index==1 and node.col_index==2 and i==3:
                    #    print "hello"
                    hash={}
                    #hashVal={}
                    print "selected for DFS i="+str(node.row_index)+" j="+str(node.col_index)
                    print "Assigning domain value as "+str(i)
                    print "Domain", node.domain
                    node.node_value=i
                    #backing up all domains of adj list in hash
                    #backup the values also
                    for a,b in node.adj_list:
                        hash[(a*self.rows)+b]= copy.deepcopy(self.matrix[a][b].domain)
                    for a,b in node.adj_list:
                        print "a="+str(a)+" b="+str(b)
                        print self.matrix[a][b].domain
                        #self.matrix[a][b].domain=hash[(a*self.rows)+b]
                        if i in self.matrix[a][b].domain:
                            del self.matrix[a][b].domain[i]
                        print self.matrix[a][b].domain
                    # Need to do the following here
                    # Take a backup of all domains of nodes in adjacency list of this node
                    # Reduce domain of all adjacent nodes according to this assignment

                    if self.check_constraint_violated(node)==True:
                        print "Constraint violated"
                        node.node_value=0
                        for a,b in node.adj_list:
                            print "Restoring domain for a="+str(a)+" b="+str(b)
                            print self.matrix[a][b].domain
                            self.matrix[a][b].domain=hash[(a*self.rows)+b]
                            print self.matrix[a][b].domain
                        works = False
                        continue
                    else:
                        print "Constraint not violated"
                        nextNode= self.getNextLeastConstrainedVar(node)
                        #nextNode = self.getNextMostConstrainedVar()
                        if nextNode == None:
                            return True
                        while(nextNode.node_type!=NodeType.VALUE_NODE):
                            nextNode= self.getNextLeastConstrainedVar(nextNode)
                            #nextNode = self.getNextMostConstrainedVar()
                        if self.DFS(nextNode)==True:
                            works = True
                            return True
                        else:
                            node.node_value=0
                            for a,b in node.adj_list:
                                print "DFS failed Restoring domain for a="+str(a)+" b="+str(b)
                                print self.matrix[a][b].domain
                                self.matrix[a][b].domain=hash[(a*self.rows)+b]
                                #self.matrix[a][b].node_value=0
                                print self.matrix[a][b].domain
                            works = False
                            node.node_value=0

                if works==False:
                    node.visited=False
                return works

    def BackTrackingSearch(self,node):
                #while node.node_type!=NodeType.VALUE_NODE:
                    #node = self.getNextLeastConstrainedVar(node)
                #node = self.getNextMostConstrainedVar()
                node.visited=True
                works = False
                #print "selected for DFS"
                #print "i= "+str(node.row_index)
                #print "j="+str(node.col_index)
                domainCopy = copy.deepcopy(node.domain)
                for i in domainCopy:
                    if i not in node.domain:
                        continue
                    #if node.row_index==1 and node.col_index==2 and i==3:
                    #    print "hello"
                    hash={}
                    #hashVal={}
                    print "selected for DFS i="+str(node.row_index)+" j="+str(node.col_index)
                    print "Assigning domain value as "+str(i)
                    print "Domain", node.domain
                    node.node_value=i
                    #backing up all domains of adj list in hash
                    #backup the values also
                    for a,b in node.adj_list:
                        hash[(a*self.rows)+b]= copy.deepcopy(self.matrix[a][b].domain)
                    for a,b in node.adj_list:
                        print "a="+str(a)+" b="+str(b)
                        print self.matrix[a][b].domain
                        #self.matrix[a][b].domain=hash[(a*self.rows)+b]
                        if i in self.matrix[a][b].domain:
                            del self.matrix[a][b].domain[i]
                        print self.matrix[a][b].domain
                    # Need to do the following here
                    # Take a backup of all domains of nodes in adjacency list of this node
                    # Reduce domain of all adjacent nodes according to this assignment

                    if self.check_constraint_violated(node)==True:
                        print "Constraint violated"
                        node.node_value=0
                        for a,b in node.adj_list:
                            print "Restoring domain for a="+str(a)+" b="+str(b)
                            print self.matrix[a][b].domain
                            self.matrix[a][b].domain=hash[(a*self.rows)+b]
                            print self.matrix[a][b].domain
                        works = False
                        continue
                    else:
                        print "Constraint not violated"
                        #nextNode= self.getNextLeastConstrainedVar(node)
                        nextNode = self.getNextMostConstrainedVar()
                        if nextNode == None:
                            return True
                        while(nextNode.node_type!=NodeType.VALUE_NODE):
                            #nextNode= self.getNextLeastConstrainedVar(nextNode)
                            nextNode = self.getNextMostConstrainedVar()
                        if self.BackTrackingSearch(nextNode)==True:
                            works = True
                            return True
                        else:
                            node.node_value=0
                            for a,b in node.adj_list:
                                print "DFS failed Restoring domain for a="+str(a)+" b="+str(b)
                                print self.matrix[a][b].domain
                                self.matrix[a][b].domain=hash[(a*self.rows)+b]
                                #self.matrix[a][b].node_value=0
                                print self.matrix[a][b].domain
                            works = False
                            node.node_value=0

                if works==False:
                    node.visited=False
                return works










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
                        #print "Traversing constraints in the same column"
                        # found a valid column constraint for this node
                        # search all rows greater than i till the next constraint node or black node

                        k=i+1;
                        while k<self.rows and self.matrix[k][j].node_type!=NodeType.BLACK_NODE and self.matrix[k][j].node_type!=NodeType.CONSTRAINT_NODE:
                            self.matrix[k][j].top_constraint_coord = (i,j)
                            col_list.append(self.matrix[k][j])
                            k=k+1
                        done_list=[]
                        for nd1 in col_list:
                            #nd1.adj_list.append((-1,i,j))
                            for nd2 in col_list:
                                if nd2.row_index not in done_list:
                                    if nd1.row_index!=nd2.row_index:
                                        nd1.adj_list.append((nd2.row_index,nd2.col_index))
                                        nd2.adj_list.append((nd1.row_index,nd1.col_index))
                            done_list.append(nd1.row_index)
                        # further reduce the domain by eliminating constraint - {number of blank boxes}


                    # doing the same thing for row constraints
                    row_constraint = self.matrix[i][j].row_constraint;
                    #print "row_constraint " +str(row_constraint)
                    if row_constraint!=-1:
                        k=j+1;
                        row_list=[]
                        #print "Traversing constraints in the same row"
                        while k<self.cols and (self.matrix[i][k].node_type!=NodeType.BLACK_NODE and self.matrix[i][k].node_type!=NodeType.CONSTRAINT_NODE):
                            self.matrix[i][k].left_constraint_coord=(i,j)
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
                if self.matrix[i][j].node_type==NodeType.VALUE_NODE:
                    print "lef constraint==>"+str(self.matrix[i][j].left_constraint_coord)
                    print "top constraint==>"+str(self.matrix[i][j].top_constraint_coord)
                print "--------------"


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
                        while k<self.rows and (self.matrix[k][j].node_type!=NodeType.BLACK_NODE and self.matrix[k][j].node_type!=NodeType.CONSTRAINT_NODE):
                            blankCount=blankCount+1
                            #for key in  self.matrix[k][j].domain.keys():
                            #    if key>=col_constraint:
                            #        del self.matrix[k][j].domain[key]
                            k=k+1

                        # further reduce the domain by eliminating constraint - {n(n-1)/2}
                        # and constraint -{(n-1)(20-n)/2}

                        k=i+1;
                        if(blankCount>=1):
                            while k<self.rows and (self.matrix[k][j].node_type!=NodeType.BLACK_NODE and self.matrix[k][j].node_type!=NodeType.CONSTRAINT_NODE):
                                offset = blankCount*(blankCount-1)/2
                                offset2 = ((blankCount-1)*(20-blankCount))/2
                                print "offset= "+str(offset)
                                for key in  self.matrix[k][j].domain.keys():
                                    if key>col_constraint-offset or key<col_constraint-offset2:
                                        del self.matrix[k][j].domain[key]
                                k += 1
                    self.print_matrix()
                    # doing the same thing for row constraints
                    row_constraint = self.matrix[i][j].row_constraint;
                    print "row_constraint " +str(row_constraint)
                    if row_constraint!=-1:
                        k=j+1;
                        blankCount=0
                        while k<self.cols and (self.matrix[i][k].node_type!=NodeType.BLACK_NODE and self.matrix[i][k].node_type!=NodeType.CONSTRAINT_NODE):
                            blankCount+=1
                            #for key in self.matrix[i][k].domain.keys():
                             #   if key>col_constraint:
                              #      del self.matrix[k][j].domain[key]
                            k=k+1
                        print "Reducing domain for cells in the same row"
                        k=j+1;
                        if blankCount>0:
                            offset= blankCount*(blankCount-1)/2
                            offset2 = ((blankCount-1)*(20-blankCount))/2
                            print "offset= "+str(offset)
                            while k<self.cols and (self.matrix[i][k].node_type!=NodeType.BLACK_NODE and self.matrix[i][k].node_type!=NodeType.CONSTRAINT_NODE):
                                for key in self.matrix[i][k].domain.keys():
                                    if key>row_constraint-offset or key<row_constraint-offset2:
                                        del self.matrix[i][k].domain[key]
                                k=k+1
                        self.print_matrix()
                        print self.unsolvedCount

