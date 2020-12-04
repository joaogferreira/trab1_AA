import sys
import argparse
import logging
import faulthandler
import time
import writeRec

parser = argparse.ArgumentParser()
sys.setrecursionlimit(1000000)


OPERATIONS_COUNT=0

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
    
    global OPERATIONS_COUNT
    
    if(j<len(matrix[i])):
        
        OPERATIONS_COUNT+=1
        
        if( i == 0 and j == 0):
            OPERATIONS_COUNT += 1
            
            matrix[i][j]=0.0
            OPERATIONS_COUNT +=1
            
            j+=1
            OPERATIONS_COUNT+=1
            
            return fill_first_line(matrix,i,j)
        
        else:
            matrix[i][j] = matrix[i][j-1] + gap
            OPERATIONS_COUNT+=1
            
            j+=1
            OPERATIONS_COUNT+=1
            
            return fill_first_line(matrix,i,j)
    
    OPERATIONS_COUNT+=1
    
    return matrix

def fill_first_col(matrix, i, j):
    '''
    Fills first column of the matrix
    Position (0,0) is equal to 0.0 
    Positions (0,x) for x>=1 are equal to (0,x-1) + gap
    '''

    global OPERATIONS_COUNT
    
    if(i<len(matrix)):
        
        OPERATIONS_COUNT+=1
        
        if(i==0 and j==0):
            matrix[i][j]=0.0
            OPERATIONS_COUNT+=1
            
            i+=1
            OPERATIONS_COUNT+=1
            
            return fill_first_col(matrix, i,j)
        
        else:
            matrix[i][j] = matrix[i-1][j] + gap
            OPERATIONS_COUNT+=1
            
            i+=1
            OPERATIONS_COUNT+=1
            
            return fill_first_col(matrix, i,j)
    
    return matrix

def get_top(matrix, i, j):
    '''
    Calculates top
    top is equal to the element above + gap 
    '''

    global OPERATIONS_COUNT
    
    OPERATIONS_COUNT+=1
    
    return matrix[i-1][j] + gap


def get_left(matrix, i,j):
    '''
    Calculates left
    left is equal to the element on the left + gap
    '''
    global OPERATIONS_COUNT
    
    OPERATIONS_COUNT+=1
    
    return matrix[i][j-1] + gap 

def get_diagonal(matrix, i, j,s1,s2):
    '''
    Calculates diagonal 
    if the char in position (current_line, 0) is equal to the char in position (0, current_column) 
    the diagonal is equal to the value in the position (current_line - 1, current_column - 1) + match
    Otherwise, the value of diagonal is equal to value in the position (current_line - 1, current_column - 1) + mismatch)
    '''

    global OPERATIONS_COUNT
    
    col_char = s1[j-1]
    OPERATIONS_COUNT+=1
    
    line_char = s2[i-1]
    OPERATIONS_COUNT+=1

    if col_char==line_char:
        OPERATIONS_COUNT+=1
        return matrix[i-1][j-1] + match
    else:
        OPERATIONS_COUNT+=1
        return matrix[i-1][j-1] + mismatch


def fill_matrix(matrix,i, j,s1,s2):
    ''' 
    iterates over the matrix 
    the value to write in current position must be the greatest value between top, left and diagonal 
    '''

    global OPERATIONS_COUNT
    
    
    if(i<len(matrix)):
        OPERATIONS_COUNT+=1
        
        if(j<len(matrix[i])):
            OPERATIONS_COUNT+=1

            matrix[i][j] = max(get_top(matrix,i,j), get_diagonal(matrix, i, j,s1,s2), get_left(matrix,i,j))
            OPERATIONS_COUNT+=1
            
            j+=1
            OPERATIONS_COUNT+=1
            
            return fill_matrix(matrix,i,j,s1,s2)
        
        else:
            i+=1
            OPERATIONS_COUNT+=1
            
            j=1
            OPERATIONS_COUNT+=1
            
            return fill_matrix(matrix,i,j,s1,s2)
    
    return matrix

