def reverse_transpose(mat):
    n=len(mat)
    if n== len(mat[0]):
        for i in range(n):
            for j in range(i+1,n):
                mat[i][j],mat[j][i]=mat[j][i],mat[i][j]

         
    
                # Clean, unified row-reversal step (Works for both odd and even N)
        for num in range(n // 2):
            # Swap top rows with bottom rows simultaneously to prevent overwriting
            mat[num], mat[n - 1 - num] = mat[n - 1 - num], mat[num]

    return mat

matrix=[[1,2,3],[4,5,6],[7,8,9]]

print(reverse_transpose(matrix))

