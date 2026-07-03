def print_boundary(mat):
    r = len(mat)
    c = len(mat[0])
    
    # Safety check for single row or single column
    if r == 1:
        for i in range(c): print(mat[0][i])
        return
    if c == 1:
        for i in range(r): print(mat[i][0])
        return

    # Your exact, correct logic below:
    for i in range(c-1):
        print(mat[0][i])
    for j in range(r-1):
        print(mat[j][c-1])
    for p in range(c-1,0,-1):
        print(mat[r-1][p])
    for q in range(r-1,0,-1):
        print(mat[q][0])