def find_path(matrix, i, j, s1, new_s1, s2, new_s2, path):
    '''
    finds path
    starts at last position in the matrix 
    stops in position (0,0)
    '''

    global OPERATIONS_COUNT
    
    if (i==0 and j==0):
        OPERATIONS_COUNT+=1
        return new_s1, new_s2, path
    
    elif (i==0 and j!=0):
        #the only path available goes to left position, so we know it came from left (first line)
        
        path.append("left")
        OPERATIONS_COUNT+=1
        
        new_s1 = s1[j-1] + new_s1
        OPERATIONS_COUNT+=1
        
        new_s2 = "-" + new_s2
        OPERATIONS_COUNT+=1
        
        j=j-1
        OPERATIONS_COUNT+=1
        
        return find_path(matrix, i, j, s1, new_s1, s1, new_s2, path)
    
    elif (i!=0 and j==0):
        #the only path available goes to top position, so we know it came from top (first column) 

        path.append("top")
        OPERATIONS_COUNT+=1
        
        new_s1 = "-" + new_s1
        OPERATIONS_COUNT+=1
        
        new_s2 = s2[i-1] + new_s2
        OPERATIONS_COUNT+=1
        
        i=i-1
        OPERATIONS_COUNT+=1
        
        return find_path(matrix, i, j, s1, new_s1, s2, new_s2, path)
    elif (i!=0 and j!=0):
        '''
        path available: top, left, diagonal
        we need to calculate all 3 values and the greatest is where it came from        
        '''
        top = get_top(matrix, i, j)
        OPERATIONS_COUNT+=1
        
        left = get_left(matrix, i, j)
        OPERATIONS_COUNT+=1
        
        diagonal = get_diagonal(matrix, i, j,s1,s2)
        OPERATIONS_COUNT+=1
        
        max_value = max(top, left, diagonal)
        OPERATIONS_COUNT+=1

        if max_value==diagonal:
            OPERATIONS_COUNT+=1

            path.append("diagonal")
            OPERATIONS_COUNT+=1
            
            new_s1 = s1[j-1] + new_s1
            OPERATIONS_COUNT+=1
            
            new_s2 = s2[i-1] + new_s2
            OPERATIONS_COUNT+=1
            
            j=j-1
            OPERATIONS_COUNT+=1
            
            i= i-1
            OPERATIONS_COUNT+=1 
            
            return find_path(matrix, i, j, s1, new_s1, s2, new_s2, path)
        
        elif max_value==left:
            OPERATIONS_COUNT+=1
            
            path.append("left")
            OPERATIONS_COUNT+=1
            
            new_s1 = s1[j-1] + new_s1
            OPERATIONS_COUNT+=1
            
            new_s2 = "-" + new_s2
            OPERATIONS_COUNT+=1
            
            j=j-1
            OPERATIONS_COUNT+=1
            
            return find_path(matrix, i, j, s1, new_s1, s1, new_s2, path)

        elif max_value==top:
            OPERATIONS_COUNT+=1
            path.append("top")
            
            OPERATIONS_COUNT+=1
            new_s1 = "-" + new_s1
            
            OPERATIONS_COUNT+=1
            new_s2 = s2[i-1] + new_s2
            
            OPERATIONS_COUNT+=1
            i=i-1
            
            OPERATIONS_COUNT+=1
            
            return find_path(matrix, i, j, s1, new_s1, s2, new_s2, path)
        
    return new_s1, new_s2, path


def main(s1, s2, match, mismatch, gap):
    start_time = time.time()

    global OPERATIONS_COUNT
    
    s1,s2 = s1.read().strip(), s2.read().strip()
    OPERATIONS_COUNT+=2
    
    matrix = build_matrix(len(s2), len(s1))
    OPERATIONS_COUNT+=1
    

    fill_first_line(matrix,0,0)
    OPERATIONS_COUNT+=1
    
    fill_first_col(matrix, 0,0)
    OPERATIONS_COUNT+=1

    fill_matrix(matrix, 1, 1,s1,s2)
    OPERATIONS_COUNT+=1
    
    new_s1, new_s2, path = find_path(matrix, len(matrix)-1, len(matrix[0])-1, s1, "", s2,  "", [])
    OPERATIONS_COUNT+=1

    print("Sequências alinhadas: ")
    print("Sequência 1: "+new_s1)
    print("Sequência 2: "+new_s2)
    print("Path: "+str(path))
    print("Operations count: "+str(OPERATIONS_COUNT))
    end = time.time()-start_time
    print("Execution time: %s seconds" % (end))
    print("Sequence 1 length: %s characters" % str(len(s1)))
    print("Sequence 2 length: %s characters" % str(len(s2)))

    writeRec.write(args.sequence1_file,args.sequence2_file,OPERATIONS_COUNT,end)

    
    
    
    
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
