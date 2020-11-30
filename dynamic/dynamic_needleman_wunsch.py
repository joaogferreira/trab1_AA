
def score(x,y,i,j):
    if(x[j]==y[i]):
        return 1 #match
    else:
        return -1 #mismatch

def find_path(matrix, m, n):
    if m==0 and n==0:
        return path
    if m==0 and n!=0:
        path.append("left")
        return find_path(matrix[:m+1][:n],m,n-1)
    elif m!=0 and n==0:
        path.append("top")
        return find_path(matrix[:m][:n+1],m-1,n)
    

    left = matrix[m][n-1] - 1 #pos anterior + gap
    diagonal = matrix[m-1][n-1] + score(x,y, m-1, n-1) 
    top = matrix[m-1][n] - 1  #pos anterior + gap 

    choice = max(left, diagonal, top)
    
    if choice==left:
        path.append("left")
        return find_path(matrix[:m+1][:n],m,n-1)
    elif choice==diagonal:
        path.append("diagonal")
        return find_path(matrix[:m][:n],m-1,n-1)
    elif choice==top:
        path.append("top")
        return find_path(matrix[:m][:n+1],m-1,n)
        


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


    path = find_path(matrix, m, n)[::-1]

    #print(path)

if __name__=='__main__':
    path = [] 

    #ler de um ficheiro
    x = 'gtat'
    y = 'tagg'

    alignment(x,y)
