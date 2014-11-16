__author__ = 'prateek'

class Game:
    matrix = [[]]
    rows =0
    cols =0
    def __init__(self,matrix,row_count,column_count):
        self.matrix = matrix
        self.rows=row_count
        self.cols = column_count

    def formulize(self):
        print "Starting problem formulation"
        # formulate the problem and add data structures which might help solve the problem
        # instrument the matrix to populate the data structures

    def solve(self):
        # The Algorithm goes here
        print "Solving the KAKURO"

    def print_matrix(self):
        for i in range(0,self.rows):
            for j in range(0,self.cols):
                print self.matrix[i][j]