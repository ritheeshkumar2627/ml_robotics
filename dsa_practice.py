def stair_case_search(mat,target):
    r=len(mat)
    c=len(mat[0])
    p=0
    q=c-1
    while p<r and c>=0:
        if mat[p][q]==target:
            return True
        elif target<mat[p][q]:
            q-=1
        else :
            p+=1
test=[[1,2,3],[4,5,6],[7,8,9]]

print(stair_case_search(test,7))