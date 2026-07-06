def find_common(mat):
    hash_map = {x: 1 for x in set(mat[0])}
    m=len(mat)
    n=len(mat[0])

    for i in range(1,m):
        for j in range(n):
            if mat[i][j] in hash_map and hash_map[mat[i][j]]==i:
                hash_map[mat[i][j]]=i+1

    
    target_value = int(m)

    # Gather keys where the value matches exactly
    matching_keys = [key for key, val in hash_map.items() if val == target_value]

    print(matching_keys)  

test=[[1,2,3],[2,4,2],[4,2,1]]

find_common(test)


