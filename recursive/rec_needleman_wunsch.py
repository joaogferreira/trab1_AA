import sys
import argparse
import logging
import faulthandler
import time

parser = argparse.ArgumentParser()
sys.setrecursionlimit(1000000)


#OPERATIONS_COUNT=0

def print_matrix(matrix):
    for i in matrix:
        print(i)

#Falta incrementar as #OPERATIONS_COUNT 
#carina
def build_matrix(n_rows, n_cols):
    matrix = [[0.0 for x in range(n_cols+1)] for x in range(n_rows+1)]
    return matrix


def fill_first_line(matrix,i,j):
    #global #OPERATIONS_COUNT
    
    if(j<len(matrix[i])):
        
        #OPERATIONS_COUNT+=1
        
        if( i == 0 and j == 0):
            #OPERATIONS_COUNT += 1
            
            matrix[i][j]=0.0
            #OPERATIONS_COUNT +=1
            
            j+=1
            #OPERATIONS_COUNT+=1
            
            return fill_first_line(matrix,i,j)
        
        else:
            matrix[i][j] = matrix[i][j-1] + gap
            #OPERATIONS_COUNT+=1
            
            j+=1
            #OPERATIONS_COUNT+=1
            
            return fill_first_line(matrix,i,j)
    
    #OPERATIONS_COUNT+=1
    
    return matrix

def fill_first_col(matrix, i, j):
    #global #OPERATIONS_COUNT
    
    if(i<len(matrix)):
        
        #OPERATIONS_COUNT+=1
        
        if(i==0 and j==0):
            matrix[i][j]=0.0
            #OPERATIONS_COUNT+=1
            
            i+=1
            #OPERATIONS_COUNT+=1
            
            return fill_first_col(matrix, i,j)
        
        else:
            matrix[i][j] = matrix[i-1][j] + gap
            #OPERATIONS_COUNT+=1
            
            i+=1
            #OPERATIONS_COUNT+=1
            
            return fill_first_col(matrix, i,j)
    
    return matrix

def get_top(matrix, i, j):
    #global #OPERATIONS_COUNT
    
    #OPERATIONS_COUNT+=1
    
    return matrix[i-1][j] + gap


def get_left(matrix, i,j):
    #global #OPERATIONS_COUNT
    
    #OPERATIONS_COUNT+=1
    
    return matrix[i][j-1] + gap 

def get_diagonal(matrix, i, j,s1,s2):
    #global #OPERATIONS_COUNT
    
    col_char = s1[j-1]
    #OPERATIONS_COUNT+=1
    
    line_char = s2[i-1]
    #OPERATIONS_COUNT+=1

    if col_char==line_char:
        #OPERATIONS_COUNT+=1
        return matrix[i-1][j-1] + match
    else:
        #OPERATIONS_COUNT+=1
        return matrix[i-1][j-1] + mismatch


def fill_matrix(matrix,i, j,s1,s2):
    #global #OPERATIONS_COUNT
    
    if(i<len(matrix)):
        
        #OPERATIONS_COUNT+=1
        
        if(j<len(matrix[i])):
            #OPERATIONS_COUNT+=1
            
            matrix[i][j] = max(get_top(matrix,i,j), get_diagonal(matrix, i, j,s1,s2), get_left(matrix,i,j))
            #OPERATIONS_COUNT+=1
            
            j+=1
            #OPERATIONS_COUNT+=1
            
            return fill_matrix(matrix,i,j,s1,s2)
        
        else:
            i+=1
            #OPERATIONS_COUNT+=1
            
            j=1
            #OPERATIONS_COUNT+=1
            
            return fill_matrix(matrix,i,j,s1,s2)
    
    return matrix

