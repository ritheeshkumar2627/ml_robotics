def transpose(matrix):
    n=len(matrix)
    for i in range(n):
        for j in range(i+1,n):
            matrix[i][j],matrix[j][i]=matrix[j][i],matrix[i][j]

test_matrix =[[1,2,3],[0,0,0],[1,2,3]]
print("📥 Input Matrix Layout:")
for row in test_matrix:
    print(row)

# Run the transpose function (modifies the matrix directly in memory)
transpose(test_matrix)

print("\n📤 Transposed Output Matrix Layout:")
for row in test_matrix:
    print(row)
print("✅ Success! Matrix flipped diagonally with zero extra memory allocation.")