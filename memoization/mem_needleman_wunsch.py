import sys
import argparse
import logging
import faulthandler
import time

parser = argparse.ArgumentParser()
sys.setrecursionlimit(1000000)

#Dictionary to save directions from each position of the matrix
directions = {}

def print_matrix(matrix):
    ''' 
    Prints the matrix 
    '''
    for i in matrix:
        print(i)

def build_matrix(n_rows, n_cols):
    ''' 
    Build matrix. All positions are equal to 0.0 
    '''
    matrix = [[0.0 for x in range(n_cols+1)] for x in range(n_rows+1)]
    return matrix


def fill_first_line(matrix,i,j):
    '''
    Fills first line of the matrix
    Position (0,0) is equal to 0.0 
    Positions (0,x) for x>=1 are equal to (0,x-1) + gap
    '''

    if(j<len(matrix[i])):

        if( i == 0 and j == 0):

            matrix[i][j]=0.0
            j+=1

            return fill_first_line(matrix,i,j)
        
        else:
            matrix[i][j] = matrix[i][j-1] + gap

            j+=1

            return fill_first_line(matrix,i,j)
    
    return matrix

def fill_first_col(matrix, i, j):
    '''
    Fills first column of the matrix
    Position (0,0) is equal to 0.0 
    Positions (0,x) for x>=1 are equal to (0,x-1) + gap
    '''

    if(i<len(matrix)):
        
        
        if(i==0 and j==0):
            matrix[i][j]=0.0
  
            i+=1

            return fill_first_col(matrix, i,j)
        
        else:
            matrix[i][j] = matrix[i-1][j] + gap
 
            i+=1

            return fill_first_col(matrix, i,j)
    
    return matrix

def get_top(matrix, i, j):
    '''
    Calculates top
    top is equal to the element above + gap 
    '''

    return matrix[i-1][j] + gap


def get_left(matrix, i,j):
    '''
    Calculates left
    left is equal to the element on the left + gap
    '''
    
    return matrix[i][j-1] + gap 

def get_diagonal(matrix, i, j,s1,s2):
    '''
    Calculates diagonal 
    if the char in position (current_line, 0) is equal to the char in position (0, current_column) 
    the diagonal is equal to the value in the position (current_line - 1, current_column - 1) + match
    Otherwise, the value of diagonal is equal to value in the position (current_line - 1, current_column - 1) + mismatch)
    '''
 
    col_char = s1[j-1]
    
    line_char = s2[i-1]

    if col_char==line_char:
        return matrix[i-1][j-1] + match
    else:
        return matrix[i-1][j-1] + mismatch


def fill_matrix(matrix,i, j,s1,s2):
    ''' 
    iterates over the matrix 
    the value to write in current position must be the greatest value between top, left and diagonal 
    '''

    
    if(i<len(matrix)):
        
        if(j<len(matrix[i])):

            matrix[i][j] = max(get_top(matrix,i,j), get_diagonal(matrix, i, j,s1,s2), get_left(matrix,i,j))
            
            '''
            Save the direction from each cell 
            Key : (i,j) 
            Value: "diagonal" / "left" / "top"
            '''
            if(matrix[i][j]==get_diagonal(matrix,i,j,s1,s2)):
                directions[str(i)+","+str(j)]="diagonal"
            elif(matrix[i][j]==get_left(matrix,i,j)):
                directions[str(i)+","+str(j)]="left"
            elif(matrix[i][j]==get_top(matrix,i,j)):
                directions[str(i)+","+str(j)]="top"
        
            j+=1
            
            return fill_matrix(matrix,i,j,s1,s2)
        
        else:
            i+=1
            j=1

            return fill_matrix(matrix,i,j,s1,s2)
    
    return matrix

