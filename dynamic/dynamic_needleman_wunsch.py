
def score(x,y,i,j):
    if(x[j]==y[i]):
        return 1 #match
    else:
        return -1 #mismatch

def find_path(matrix, m, n):
    pass

def alignment(x,y):
    n = len(x)
    m = len(y)

    #fill matrix with 0's
    matrix = [ [0 for i in range(n+1)] for j in range(m+1)]

    for i in range(1, m+1):
        matrix[i][0] = matrix[i-1][0] - 1 #pos anterior + gap 

    for j in range(1, n+1):
        matrix[0][j] = matrix[0][j-1] - 1 #pos anterior + gap
    
        for i in range(1,m+1):
            for j in range(1, n+1):
                matrix[i][j] = max(matrix[i-1][j-1] + score(x,y,i-1,j-1),  matrix[i-1][j]-1, matrix[i][j-1]-1) #diagonal (align), top (delete), left (insert)

    for line in matrix:
        print(line)
if __name__=='__main__':
    #ler de um ficheiro
    x = 'gtat'
    y = 'tagg'

    alignment(x,y)
