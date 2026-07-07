def max_sub_square_ones(mat):
    m=len(mat)
    n=len(mat[0])
    dp = [[0] * n for _ in range(m)]
    max_side=0
    for i in range(m):
        for j in range(n):
            if i==0 or j==0:
                dp[i][j]=mat[i][j]
            elif mat[i][j]==1:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
            max_side = max(max_side, dp[i][j])


    return max_side


test=[[0,1,1],[1,1,0],[1,1,1]]

print(max_sub_square_ones(test))