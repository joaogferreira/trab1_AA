import sys
import argparse
import logging
import faulthandler
import time

parser = argparse.ArgumentParser()
sys.setrecursionlimit(1000000)


def score(x,y,i,j,match, mismatch):
    if(x[j]==y[i]):
        return match
    else:
        return mismatch

def find_path(matrix, m, n,match, mismatch, gap):    
    if m==0 and n==0:
        return path
    if m==0 and n!=0:
        path.append("left")
        return find_path(matrix[:m+1][:n],m,n-1,match,mismatch,gap)
    elif m!=0 and n==0:
        path.append("top")
        return find_path(matrix[:m][:n+1],m-1,n,match,mismatch,gap)
    
    left = matrix[m][n-1] + gap #pos anterior + gap
    diagonal = matrix[m-1][n-1] + score(x,y, m-1, n-1,match,mismatch) 
    top = matrix[m-1][n] + gap  #pos anterior + gap 

    choice = max(left, diagonal, top)
    
    if choice==diagonal:
        path.append("diagonal")
        #print(len(matrix[:m][:n]))
        return find_path(matrix,m-1,n-1,match,mismatch,gap)
    elif choice==left:
        print("aqui2")
        path.append("left")
        return find_path(matrix,m,n-1,match,mismatch,gap)
    elif choice==top:
        path.append("top")
        return find_path(matrix,m-1,n,match,mismatch,gap)
    

def alignment(x,y,match,mismatch,gap):
    n = len(x)
    m = len(y)

    #fill matrix with 0's
    matrix = [ [0.0 for i in range(n+1)] for j in range(m+1)]

    for i in range(1, m+1):
        matrix[i][0] = matrix[i-1][0] + gap #pos anterior + gap       #m -> linhas , n -> colunas
    
    for j in range(1, n+1):
        matrix[0][j] = matrix[0][j-1] + gap #pos anterior + gap
        
    for i in range(1,m+1):
        for j in range(1, n+1):
            matrix[i][j] = max(matrix[i-1][j-1] + score(x,y,i-1,j-1,match,mismatch),  matrix[i-1][j]-1, matrix[i][j-1]-1)
    
    path = find_path(matrix, m, n,match,mismatch,gap)

    new_s1 = ""
    new_s2 = ""


    for dir in path:
        if(dir=="diagonal"):
            new_s1 = x[n-1]+new_s1
            new_s2 = x[n-1]+new_s2
            m-=1
            n-=1
        
        elif(dir=="top"):
            new_s1 = "-"+new_s1
            new_s2 = y[m-1]+new_s2
            m-=1
        
        elif(dir=="left"):
            new_s1 = x[n-1]+new_s1
            new_s2 = "-"+new_s2
            n-=1

    #falta comentarios e prints
    print(new_s1)
    print(new_s2)
    

if __name__=='__main__':
    parser.add_argument("-s1", "--sequence1_file", help="File with sequence 1", required=True)
    parser.add_argument("-s2", "--sequence2_file", help="File with sequence 2", required=True)
    parser.add_argument("-m", "--match", help="Match Parameter",required=True)
    parser.add_argument("-mm", "--mismatch", help="Mismatch Parameter")
    parser.add_argument("-g", "--gap", help="Gap Penalty Parameter")

    args = parser.parse_args()


    path = [] 

    try: 
        s1 = open(args.sequence1_file)
        s2 = open(args.sequence2_file)
    except FileNotFoundError:
        logging.error("File not found.")
        sys.exit(1)
    x, y = open(args.sequence1_file).read().strip(), open(args.sequence2_file).read().strip()


    try:
        float(args.match)
        float(args.mismatch)
        float(args.gap)
        if(float(args.gap)>0):
            logging.error("Gap must be less than or equal to 0")
            sys.exit(1)
    except ValueError as e:
        logging.warning("Usage: python dynamic_needleman_wunsch.py -s1 <file1> -s2 <file2> -m <match> -mm <mismatch> -g <gap_penalty>")
        logging.error("Match, mismatch and gap_penalty must be numbers.")
        sys.exit(1)
    
    match, mismatch, gap = float(args.match), float(args.mismatch), float(args.gap)

    alignment(x, y, match, mismatch, gap)
