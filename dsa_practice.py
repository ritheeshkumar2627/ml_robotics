def max_sum_submatrix(mat,k):
    m=len(mat)
    n=len(mat[0])
    arr = [[0] * (n + 1) for _ in range(m + 1)]
    max_sum=-float('inf')

    for i in range(1,m+1):
        for j in range(1,n+1):
            arr[i][j]=-arr[i-1][j-1]+arr[i-1][j]+arr[i][j-1]+mat[i-1][j-1]
    for i in range(k,m+1):
        for j in range(k,n+1):
            current_box_sum = arr[i][j] -arr[i-k][j] - arr[i][j-k] + arr[i-k][j-k]
            max_sum=max(max_sum,current_box_sum)
test=[[1,2,-1],[0,0,2]]

print(max_sum_submatrix(test,2))