def find_path(matrix, i, j, s1, new_s1, s2, new_s2, path):
    '''
    finds path
    starts at last position in the matrix 
    stops in position (0,0)
    '''
    
    if (i==0 and j==0):
        return new_s1, new_s2, path
    
    elif (i==0 and j!=0):
        path.append("left")
        
        new_s1 = s1[j-1] + new_s1
        
        new_s2 = "-" + new_s2
        
        j=j-1
        
        return find_path(matrix, i, j, s1, new_s1, s1, new_s2, path)
    
    elif (i!=0 and j==0):

        path.append("top")
        
        new_s1 = "-" + new_s1
        
        new_s2 = s2[i-1] + new_s2
        
        i=i-1
        
        return find_path(matrix, i, j, s1, new_s1, s2, new_s2, path)
    elif (i!=0 and j!=0):
        '''
        path available: top, left, diagonal
        the difference to recursive without memoization is that we don't need to calculate the values from diagonal, left and top again
        we get them from the dictionary that stored those values     
        '''
        direction = directions[str(i)+","+str(j)]

        if direction=="diagonal":

            path.append("diagonal")
     
            new_s1 = s1[j-1] + new_s1
            
            new_s2 = s2[i-1] + new_s2
            
            j=j-1
            
            i= i-1
            
            return find_path(matrix, i, j, s1, new_s1, s2, new_s2, path)
        
        elif direction=="left":
    
            path.append("left")
            
            new_s1 = s1[j-1] + new_s1
            
            new_s2 = "-" + new_s2
            
            j=j-1
            
            return find_path(matrix, i, j, s1, new_s1, s1, new_s2, path)

        elif direction=="top":
            path.append("top")
            
            new_s1 = "-" + new_s1
            
            new_s2 = s2[i-1] + new_s2
            
            i=i-1
            
            return find_path(matrix, i, j, s1, new_s1, s2, new_s2, path)
        
    return new_s1, new_s2, path


def main(s1, s2, match, mismatch, gap):
    start_time = time.time()

    s1,s2 = s1.read().strip(), s2.read().strip()

    matrix = build_matrix(len(s2), len(s1))

    fill_first_line(matrix,0,0)
    
    fill_first_col(matrix, 0,0)

   
    fill_matrix(matrix, 1, 1,s1,s2)

    print_matrix(matrix)
  
    new_s1, new_s2, path = find_path(matrix, len(matrix)-1, len(matrix[0])-1, s1, "", s2,  "", [])
    
    print("Aligned Sequences:")
    print("Sequence 1: "+new_s1)
    print("Sequence 2: "+new_s2)
    print("Path: "+path)
    print("Execution time: %s seconds" % (time.time() - start_time))
    print("Sequence 1 length: %s characters" % str(len(s1)))
    print("Sequence 2 length: %s characters" % str(len(s2)))
    
    
    
    
if __name__ == "__main__":
    parser.add_argument("-s1", "--sequence1_file", help="File with sequence 1", required=True)
    parser.add_argument("-s2", "--sequence2_file", help="File with sequence 2", required=True)
    parser.add_argument("-m", "--match", help="Match Parameter",required=True)
    parser.add_argument("-mm", "--mismatch", help="Mismatch Parameter")
    parser.add_argument("-g", "--gap", help="Gap Penalty Parameter")

    args = parser.parse_args()

    '''
    Verify if files exist
    '''
    try: 
        s1 = open(args.sequence1_file)
        s2 = open(args.sequence2_file)
    except FileNotFoundError:
        logging.error("File not found.")
        sys.exit(1)
    s1, s2 = open(args.sequence1_file), open(args.sequence2_file)
    
    '''
    Parameters : Match, Mismatch and Gap penalty
    '''
    try:
        float(args.match)
        float(args.mismatch)
        float(args.gap)
        if(float(args.gap)>0):
            logging.error("Gap must be less than or equal to 0")
            sys.exit(1)
    except ValueError as e:
        logging.warning("Usage: python rec_needleman_wunsch.py -s1 <file1> -s2 <file2> -m <match> -mm <mismatch> -g <gap_penalty>")
        logging.error("Match, mismatch and gap_penalty must be numbers.")
        sys.exit(1)
    
    match, mismatch, gap = float(args.match), float(args.mismatch), float(args.gap)
    
    main(s1,s2, match, mismatch, gap)
