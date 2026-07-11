def rotate_asymmetrical(mat):
    m=len(mat)
    n=len(mat[0])
    rotated = [[0] * m for _ in range(n)]
    for j in range(n):
        for i in range(m):
            rotated[j][i]=mat[m-1-i][j]
    print(rotated)
test=[[1,2,3],[4,5,6]]
rotate_asymmetrical(test)