def find_path(matrix, i, j, s1, new_s1, s2, new_s2, path):
    #global #OPERATIONS_COUNT
    
    if (i==0 and j==0):
        #OPERATIONS_COUNT+=1
        return new_s1, new_s2, path
    
    elif (i==0 and j!=0):
        left = get_left(matrix, i,j)
        #OPERATIONS_COUNT+=1
        
        path.append("left")
        #OPERATIONS_COUNT+=1
        
        new_s1 = s1[j-1] + new_s1
        #OPERATIONS_COUNT+=1
        
        new_s2 = "-" + new_s2
        #OPERATIONS_COUNT+=1
        
        j=j-1
        #OPERATIONS_COUNT+=1
        
        return find_path(matrix, i, j, s1, new_s1, s1, new_s2, path)
    
    elif (i!=0 and j==0):
        path.append("top")
        #OPERATIONS_COUNT+=1
        
        new_s1 = "-" + new_s1
        #OPERATIONS_COUNT+=1
        
        new_s2 = s2[i-1] + new_s2
        #OPERATIONS_COUNT+=1
        
        i=i-1
        #OPERATIONS_COUNT+=1
        
        return find_path(matrix, i, j, s1, new_s1, s2, new_s2, path)
    elif (i!=0 and j!=0):
        top = get_top(matrix, i, j)
        #OPERATIONS_COUNT+=1
        
        left = get_left(matrix, i, j)
        #OPERATIONS_COUNT+=1
        
        diagonal = get_diagonal(matrix, i, j,s1,s2)
        #OPERATIONS_COUNT+=1
        
        max_value = max(top, left, diagonal)
        #OPERATIONS_COUNT+=1

        if max_value==diagonal:
            #OPERATIONS_COUNT+=1
            
            path.append("diagonal")
            #OPERATIONS_COUNT+=1
            
            new_s1 = s1[j-1] + new_s1
            #OPERATIONS_COUNT+=1
            
            new_s2 = s2[i-1] + new_s2
            #OPERATIONS_COUNT+=1
            
            j=j-1
            #OPERATIONS_COUNT+=1
            
            i= i-1
            #OPERATIONS_COUNT+=1 
            
            return find_path(matrix, i, j, s1, new_s1, s2, new_s2, path)
        
        elif max_value==left:
            #OPERATIONS_COUNT+=1
            
            path.append("left")
            #OPERATIONS_COUNT+=1
            
            new_s1 = s1[j-1] + new_s1
            #OPERATIONS_COUNT+=1
            
            new_s2 = "-" + new_s2
            #OPERATIONS_COUNT+=1
            
            j=j-1
            #OPERATIONS_COUNT+=1
            
            return find_path(matrix, i, j, s1, new_s1, s1, new_s2, path)

        elif max_value==top:
            #OPERATIONS_COUNT+=1
            path.append("top")
            
            #OPERATIONS_COUNT+=1
            new_s1 = "-" + new_s1
            
            #OPERATIONS_COUNT+=1
            new_s2 = s2[i-1] + new_s2
            
            #OPERATIONS_COUNT+=1
            i=i-1
            
            #OPERATIONS_COUNT+=1
            
            return find_path(matrix, i, j, s1, new_s1, s2, new_s2, path)
        
    return new_s1, new_s2, path


def main(s1, s2, match, mismatch, gap):
    start_time = time.time()

    #global #OPERATIONS_COUNT
    
    s1,s2 = s1.read().strip(), s2.read().strip()
    #OPERATIONS_COUNT+=2
    
    matrix = build_matrix(len(s2), len(s1))
    #OPERATIONS_COUNT+=1
    
    fill_first_line(matrix,0,0)
    #OPERATIONS_COUNT+=1
    
    fill_first_col(matrix, 0,0)
    #OPERATIONS_COUNT+=1
    
    fill_matrix(matrix, 1, 1,s1,s2)
    #OPERATIONS_COUNT+=1

    #print_matrix(matrix)

    new_s1, new_s2, path = find_path(matrix, len(matrix)-1, len(matrix[0])-1, s1, "", s2,  "", [])
    #OPERATIONS_COUNT+=1


    print("Sequências alinhadas:")
    print("Sequência 1: "+new_s1)
    print("Sequência 2: "+new_s2)
    
    #print(path)
    #print("Número de operações: "+str(OPERATIONS_COUNT))
    
    print("Tempo de execução: %s segundos" % (time.time() - start_time))
    print("Tamanho s1: "+str(len(s1)))
    print("Tamanho s2: "+str(len(s2)))
    
    
    
    
if __name__ == "__main__":
    parser.add_argument("-s1", "--sequence1", help="File with sequence 1", required=True)
    parser.add_argument("-s2", "--sequence2", help="File with sequence 2", required=True)
    parser.add_argument("-m", "--match", help="Match Parameter",required=True)
    parser.add_argument("-mm", "--mismatch", help="Mismatch Parameter")
    parser.add_argument("-g", "--gap", help="Gap Penalty Parameter")

    args = parser.parse_args()

    '''
    Verify if files exist
    '''
    try: 
        s1 = open(args.sequence1)
        s2 = open(args.sequence2)
    except FileNotFoundError:
        logging.error("File not found.")
        sys.exit(1)
    s1, s2 = open(args.sequence1), open(args.sequence2)
    
    '''
    Parameters : Match, Mismatch and Gap penalty
    '''
    try:
        float(args.match)
        float(args.mismatch)
        float(args.gap)
    except ValueError as e:
        logging.warning("Usage: python rec_needleman_wunsch.py -s1 <file1> -s2 <file2> -m <match> -mm <mismatch> -g <gap_penalty>")
        logging.error("Match, mismatch and gap_penalty must be numbers.")
        sys.exit(1)
    match, mismatch, gap = float(args.match), float(args.mismatch), float(args.gap)
    
    main(s1,s2, match, mismatch, gap)