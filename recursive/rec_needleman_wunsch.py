import sys
import argparse
import logging
parser = argparse.ArgumentParser()

def print_matrix(matrix):
    for i in matrix:
        print(i)

def build_matrix(n_rows, n_cols):
    matrix = [[0.0 for x in range(n_cols+2)] for x in range(n_rows+2)]
    return matrix

#line
def first_line_letter_to_matrix(matrix, i, j,s1,s2):
    if(j<len(matrix[i])):
        if(i==0 and j==0):
            matrix[i][j]="-"
            j+=1
            return first_line_letter_to_matrix(matrix,i,j,s1,s2)
        elif(j==1):
            matrix[i][j]="-"
            j+=1
            return first_line_letter_to_matrix(matrix,i,j,s1,s2)
        else:
            matrix[i][j] = s1[j-2]
            j+=1
            return first_line_letter_to_matrix(matrix,i,j,s1,s2)
    return matrix

#col 
def first_col_letter_to_matrix(matrix, i, j, s1, s2):
    if(i<len(matrix)):
        if(i==0 and j==0):
            matrix[i][j]="-"
            i+=1
            return first_col_letter_to_matrix(matrix,i,j,s1,s2)
        elif(i==1):
            matrix[i][j]="-"
            i+=1
            return first_col_letter_to_matrix(matrix,i,j,s1,s2)
        else:
            matrix[i][j] = s2[i-2]
            i+=1
            return first_col_letter_to_matrix(matrix,i,j,s1,s2)
    return matrix

def fill_first_line(matrix,i,j):
    if(j<len(matrix[i])):
        if(i==1 and j==1):
            matrix[i][j]=0.0
            j+=1
            return fill_first_line(matrix,i,j)
        else:
            matrix[i][j] = matrix[i][j-1] + gap
            j+=1
            return fill_first_line(matrix,i,j)
    return matrix

def fill_first_col(matrix, i, j):
    if(i<len(matrix)):
        if(i==1 and j==1):
            matrix[i][j]=0.0
            i+=1 
            return fill_first_col(matrix, i,j)
        else:
            matrix[i][j] = matrix[i-1][j] + gap 
            i+=1
            return fill_first_col(matrix, i,j)
    return matrix

def get_top(matrix, i, j):
    return matrix[i-1][j] + gap

def get_left(matrix, i,j):
    return matrix[i][j-1] + gap 

def get_diagonal(matrix, i, j):
    col_char = matrix[0][j]
    line_char = matrix[i][0]

    if col_char==line_char:
        return matrix[i-1][j-1] + match
    else:
        return matrix[i-1][j-1] + mismatch

#
# preencher restantes linhas
# ainda nao tou a chamar 
def fill_matrix(matrix,i, j):
    #i -> linha
    #j -> coluna
    if(i<len(matrix)):
        if(j<len(matrix[i])):
            matrix[i][j] = max(get_top(matrix,i,j), get_diagonal(matrix, i, j), get_left(matrix,i,j))
            j+=1
            return fill_matrix(matrix,i,j)
        else:
            i+=1
            j=2
            return fill_matrix(matrix,i,j)
    
    return matrix

def find_path(matrix, i, j, new_s1, new_s2, path):
    #para na posicao (1,1)
    if (i==1 and j==1):
        return new_s1, new_s2, path
    else:
        top = get_top(matrix, i, j)
        left = get_left(matrix, i, j)
        diagonal = get_diagonal(matrix, i, j)
        max_value = max(top, left, diagonal)
        if max_value==top:
            print("top")
            path.append("top")
            new_s1 = "-" + new_s1
            new_s2 = matrix[i][0] + new_s2
            i=i-1
            find_path(matrix, i, j, new_s1, new_s2, path)
        elif max_value==left:
            print("left")
            path.append("left")
            new_s1 = matrix[0][j] + new_s1
            new_s2 = "-" + new_s2
            j=j-1
            find_path(matrix, i, j, new_s1, new_s2, path)
        elif max_value==diagonal:
            print("diagonal")
            path.append("diagonal")
            new_s1 = matrix[0][j] + new_s1
            new_s2 = matrix[0][j] + new_s2
            j=j-1
            i= i-1 
            find_path(matrix, i, j, new_s1, new_s2, path)

    return new_s1, new_s2, path


def main(s1, s2, match, mismatch, gap):
    s1,s2 = s1.read().strip(), s2.read().strip()
    
    matrix = build_matrix(len(s2), len(s1))
    
    first_line_letter_to_matrix(matrix,0,0,s1,s2)
    first_col_letter_to_matrix(matrix, 0,0, s1,s2)
    
    fill_first_line(matrix,1,1)
    fill_first_col(matrix, 1,1)
    
    fill_matrix(matrix, 2, 2) #queremos começar na posicao (2,2), as duas primeiras linhas e colunas ja tao cheias

    
    
    #print_matrix(matrix)

    #path vai desde o ultimo elemento ate ao 1,1
    #len -1 para começar na ultima posicao 
    new_s1, new_s2, path = find_path(matrix, len(matrix)-1, len(matrix[0])-1, "", "", [])

    print(new_s1)
    print(new_s2)

    
    
    
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